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

import sys
import unicodedata
from pathlib import Path

import glyph_to_svg
from fontTools import unicodedata as ft_unicodedata
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont


def report_glyphs(font_path: Path) -> None:
    # fonttools TTFont object
    tt = TTFont(font_path)

    # Define tables, metrics, glyph sets of interest
    os2_table = tt["OS/2"]
    typo_ascender = os2_table.sTypoAscender
    typo_descender = os2_table.sTypoDescender

    glyph_set = tt.getGlyphSet()
    cmap_table = tt.getBestCmap()

    # create results data structures for reporting
    bad_metrics_dict = {}
    error_list = []

    # testing block
    for glyph_name in tt.getGlyphOrder():
        glyph = glyph_set[glyph_name]
        bounds_pen = BoundsPen(glyph_set)
        glyph.draw(bounds_pen)
        bounds = bounds_pen.bounds

        if bounds is None:
            continue

        (_, y_min, _, y_max) = bounds_pen.bounds

        # Unicode data
        uni_script = None
        uni_block = None
        uni_name = None
        uni_codepoint = None
        uni_category = None

        try:
            for codepoint, name in cmap_table.items():
                if name == glyph_name:
                    uni_script_code = ft_unicodedata.script(chr(codepoint))
                    uni_script = ft_unicodedata.script_name(
                        uni_script_code, default="Unknown"
                    )
                    uni_block = ft_unicodedata.block(chr(codepoint))
                    uni_name = unicodedata.name(chr(codepoint), "No Unicode name")
                    uni_codepoint = hex(codepoint)
                    uni_category = unicodedata.category(chr(codepoint))
            if uni_script is None:
                uni_script = "Unknown"
            if uni_block is None:
                uni_block = "Unknown"
            if uni_name is None:
                uni_name = "Unknown"
            if uni_codepoint is None:
                uni_codepoint = "Unencoded"
            if uni_category is None:
                uni_category = "Unknown"
        except Exception as e:
            uni_script = "Unknown"
            uni_block = "Unknown"
            uni_name = "Unknown"
            uni_codepoint = "Unknown"
            uni_category = "Unknown"
            raise e

        bad_flag = None

        if y_min is not None and y_max is not None:
            if y_min < typo_descender and y_max <= typo_ascender:
                error_string = f"yMin ({y_min}) below typoDescender ({typo_descender})"
                bad_flag = True
            elif y_min >= typo_descender and y_max > typo_ascender:
                error_string = f"yMax ({y_max}) above typoAscender ({typo_ascender})"
                bad_flag = True
            elif y_min < typo_descender and y_max > typo_ascender:
                error_string = f"yMin ({y_min}) below typoDescender ({typo_descender}) and yMax ({y_max}) above typoAscender ({typo_ascender})"
                bad_flag = True

            if bad_flag is True:
                if uni_script not in bad_metrics_dict:
                    bad_metrics_dict[uni_script] = []

                severity = max(typo_descender - y_min, y_max - typo_ascender)

                bad_metrics_dict[uni_script].append(
                    {
                        "glyph_name": glyph_name,
                        "uni_name": uni_name,
                        "uni_codepoint": uni_codepoint,
                        "y_min": y_min,
                        "y_max": y_max,
                        "uni_block": uni_block,
                        "uni_category": uni_category,
                        "error_string": error_string,
                        "severity": severity,
                    }
                )

        else:
            error_list.append(
                f"Glyph '{glyph_name}' missing yMin and/or yMax value. (Script: {uni_script})"
            )

    # ~~~~~~~~~~~~~~~~~~
    #   Text Reporting
    # ~~~~~~~~~~~~~~~~~~

    # overall script results
    if len(bad_metrics_dict) > 0:
        sorted_scripts = sorted(bad_metrics_dict.keys())
        print(
            "Scripts with metrics that extend beyond OS/2 table global typo metrics values:"
        )
        for script in sorted_scripts:
            print(script)

        for script_name in sorted_scripts:
            print(f"\n\n{script_name}:")
            for bad_glyph in bad_metrics_dict[script_name]:
                print(
                    f"  {bad_glyph['glyph_name']} ({bad_glyph['uni_name']}, {bad_glyph['uni_codepoint']}, {bad_glyph['uni_block']}, Category: {bad_glyph['uni_category']}): {bad_glyph['error_string']}"
                )

    # testing errors
    print("\n\nTesting errors:")
    for error_string in error_list:
        print(error_string)

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
                    {script_sections}
                </body>
            </html>
        """

        Path(f"report_{font_path.stem}.html").write_text(template)


if __name__ == "__main__":
    for font_path in sys.argv[1:]:
        report_glyphs(Path(font_path))
