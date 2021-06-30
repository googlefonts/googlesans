# Copyright 2021 Google Sans Authors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Framework to evaluate kerning reduction strategies.

This script tries various programmer-defined strategies to reduce/prune kerning
in order and compares size and advance-width changes.
"""

from __future__ import annotations

import csv
import json
import re
import statistics
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Mapping, Sequence, Set, Tuple

import requests
import ufo2ft
import ufoLib2
import uharfbuzz as hb
from fontTools import designspaceLib, unicodedata
from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.ttLib.ttFont import TTFont
from tqdm import tqdm

from . import compact_kern_feature_writer, drop_kerning, tighten

PACKAGE_DIR = Path(__file__).parent
DOWNLOADS = (Path(__file__) / "../../../downloads").resolve()
TEST_OUTPUT = (Path(__file__) / "../test_output/").resolve()

# TODO:
# - Use HarfBuzz to excercise kerning with various features (alternates, smcp)
# - Add more words and sentences from different languages
#   (http://unicode.org/udhr/downloads.html)
# - Add more words from some dictionary? Kerning words list? Should be short to
#   keep execution times low.
# - Report word and sentence changes per script/language?

# Ideas for configurations:
# - algorithmic respace + rekern + drop small values
# - swap out designspace with the one respaced and rekerned by hand by a designer
#   + drop small values
# - don't change input spacing or kerning but add ufo2ft key to trigger binary
#   optimization
# - combined: designer-led respace + rekern + algorithmic changes + drop small
#   + ufo2ft key


def main() -> None:
    all_sentences, all_words = get_sentences_and_words()
    for input in INPUTS:
        print(f"Preparing input for {input.designspace_path}")
        ds_before = DesignSpaceDocument.fromfile(input.designspace_path)
        ds_before.loadSourceFonts(ufoLib2.Font.open)

        code_points = get_code_points(ds_before)
        sentences = filter_all_code_points_covered(code_points, all_sentences)
        words = filter_all_code_points_covered(code_points, all_words)

        font_before = input.compile(ds_before)
        report_before = full_report(
            sentences,
            words,
            ds_before,
            font_before,
            input.test_locations,
            input.designspace_path.stem,
        )
        print_report(report_before, " # Before")
        del font_before

        reports: List[Tuple[str, Report]] = [("input", report_before)]
        scores: List[Score] = []  # overallscore
        for index, conf in enumerate(input.configurations):
            print(
                "\n"
                f"Running configuration {index + 1} of {len(input.configurations)}, "
                f'"{conf.name}", '
                f"for {input.designspace_path}"
            )
            # Reload fresh from disk
            ds_before = DesignSpaceDocument.fromfile(input.designspace_path)
            ds_before.loadSourceFonts(ufoLib2.Font.open)
            ds_after = conf.optimize(ds_before)
            font_after = conf.compile(ds_after)
            report_after = full_report(
                sentences,
                words,
                ds_after,
                font_after,
                input.test_locations,
                input.designspace_path.stem + "_" + sanitize(conf.name),
            )
            reports.append((conf.name, report_after))
            print_report(report_after, " # After")

            score = compute_score(conf, report_before, report_after)
            scores.append(score)
            print_score(score)

        # Output changes per word or sentence using various strategies.
        with open(
            TEST_OUTPUT / "words.csv", "w", newline="", encoding="utf-8"
        ) as csvfile:
            # Allow UTF-8 to work in Excel https://stackoverflow.com/a/16231345
            csvfile.write("\uFEFF")
            writer = csv.writer(csvfile)
            writer.writerow(
                ["word"]
                + [
                    col
                    for name, report in reports
                    for location, _ in report.reports.items()
                    for col in (
                        f"{location} {name} Length",
                        f"{location} {name} Change Percentage",
                    )
                ]
            )
            for word in words:
                row = [
                    word,
                    *[
                        val
                        for _, report in reports
                        for location, report_at_loc in report.reports.items()
                        for val in (
                            report_at_loc.word_length[word],
                            (
                                report_at_loc.word_length[word]
                                - report_before.reports[location].word_length[word]
                            )
                            / report_before.reports[location].word_length[word]
                            * 100.0,
                        )
                    ],
                ]
                writer.writerow(row)

        with open(
            TEST_OUTPUT / "sentences.csv", "w", newline="", encoding="utf-8"
        ) as csvfile:
            # Allow UTF-8 to work in Excel https://stackoverflow.com/a/16231345
            csvfile.write("\uFEFF")
            writer = csv.writer(csvfile)
            writer.writerow(
                ["sentence"]
                + [
                    col
                    for name, report in reports
                    for location, _ in report.reports.items()
                    for col in (
                        f"{location} {name} Length",
                        f"{location} {name} Change Percentage",
                    )
                ]
            )
            for sentence in sentences:
                writer.writerow(
                    [
                        sentence,
                        *[
                            val
                            for _, report in reports
                            for location, report_at_loc in report.reports.items()
                            for val in (
                                report_at_loc.sentence_length[sentence],
                                (
                                    report_at_loc.sentence_length[sentence]
                                    - report_before.reports[location].sentence_length[
                                        sentence
                                    ]
                                )
                                / report_before.reports[location].sentence_length[
                                    sentence
                                ]
                                * 100.0,
                            )
                        ],
                    ]
                )

        # Output comparison of score across strategies
        with open(
            TEST_OUTPUT / "score.csv", "w", newline="", encoding="utf-8"
        ) as csvfile:
            csvfile.write("\uFEFF")

            header = [
                "Name",
                "Font Bytes Before",
                "Font Bytes After",
                "Font Bytes Diff",
                "Font Bytes Percentage",
                "GPOS Bytes Before",
                "GPOS Bytes After",
                "GPOS Bytes Diff",
                "GPOS Bytes Percentage",
                "WOFF2 Bytes Before",
                "WOFF2 Bytes After",
                "WOFF2 Bytes Diff",
                "WOFF2 Bytes Percentage",
            ]
            header_per_location = [
                "Time Before",
                "Time After",
                "Time Diff",
                "Time Percentage",
                "Word Change Percentage Min",
                "Word Change Percentage 1",
                "Word Change Percentage 5",
                "Word Change Percentage 50",
                "Word Change Percentage 95",
                "Word Change Percentage 99",
                "Word Change Percentage Max",
                "Sentence Change Percentage Min",
                "Sentence Change Percentage 1",
                "Sentence Change Percentage 5",
                "Sentence Change Percentage 50",
                "Sentence Change Percentage 95",
                "Sentence Change Percentage 99",
                "Sentence Change Percentage Max",
            ]
            for location in TEST_LOCATIONS:
                header.extend([f"{location.name} {h}" for h in header_per_location])

            writer = csv.writer(csvfile)
            writer.writerow(header)
            for conf, score in zip(input.configurations, scores):
                row = [
                    conf.name,
                    score.before.font_bytes,
                    score.after.font_bytes,
                    score.font_bytes_diff,
                    score.font_bytes_percentage,
                    score.before.font_gpos_bytes,
                    score.after.font_gpos_bytes,
                    score.font_gpos_bytes_diff,
                    score.font_gpos_bytes_percentage,
                    score.before.font_woff2_bytes,
                    score.after.font_woff2_bytes,
                    score.font_woff2_bytes_diff,
                    score.font_woff2_bytes_percentage,
                ]

                for location in TEST_LOCATIONS:
                    score_at_loc = score.scores[location]
                    row.extend(
                        [
                            score_at_loc.before.time,
                            score_at_loc.after.time,
                            score_at_loc.time_diff,
                            score_at_loc.time_percentage,
                            min(score_at_loc.word_len_change_rel),
                            score_at_loc.word_len_change_rel_percentiles[0],
                            score_at_loc.word_len_change_rel_percentiles[9],
                            score_at_loc.word_len_change_rel_percentiles[49],
                            score_at_loc.word_len_change_rel_percentiles[89],
                            score_at_loc.word_len_change_rel_percentiles[98],
                            max(score_at_loc.word_len_change_rel),
                            min(score_at_loc.sentence_len_change_rel),
                            score_at_loc.sentence_len_change_rel_percentiles[0],
                            score_at_loc.sentence_len_change_rel_percentiles[9],
                            score_at_loc.sentence_len_change_rel_percentiles[49],
                            score_at_loc.sentence_len_change_rel_percentiles[89],
                            score_at_loc.sentence_len_change_rel_percentiles[98],
                            max(score_at_loc.sentence_len_change_rel),
                        ]
                    )

                writer.writerow(row)


@dataclass(frozen=True)
class Location:
    name: str
    location: Tuple[Tuple[str, float], ...]

    def __str__(self):
        loc = ", ".join(f"{k}={v}" for (k, v) in self.location)
        return f"{self.name} ({loc})"


@dataclass
class Input:
    designspace_path: Path
    test_locations: List["Location"]
    compile: Callable
    configurations: List["Configuration"]


@dataclass
class Configuration:
    name: str
    optimize: Callable[[DesignSpaceDocument], DesignSpaceDocument]
    compile: Callable


TEST_LOCATIONS = [
    Location("Bold", (("opsz", 18), ("wght", 700), ("GRAD", 0))),
    Location("Regular GRAD-50", (("opsz", 18), ("wght", 400), ("GRAD", -50))),
    Location("Regular", (("opsz", 18), ("wght", 400), ("GRAD", 0))),
    Location("Regular GRAD200", (("opsz", 18), ("wght", 400), ("GRAD", 200))),
    Location("Text Bold", (("opsz", 17), ("wght", 700), ("GRAD", 0))),
    Location("Text Regular GRAD-50", (("opsz", 17), ("wght", 400), ("GRAD", -50))),
    Location("Text Regular", (("opsz", 17), ("wght", 400), ("GRAD", 0))),
    Location("Text Regular GRAD200", (("opsz", 17), ("wght", 400), ("GRAD", 200))),
]

INPUTS = [
    Input(
        PACKAGE_DIR / "../../source/GoogleSans/GoogleSans.designspace",
        TEST_LOCATIONS,
        lambda source: ufo2ft.compileVariableTTF(source),
        [
            Configuration(
                "Do nothing",
                lambda source: source,
                lambda source: ufo2ft.compileVariableTTF(source),
            ),
            Configuration(
                "Drop all kerning",
                lambda source: drop_kerning.drop_all(source),
                lambda source: ufo2ft.compileVariableTTF(source),
            ),
            Configuration(
                "Drop kerning < 5 font units",
                lambda source: drop_kerning.drop_threshold(source, 5),
                lambda source: ufo2ft.compileVariableTTF(source),
            ),
            Configuration(
                "Drop kerning < 10 font units",
                lambda source: drop_kerning.drop_threshold(source, 10),
                lambda source: ufo2ft.compileVariableTTF(source),
            ),
            Configuration(
                "Drop kerning < 10 font units and tighten all side-bearings by 1 fU",
                lambda source: tighten.drop_and_tighten(source),
                lambda source: ufo2ft.compileVariableTTF(source),
            ),
            Configuration(
                "Drop kerning < 20 font units",
                lambda source: drop_kerning.drop_threshold(source, 20),
                lambda source: ufo2ft.compileVariableTTF(source),
            ),
            Configuration(
                "Compact GPOS 1 subtable",
                lambda source: source,
                lambda source: compact_kern_feature_writer.compact(
                    ufo2ft.compileVariableTTF(source), mode="one"
                ),
            ),
            Configuration(
                "Compact GPOS max subtables",
                lambda source: source,
                lambda source: compact_kern_feature_writer.compact(
                    ufo2ft.compileVariableTTF(source), mode="max"
                ),
            ),
            Configuration(
                "Compact GPOS auto subtables",
                lambda source: source,
                lambda source: compact_kern_feature_writer.compact(
                    ufo2ft.compileVariableTTF(source), mode="auto"
                ),
            ),
            Configuration(
                "Compact GPOS auto2 subtables",
                lambda source: source,
                lambda source: compact_kern_feature_writer.compact(
                    ufo2ft.compileVariableTTF(source),
                    mode="auto",
                    clustering_kwargs={"lines_per_cluster": 3.8},
                ),
            ),
            Configuration(
                "Drop kerning < 20 font units + compact GPOS auto",
                lambda source: drop_kerning.drop_threshold(source, 20),
                lambda source: compact_kern_feature_writer.compact(
                    ufo2ft.compileVariableTTF(source), mode="auto"
                ),
            ),
        ],
    )
]


# TODO: Store different HarfBuzz options along with their results.
@dataclass
class Report:
    font_bytes: int
    font_gpos_bytes: int
    font_woff2_bytes: int
    source_kern_entries: Dict[str, int]
    reports: Dict[Location, ReportAtLocation]


@dataclass
class ReportAtLocation:
    word_length: Dict[str, int]
    words_time: float
    sentence_length: Dict[str, int]
    sentences_time: float

    @property
    def time(self) -> float:
        return self.words_time + self.sentences_time


def full_report(
    sentences: List[str],
    words: List[str],
    designspace: DesignSpaceDocument,
    font: TTFont,
    test_locations: List[Location],
    filename_stem: str,
) -> Report:
    path = TEST_OUTPUT / (filename_stem + ".ttf")
    path_woff2 = path.with_suffix(".woff2")

    change_family_name(font, filename_stem)
    path.parent.mkdir(parents=True, exist_ok=True)
    font.save(path)
    total_size = path.stat().st_size
    gpos_size = len(font.getTableData("GPOS"))

    font.flavor = "woff2"
    font.save(path_woff2)
    woff2_size = path_woff2.stat().st_size

    source_kern_entries = {}
    for source in designspace.sources:
        source_kern_entries[source.name] = len(source.font.kerning)

    hb_font = hb.Font(hb.Face(path.read_bytes()))

    reports = {}
    for location in test_locations:
        words_start = time.process_time()
        word_length = {}
        for word in tqdm(words, desc="Measuring words"):
            word_length[word] = shaped_text_length(
                hb_font, word, location, features={"kern": True}
            )
        words_end = time.process_time()

        sentences_start = time.process_time()
        sentence_length = {}
        for sentence in tqdm(sentences, desc="Measuring sentences"):
            sentence_length[sentence] = shaped_text_length(
                hb_font, sentence, location, features={"kern": True}
            )
        sentences_end = time.process_time()

        reports[location] = ReportAtLocation(
            word_length=word_length,
            words_time=words_end - words_start,
            sentence_length=sentence_length,
            sentences_time=sentences_end - sentences_start,
        )

    return Report(
        font_bytes=total_size,
        font_gpos_bytes=gpos_size,
        font_woff2_bytes=woff2_size,
        source_kern_entries=source_kern_entries,
        reports=reports,
    )


def shaped_text_length(
    hb_font: hb.Font, text: str, location: Location, features: Dict[str, bool]
) -> int:
    hb_font.set_variations(dict(location.location))
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hb_font, buf, features)
    return sum(p.x_advance for p in buf.glyph_positions)


@dataclass
class Score:
    before: Report
    after: Report
    scores: Dict[Location, ScoreAtLocation]
    source_kern_entries_diff: Mapping[str, float]

    @property
    def font_bytes_diff(self) -> float:
        return self.after.font_bytes - self.before.font_bytes

    @property
    def font_bytes_percentage(self) -> float:
        return self.font_bytes_diff / self.before.font_bytes * 100

    @property
    def font_gpos_bytes_diff(self) -> float:
        return self.after.font_gpos_bytes - self.before.font_gpos_bytes

    @property
    def font_gpos_bytes_percentage(self) -> float:
        return self.font_gpos_bytes_diff / self.before.font_gpos_bytes * 100

    @property
    def font_woff2_bytes_diff(self) -> float:
        return self.after.font_woff2_bytes - self.before.font_woff2_bytes

    @property
    def font_woff2_bytes_percentage(self) -> float:
        return self.font_woff2_bytes_diff / self.before.font_woff2_bytes * 100


@dataclass
class ScoreAtLocation:
    before: ReportAtLocation
    after: ReportAtLocation
    word_len_change_abs: Sequence[float]
    word_len_change_rel: Sequence[float]
    word_len_change_rel_percentiles: Sequence[float]
    sentence_len_change_abs: Sequence[float]
    sentence_len_change_rel: Sequence[float]
    sentence_len_change_rel_percentiles: Sequence[float]

    @property
    def time_diff(self) -> float:
        return self.after.time - self.before.time

    @property
    def time_percentage(self) -> float:
        return self.time_diff / self.before.time * 100


def compute_score(conf: Configuration, before: Report, after: Report) -> Score:
    source_kern_entries_diff = {}
    for ((name1, before_len), (name2, after_len)) in zip(
        before.source_kern_entries.items(), after.source_kern_entries.items()
    ):
        assert name1 == name2
        source_kern_entries_diff[name1] = after_len - before_len

    scores_at_locations = {}
    for location in before.reports.keys():
        before_at_loc = before.reports[location]
        after_at_loc = after.reports[location]

        word_len_change_abs = []
        word_len_change_rel = []
        for ((word1, before_len), (word2, after_len)) in zip(
            before_at_loc.word_length.items(), after_at_loc.word_length.items()
        ):
            assert word1 == word2
            word_len_change_abs.append(after_len - before_len)
            word_len_change_rel.append((after_len - before_len) / before_len * 100)
        word_len_change_rel_percentiles = statistics.quantiles(
            word_len_change_rel, n=100, method="inclusive"
        )

        sentence_len_change_abs = []
        sentence_len_change_rel = []
        for ((sentence1, before_len), (sentence2, after_len)) in zip(
            before_at_loc.sentence_length.items(), after_at_loc.sentence_length.items()
        ):
            assert sentence1 == sentence2
            sentence_len_change_abs.append(after_len - before_len)
            sentence_len_change_rel.append((after_len - before_len) / before_len * 100)
        sentence_len_change_rel_percentiles = statistics.quantiles(
            sentence_len_change_rel, n=100, method="inclusive"
        )

        scores_at_locations[location] = ScoreAtLocation(
            before=before_at_loc,
            after=after_at_loc,
            word_len_change_abs=word_len_change_abs,
            word_len_change_rel=word_len_change_rel,
            word_len_change_rel_percentiles=word_len_change_rel_percentiles,
            sentence_len_change_abs=sentence_len_change_abs,
            sentence_len_change_rel=sentence_len_change_rel,
            sentence_len_change_rel_percentiles=sentence_len_change_rel_percentiles,
        )

    return Score(
        before=before,
        after=after,
        scores=scores_at_locations,
        source_kern_entries_diff=source_kern_entries_diff,
    )


def print_report(report: Report, header: str) -> None:
    print(header)
    print(f" Total size: {report.font_bytes:,d} bytes")
    print(f" GPOS size:  {report.font_gpos_bytes:,d} bytes")
    print(f" WOFF2 size: {report.font_woff2_bytes:,d} bytes")
    for location, report_at_location in report.reports.items():
        print(
            f" {location}: Words + sentences time: "
            f"{int(report_at_location.time*1000):,d} ms"
        )

    # print(" Source kern entries:")
    # for name, amount in report.source_kern_entries.items():
    #     print(f"    {name}: {amount}")
    # print(" Word lengths:")
    # for word, length in report.word_length.items():
    #     print(f"    {word}: {length}")
    # print(" Sentence lengths:")
    # for sentence, length in report.sentence_length.items():
    #     print(f"    {sentence}: {length}")


def print_score(score: Score) -> None:
    print(" # Difference")
    print(
        f" Total size diff: {score.font_bytes_diff:,d} bytes "
        f"({score.font_bytes_percentage:.1f}%)"
    )
    print(
        f" GPOS size diff:  {score.font_gpos_bytes_diff:,d} bytes "
        f"({score.font_gpos_bytes_percentage:.1f}%)"
    )
    print(
        f" WOFF2 size diff: {score.font_woff2_bytes_diff:,d} bytes "
        f"({score.font_woff2_bytes_percentage:.1f}%)"
    )

    for loc, score_at_loc in score.scores.items():
        print(f" {loc}:")
        print(
            f"  Words + sentences time diff: {int(score_at_loc.time_diff*1000):,d} ms "
            f"({score_at_loc.time_percentage:.1f}%)"
        )

        wlen_change_abs = score_at_loc.word_len_change_abs
        wlen_change_rel = score_at_loc.word_len_change_rel
        w_min, w_max = min(wlen_change_abs), max(wlen_change_abs)
        w_min_rel, w_max_rel = min(wlen_change_rel), max(wlen_change_rel)
        print(
            "  Word length diffs, min and max: "
            f"{w_min} ({w_min_rel:.1f}%), {w_max} ({w_max_rel:.1f}%)"
        )
        w_p = score_at_loc.word_len_change_rel_percentiles
        print(
            "  Word length diffs, 1., 10., 50., 90., 99. percentile: "
            f"{w_p[0]:.1f}, {w_p[9]:.1f}, {w_p[49]:.1f}, {w_p[89]:.1f}, {w_p[98]:.1f}%"
        )

        slen_change_abs = score_at_loc.sentence_len_change_abs
        slen_change_rel = score_at_loc.sentence_len_change_rel
        s_min, s_max = min(slen_change_abs), max(slen_change_abs)
        s_min_rel, s_max_rel = min(slen_change_rel), max(slen_change_rel)
        print(
            "  Sentence length diffs, min and max: "
            f"{s_min} ({s_min_rel:.1f}%), {s_max} ({s_max_rel:.1f}%)"
        )
        s_p = score_at_loc.sentence_len_change_rel_percentiles
        print(
            "  Sentence length diffs, 1., 10., 50., 90., 99. percentile: "
            f"{s_p[0]:.1f}, {s_p[9]:.1f}, {s_p[49]:.1f}, {s_p[89]:.1f}, {s_p[98]:.1f}%"
        )


def get_sentences_and_words():
    # return ["Hello world!", "Bonjour le monde!"], ["Hello", "Bonjour"]
    print("Loading sentences and words")
    sentences = set()
    words = set()

    # Download UDHR instead of committing it to the repository (for licence reasons)
    udhr_full_all_path = DOWNLOADS / "udhr_full_all.txt"
    udhr_full_all = cache_download(
        "https://unicode.org/udhr/assemblies/full_all.txt", udhr_full_all_path
    )
    for s in udhr_full_all.splitlines():
        if not re.match(r"^(\s|\n)*$", s) and len(s) > 20:
            sentences.add(s)
        for w in s.split():
            if len(w) > 1:
                words.add(w)

    # Load strings extracted from Android Open Source apps
    json_string = cache_download(
        "https://github.com/googlefonts/aosp-test-texts/raw/main/corpus/aosp.json",
        DOWNLOADS / "aosp.json",
    )
    aosp = json.loads(json_string)
    # Keys are strings, values are where the string came from
    for s in aosp:
        # Upstream string sources may contain questionable data. Filter those to
        # avoid unrenderable sentences and words with zero length -> division by zero.
        s_filtered = "".join(c for c in s if not unicodedata.category(c).startswith("C"))
        if len(s_filtered) > 20:
            sentences.add(s_filtered)
        for w in s_filtered.split():
            if len(w) > 1:
                words.add(w)

    return sorted(sentences), sorted(words)


def cache_download(url: str, path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    response = requests.get(url)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fp:
        fp.write(response.text)
    return response.text


def get_code_points(ds: designspaceLib.DesignSpaceDocument) -> Set[int]:
    code_points = set()
    source = ds.findDefault()
    for g in source.font:
        code_points.update(g.unicodes)
    return code_points


def filter_all_code_points_covered(
    code_points: Set[int], strings: List[str]
) -> List[str]:
    chars = frozenset(chr(c) for c in code_points)
    return [s for s in strings if all(c in chars for c in s)]


def sanitize(string: str) -> str:
    return re.sub(r"[^A-Za-z0-9_\-]+", "_", string)


def change_family_name(font: TTFont, family_name_new: str) -> None:
    font_name_table = font["name"]

    family_name = get_family_name(font)
    family_name_no_space = family_name.replace(" ", "")
    family_name_no_space_new = family_name_new.replace(" ", "")

    for record in font_name_table.names:
        if record.nameID in {1, 4, 16, 18, 21}:
            record.string = record.toUnicode().replace(family_name, family_name_new, 1)
        elif record.nameID in {3, 6, 20}:
            # Unique ID or PostScript or PostScript CID findfont name: no spaces
            record.string = record.toUnicode().replace(
                family_name_no_space, family_name_no_space_new, 1
            )


def get_family_name(font: TTFont) -> str:
    names = font["name"]
    return (names.getName(16, 3, 1) or names.getName(1, 3, 1)).toStr()
