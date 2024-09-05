# Copyright 2024 Google Sans Project Authors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path

from fontTools.misc.transform import Identity
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._h_e_a_d import table__h_e_a_d as Head
from fontTools.ttLib.tables.O_S_2f_2 import table_O_S_2f_2 as OS2


def draw_with_metrics(ttf: TTFont, glyph_name: str) -> str:
    """Draw a glyph from a TTF as an SVG, including reference lines for common
    vertical metrics."""

    # Draw metric lines
    os2: OS2 = ttf["OS/2"]  # type: ignore
    head: Head = ttf["head"]  # type: ignore

    lines: dict[str, list[int]] = {
        "red": [os2.sTypoAscender, os2.sTypoDescender],
        "blue": [os2.usWinAscent, -os2.usWinDescent],
        "green": [head.yMax, head.yMin],
    }

    highest = max(value for values in lines.values() for value in values) + 10
    lowest = min(value for values in lines.values() for value in values) - 10

    # Draw glyph to SVG
    glyph_set = ttf.getGlyphSet()
    glyph = glyph_set[glyph_name]

    bounds = BoundsPen(glyph_set)
    glyph.draw(bounds)
    assert bounds.bounds is not None
    (x_min, _, x_max, _) = bounds.bounds

    svg_pen = SVGPathPen(glyph_set)
    transform_pen = TransformPen(svg_pen, Identity.translate(y=highest).scale(y=-1))
    glyph.draw(transform_pen)

    # Construct SVG
    line_elements = "\n".join(
        f'<line x1="{x_min}" x2="{x_max}" y1="{highest - height}" y2="{highest - height}" stroke="{colour}" stroke-width="10" />'
        for colour, heights in lines.items()
        for height in heights
    )

    return f"""
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="{x_min} 0 {x_max - x_min} {highest - lowest}" preserveAspectRatio="meet">
            <g>
                <path d="{svg_pen.getCommands()}" />
            </g>
            {line_elements}
        </svg>
    """


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("ttf", type=TTFont)
    parser.add_argument("svg", type=Path)
    args = parser.parse_args()

    args.svg.write_text(draw_with_metrics(args.ttf, "A"))
