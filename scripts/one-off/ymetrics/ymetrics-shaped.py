# Copyright 2024 Google, LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Measure vertical metrics of words shaped by Harfbuzz, and report the ones
that would clip on Android.

Based on code by Behdad here:
https://gist.github.com/behdad/ed41c78d508226015750e03ab13f6425
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json
import random
from collections import defaultdict

from fontTools.ttLib import TTFont
from fontTools import unicodedata
import uharfbuzz as hb

import glyph_to_svg


ROOT = Path(__file__).parent.parent
FONT_PATHS = {
    "Upright": ROOT / "build/GoogleSans/variable/GoogleSans[GRAD,opsz,wght].ttf",
    "Italic": ROOT / "build/GoogleSans/variable/GoogleSans-Italic[GRAD,opsz,wght].ttf",
}
TEST_LOCATIONS = {
    # "Text Regular GRAD -50": {"opsz": 17, "wght": 400, "GRAD": -50},
    "Text Regular GRAD 0": {"opsz": 17, "wght": 400, "GRAD": 0},
    # "Text Regular GRAD 200": {"opsz": 17, "wght": 400, "GRAD": 200},
    # "Text Bold GRAD -50": {"opsz": 17, "wght": 700, "GRAD": -50},
    "Text Bold GRAD 0": {"opsz": 17, "wght": 700, "GRAD": 0},
    # "Text Bold GRAD 200": {"opsz": 17, "wght": 700, "GRAD": 200},
    # "Display Regular GRAD -50": {"opsz": 18, "wght": 400, "GRAD": -50},
    "Display Regular GRAD 0": {"opsz": 18, "wght": 400, "GRAD": 0},
    # "Display Regular GRAD 200": {"opsz": 18, "wght": 400, "GRAD": 200},
    # "Display Bold GRAD -50": {"opsz": 18, "wght": 700, "GRAD": -50},
    "Display Bold GRAD 0": {"opsz": 18, "wght": 700, "GRAD": 0},
    # "Display Bold GRAD 200": {"opsz": 18, "wght": 700, "GRAD": 200},
}
AOSP_DUMP = Path(__file__).parent / "diffenator2-data/aosp.json"
NUMBER_PER_SOURCE_PER_SIDE = 5


@dataclass
class Word:
    word: str
    source: str


@dataclass
class Report:
    font: str
    loc: str
    word: Word
    script: str
    ascent_clip: int
    descent_clip: int


def main() -> None:
    test_words = load_test_words(sample_size_per_list=5_000, sample_size_aosp=None)

    reports: list[Report] = []

    for font_name, font_path in FONT_PATHS.items():
        tt = TTFont(font_path)
        os2_table = tt["OS/2"]
        typo_ascender = os2_table.sTypoAscender
        typo_descender = os2_table.sTypoDescender

        blob = hb.Blob.from_file_path(font_path)
        face = hb.Face(blob)
        font = hb.Font(face)

        for loc_name, loc in TEST_LOCATIONS.items():
            font.set_variations(loc)
            for word in test_words:
                script, ascent, descent = measure_vertical(font, word.word)

                ascent_clip = max(0, ascent - typo_ascender)
                descent_clip = max(0, typo_descender - descent)
                if ascent_clip or descent_clip:
                    report = Report(
                        font=font_name,
                        loc=loc_name,
                        word=word,
                        script=script,
                        ascent_clip=ascent_clip,
                        descent_clip=descent_clip,
                    )
                    report_terminal(report)
                    reports.append(report)

    report_csv(reports)
    report_html(reports)


def report_html(reports: list[Report]):
    # Select the worst N reports for each script, generate an HTML report
    # showing those words with lines.
    by_script: defaultdict[str, list[Report]] = defaultdict(list)
    for report in reports:
        by_script[report.script].append(report)

    script_sections = []
    for script, all_reports in sorted(by_script.items()):
        glyph_sections = []
        for source in ("AOSP", "other"):
            reports = [
                report
                for report in all_reports
                if report.word.source.startswith(source)
            ]
            reports = sorted(reports, key=lambda r: (-r.ascent_clip, -r.descent_clip))
            worst_ascents = reports[:NUMBER_PER_SOURCE_PER_SIDE]
            reports = sorted(
                reports[NUMBER_PER_SOURCE_PER_SIDE:],
                key=lambda r: (-r.descent_clip, -r.ascent_clip),
            )
            worst_descents = reports[:NUMBER_PER_SOURCE_PER_SIDE]
            for report in worst_ascents:
                glyph_sections.append(
                    f"""
                        <li>
                            <figure>
                                {draw_svg(report)}
                                <figcaption>
                                {report.word.word} (from {report.word.source})<br>
                                (ascent_clip {report.ascent_clip}
                                    descent_clip {report.descent_clip})<br>
                                {report.font} {report.loc}
                                </figcaption>
                            </figure>
                        </li>
                    """
                )
            for report in worst_descents:
                glyph_sections.append(
                    f"""
                        <li>
                            <figure>
                                {draw_svg(report)}
                                <figcaption>
                                {report.word.word} (from {report.word.source})<br>
                                (ascent_clip {report.ascent_clip}
                                    descent_clip {report.descent_clip})<br>
                                {report.font} {report.loc}
                                </figcaption>
                            </figure>
                        </li>
                    """
                )

        script_sections.append(
            f"""
                <details open>
                    <summary><h2>{script}</h2></summary>
                    <ul class="drawn">
                        {"\n".join(glyph_sections)}
                    </ul>
                </details>
            """
        )

    style = """
        body {
            margin: 1em;

            font-family: sans-serif;
        }

        h1 {
            text-align: center;
        }

        details {
            margin: 4rem 0;
        }

        summary h2 {
            display: inline;
        }

        ul.drawn {
            list-style: none;
            margin-left: 0;
            padding-left: 0;

            display: flex;
            flex-wrap: wrap;
            gap: 2rem;
        }

        .drawn figure {
            margin: 0;
        }

        .drawn figcaption {
            font-family: monospace;
            text-align: center;
        }

        .drawn svg {
            height: 256px;
            border: 1px grey dashed;
            padding: 1rem;
        }
    """

    template = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>Tall Glyphs</title>
                <meta charset="utf-8"/>
                <style>{style}</style>
            </head>
            <body>
                <h1>Tall Glyphs</h1>
                <p>
                    Lines legend:<br>
                    <span style="color: green">
                        green: [head.yMax, head.yMin]
                    </span><br>
                    <span style="color: blue">
                        blue: [os2.usWinAscent, -os2.usWinDescent]
                    </span><br>
                    <span style="color: red">
                        red: [os2.sTypoAscender, os2.sTypoDescender]
                        = clipping limit for Android
                    </span>
                </p>
                {"\n".join(script_sections)}
            </body>
        </html>
    """

    Path("report_ymetrics_shaped.html").write_text(template)


def draw_svg(report: Report) -> str:
    font_path = FONT_PATHS[report.font]
    # FIXME: wasteful to reload everything but only for 10s of worst offenders
    tt = TTFont(font_path)
    blob = hb.Blob.from_file_path(font_path)
    face = hb.Face(blob)
    font = hb.Font(face)
    font.set_variations(TEST_LOCATIONS[report.loc])
    buffer = hb.Buffer()
    buffer.add_str(report.word.word)
    buffer.guess_segment_properties()
    hb.shape(font, buffer)
    return glyph_to_svg.draw_buffer_with_metrics(tt, font, buffer)


def load_test_words(
    sample_size_per_list: int | None = None, sample_size_aosp: int | None = None
) -> list[Word]:
    # return ["Hello", "లాక్ స్క్రీన్ విడ్జెట్‌లు"]  # For testing
    words_by_source: dict[str, str] = {}
    for path in (Path(__file__).parent / "diffenator2-data").glob("*.txt"):
        all_words = [
            line
            for line in path.read_text().splitlines()
            if line and not line.startswith("#")
        ]
        if sample_size_per_list is None or sample_size_per_list >= len(all_words):
            for word in all_words:
                words_by_source[word] = "other"
        else:
            random.seed("Google")
            for word in random.sample(all_words, sample_size_per_list):
                words_by_source[word] = "other"

    if AOSP_DUMP.exists():
        aosp_dump = json.loads(AOSP_DUMP.read_text(encoding="utf-8"))
        aosp_words_set = {
            "".join(
                char for char in word if not unicodedata.category(char).startswith("C")
            )
            for string in aosp_dump.keys()
            for word in string.split()
        }
        # There was probably at least one empty word
        aosp_words_set.remove("")
        # Filter out "words" that are a mix of scripts, such
        # as "<strong>ຕັ້ງເປັນຮູບພື້ນຫຼັງ</strong>"
        aosp_words = [
            w
            for w in aosp_words_set
            if len(
                set(unicodedata.script(c) for c in w).difference("Zinh", "Zyyy", "Zzzz")
            )
            <= 1
        ]

        if sample_size_aosp is None or sample_size_aosp >= len(aosp_words):
            for word in aosp_words:
                words_by_source[word] = "AOSP"
        else:
            random.seed("Google")
            for word in random.sample(aosp_words, sample_size_aosp):
                words_by_source[word] = "AOSP"
    else:
        raise ValueError(
            "Download the AOSP aosp.json to scripts/diffenator2-data to have "
            "that be used as well: "
            "https://github.com/googlefonts/aosp-test-texts/blob/main/corpus/aosp.json"
        )

    return [Word(word, source) for word, source in sorted(words_by_source.items())]


def measure_vertical(font: hb.Font, text: str) -> tuple[str, int, int]:
    ascent = descent = 0

    buffer = hb.Buffer()
    buffer.add_str(text)
    buffer.guess_segment_properties()

    hb.shape(font, buffer)

    infos = buffer.glyph_infos
    positions = buffer.glyph_positions
    for info, pos in zip(infos, positions):
        gid = info.codepoint
        yoffset = pos.y_offset
        extents = font.get_glyph_extents(gid)
        ascent = max(ascent, yoffset + extents.y_bearing)
        descent = min(descent, yoffset + extents.y_bearing + extents.height)

    return buffer.script, ascent, descent


def report_terminal(report: Report):
    print(
        f"{report.font} @ {report.loc} [{report.script}] "
        f"ascent_clip {report.ascent_clip: 6d} descent_clip {report.descent_clip: 6d}"
        f"{report.word}"
    )


def report_csv(reports: list[Report]):
    with open("ymetrics_shaped.csv", "w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(
            fp,
            fieldnames=["font", "loc", "word", "script", "ascent_clip", "descent_clip"],
        )
        writer.writeheader()
        for report in reports:
            writer.writerow(asdict(report))


if __name__ == "__main__":
    main()
