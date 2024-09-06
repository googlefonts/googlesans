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

from fontTools.ttLib import TTFont
import uharfbuzz as hb

ROOT = Path(__file__).parent.parent
FONT_PATHS = [
    (
        "Upright",
        ROOT / "build/GoogleSans/variable/GoogleSans-Italic[GRAD,opsz,wght].ttf",
    ),
    ("Italic", ROOT / "build/GoogleSans/variable/GoogleSans[GRAD,opsz,wght].ttf"),
]
TEST_LOCATIONS = [
    ("Text Regular GRAD -50", {"opsz": 17, "wght": 400, "GRAD": -50}),
    ("Text Regular GRAD 0", {"opsz": 17, "wght": 400, "GRAD": 0}),
    ("Text Regular GRAD 200", {"opsz": 17, "wght": 400, "GRAD": 200}),
    ("Text Bold GRAD -50", {"opsz": 17, "wght": 700, "GRAD": -50}),
    ("Text Bold GRAD 0", {"opsz": 17, "wght": 700, "GRAD": 0}),
    ("Text Bold GRAD 200", {"opsz": 17, "wght": 700, "GRAD": 200}),
    ("Display Regular GRAD -50", {"opsz": 18, "wght": 400, "GRAD": -50}),
    ("Display Regular GRAD 0", {"opsz": 18, "wght": 400, "GRAD": 0}),
    ("Display Regular GRAD 200", {"opsz": 18, "wght": 400, "GRAD": 200}),
    ("Display Bold GRAD -50", {"opsz": 18, "wght": 700, "GRAD": -50}),
    ("Display Bold GRAD 0", {"opsz": 18, "wght": 700, "GRAD": 0}),
    ("Display Bold GRAD 200", {"opsz": 18, "wght": 700, "GRAD": 200}),
]


@dataclass
class Report:
    font: str
    loc: str
    word: str
    script: str
    ascent_clip: int
    descent_clip: int


def main():
    test_words = load_test_words()

    reports = []

    for font_name, font_path in FONT_PATHS:
        tt = TTFont(font_path)
        os2_table = tt["OS/2"]
        typo_ascender = os2_table.sTypoAscender
        typo_descender = os2_table.sTypoDescender

        blob = hb.Blob.from_file_path(font_path)
        face = hb.Face(blob)
        font = hb.Font(face)

        for loc_name, loc in TEST_LOCATIONS:
            font.set_variations(loc)
            for word in test_words:
                script, ascent, descent = measure_vertical(font, word)

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


def load_test_words() -> list[str]:
    # return ["Hello", "లాక్ స్క్రీన్ విడ్జెట్‌లు"]  # For testing
    words = []
    for path in (Path(__file__).parent / "diffenator2-data").glob("*.txt"):
        for word in path.read_text().splitlines():
            if word:
                words.append(word)
    return words


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


def report_html(reports: list[Report]):
    # TODO: not implemented, not sure it's worth it? Lots of words, would make a gigantic page
    return
    # ~~~~~~~~~~~~~~~~~~
    #   HTML Reporting
    # ~~~~~~~~~~~~~~~~~~

    if len(bad_metrics_dict) > 0:
        sorted_scripts = sorted(bad_metrics_dict.keys())

        script_sections = []
        for script_name in sorted_scripts:
            glyph_sections = []
            for bad_glyph in sorted(
                bad_metrics_dict[script_name],
                key=lambda obj: (-obj["severity"], obj["glyph_name"]),
            ):
                glyph_sections.append(
                    f"""
                        <li>
                            <figure>
                                {glyph_to_svg.draw_with_metrics(tt, bad_glyph["glyph_name"])}
                                <figcaption>{bad_glyph["glyph_name"]}</figcaption>
                            </figure>
                        </li>
                    """
                )
            glyph_sections = "\n".join(glyph_sections)

            script_sections.append(
                f"""
                    <details>
                        <summary><h2>{script_name} ({len(bad_metrics_dict[script_name])})</h2></summary>
                        <ul class="drawn">
                            {glyph_sections}
                        </ul>
                    </details>
                """
            )
        script_sections = "\n".join(script_sections)

        style = """
            body {
                max-width: 1280px;
                margin: auto;

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
                    <style>{style}</style>
                </head>
                <body>
                    <h1>Tall Glyphs</h1>
                    <p>
                        Lines legend:<br>
                        <span style="color: green">green: [head.yMax, head.yMin]</span><br>
                        <span style="color: blue">blue: [os2.usWinAscent, -os2.usWinDescent]</span><br>
                        <span style="color: red">red: [os2.sTypoAscender, os2.sTypoDescender] = clipping limit for Android</span>
                    </p>
                    {script_sections}
                </body>
            </html>
        """

        Path(f"report_{font_path.stem}.html").write_text(template)


if __name__ == "__main__":
    main()
