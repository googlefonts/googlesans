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

from dataclasses import dataclass
from pathlib import Path

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
TEST_LOCATIONS = [("Default", {})]
TEST_WORDS = [
    "Hello",
    "లాక్ స్క్రీన్ విడ్జెట్‌లు",
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
            for word in TEST_WORDS:
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

    report_html(reports)


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
        f"{report.font} @ {report.loc} [{report.script}] ascent_clip {report.ascent_clip: 6d} descent_clip {report.descent_clip: 6d} {report.word}"
    )


def report_html(reports: list[Report]):
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
