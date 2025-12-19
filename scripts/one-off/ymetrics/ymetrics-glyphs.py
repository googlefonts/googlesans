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

from collections import defaultdict
from dataclasses import asdict, dataclass
import unicodedata
from pathlib import Path
import csv

import glyph_to_svg
from fontTools import unicodedata as ft_unicodedata
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont
from ufo2ft.util import classifyGlyphs

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


@dataclass
class Report:
    font: str
    loc: str
    glyph_name: str
    uni_script_code: str
    uni_script: str
    uni_name: str
    uni_code_points: list[int]
    y_min: int
    y_max: int
    uni_block: str
    uni_category: str
    ascent_clip: int
    descent_clip: int


def report_glyphs() -> None:
    """Find glyphs that clip in any of the designspace locations above."""
    font_to_ttfont = {}

    # create results data structures for reporting
    reports: list[Report] = []

    for font_name, font_path in FONT_PATHS.items():
        tt = TTFont(font_path)
        font_to_ttfont[font_name] = tt
        os2_table = tt["OS/2"]
        typo_ascender = os2_table.sTypoAscender
        typo_descender = os2_table.sTypoDescender

        cmap_table = tt.getBestCmap()
        reverse_cmap: defaultdict[str, set[int]] = defaultdict(set)
        for code_point, name in cmap_table.items():
            reverse_cmap[name].add(code_point)

        # Prepare scripts for each glyph using GSUB closure for better reporting
        glyph_to_scripts: defaultdict[str, set[str]] = defaultdict(set)
        # Do script first, higher chance of getting Telugu stuff right
        glyphs_by_script: dict[str, set[str]] = classifyGlyphs(
            ft_unicodedata.script,
            cmap_table,
            tt["GSUB"],
        )
        for script, glyphs in glyphs_by_script.items():
            for glyph in glyphs:
                glyph_to_scripts[glyph].add(script)
        # Also do script extensions if that can give more info
        glyphs_by_script_extension: dict[str, set[str]] = classifyGlyphs(
            ft_unicodedata.script_extension,
            cmap_table,
            tt["GSUB"],
        )
        for script, glyphs in glyphs_by_script_extension.items():
            for glyph in glyphs:
                glyph_to_scripts[glyph].add(script)

        for loc_name, loc in TEST_LOCATIONS.items():
            print(f"Checking {font_name} at {loc_name}")
            glyph_set = tt.getGlyphSet(location=loc)

            # testing block
            for glyph_name in tt.getGlyphOrder():
                glyph = glyph_set[glyph_name]
                bounds_pen = BoundsPen(glyph_set)
                glyph.draw(bounds_pen)
                bounds = bounds_pen.bounds

                if bounds is None:
                    continue

                (_, y_min, _, y_max) = bounds_pen.bounds
                is_bad = y_min < typo_descender or y_max > typo_ascender

                if is_bad:
                    # Code point for reporting: use the actual ones from the glyph
                    uni_code_points = reverse_cmap.get(glyph_name, [None])
                    for code_point in uni_code_points:
                        uni_block = (
                            ft_unicodedata.block(chr(code_point))
                            if code_point is not None
                            else "Unknown"
                        )
                        uni_name = (
                            ft_unicodedata.name(chr(code_point), "No Unicode name")
                            if code_point is not None
                            else "Unknown"
                        )
                        uni_category = (
                            unicodedata.category(chr(code_point))
                            if code_point is not None
                            else "Unknown"
                        )

                        for uni_script_code in glyph_to_scripts.get(
                            glyph_name, ["Unknown"]
                        ):
                            uni_script = ft_unicodedata.script_name(
                                uni_script_code, default="Unknown"
                            )

                            reports.append(
                                Report(
                                    font=font_name,
                                    loc=loc_name,
                                    glyph_name=glyph_name,
                                    uni_script_code=uni_script_code,
                                    uni_script=uni_script,
                                    uni_name=uni_name,
                                    uni_code_points=sorted(uni_code_points),
                                    y_min=y_min,
                                    y_max=y_max,
                                    uni_block=uni_block,
                                    uni_category=uni_category,
                                    ascent_clip=max(0, y_max - typo_ascender),
                                    descent_clip=max(0, typo_descender - y_min),
                                )
                            )

    # overall script results
    reports_by_script: defaultdict[str, list[Report]] = defaultdict(list)
    for report in reports:
        reports_by_script[report.uni_script].append(report)
    sorted_scripts = sorted(reports_by_script.items())

    # ~~~~~~~~~~~~~~~~~~
    #   Text Reporting
    # ~~~~~~~~~~~~~~~~~~
    print(
        "Scripts with metrics that extend beyond OS/2 table global "
        "typo metrics values:"
    )
    for script, _script_reports in sorted_scripts:
        print(script)

    for script, script_reports in sorted_scripts:
        print(f"\n\n{script}:")
        for report in script_reports:
            errors = []
            if report.ascent_clip > 0:
                errors.append(f"ascent clips by {report.ascent_clip}")
            if report.descent_clip > 0:
                errors.append(f"descent clips by {report.descent_clip}")
            print(
                f"  {report.glyph_name} ({report.uni_name}, "
                f"{report.uni_code_points}, {report.uni_block}, "
                f"Category: {report.uni_category}): {' and '.join(errors)}"
            )

    with open("ymetrics_glyphs.csv", "w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(
            fp,
            fieldnames=[
                "font",
                "loc",
                "glyph_name",
                "uni_script_code",
                "uni_script",
                "uni_name",
                "uni_code_points",
                "y_min",
                "y_max",
                "uni_block",
                "uni_category",
                "ascent_clip",
                "descent_clip",
            ],
        )
        writer.writeheader()
        for report in reports:
            writer.writerow(asdict(report))

    # ~~~~~~~~~~~~~~~~~~
    #   HTML Reporting
    # ~~~~~~~~~~~~~~~~~~
    script_sections = []
    for script_name, script_reports in sorted_scripts:
        glyph_sections = []
        for report in sorted(
            script_reports,
            key=lambda report: (
                max(report.ascent_clip, report.descent_clip),
                report.glyph_name,
            ),
        ):
            glyph_sections.append(
                f"""
                    <li>
                        <figure>
                            {
                                glyph_to_svg.draw_with_metrics(
                                    font_to_ttfont[report.font],
                                    report.glyph_name,
                                    TEST_LOCATIONS[report.loc],
                                )
                            }
                            <figcaption>
                                {report.glyph_name}<br>
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
                <details>
                    <summary>
                        <h2>{script_name} ({len(reports_by_script[script_name])})</h2>
                    </summary>
                    <ul class="drawn">
                        {"\n".join(glyph_sections)}
                    </ul>
                </details>
            """
        )

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

    Path("report_glyphs.html").write_text(template)


if __name__ == "__main__":
    report_glyphs()
