# Copyright 2024 Google Sans authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Change the color of a font with a COLRv0 table, for use in debugging."""

import re
from pathlib import Path

from fontTools.colorLib.builder import buildCOLR, buildCPAL
from fontTools.ttLib import TTFont

HEX_COLOR = re.compile("#" + "([0-9a-f]{2})" * 3, flags=re.IGNORECASE)

BUILD_DIR = Path(__file__).parent.parent / "build" / "GoogleSans" / "android"


def set_foreground(ttf: TTFont, color: tuple[float, float, float, float]) -> None:
    ttf["CPAL"] = buildCPAL([[color]])
    ttf["COLR"] = buildCOLR(
        {glyph: [(glyph, 0)] for glyph in ttf.getGlyphNames()}, version=0
    )


def get_color(hexa: str) -> tuple[float, float, float]:
    match = HEX_COLOR.fullmatch(hexa)
    if match is None:
        raise ValueError(
            "Hex color must be a '#' followed by six hexadecimal digits, "
            f"but was instead '{hexa}'"
        )
    r, g, b = match.groups()
    return (int(r, 16) / 255, int(g, 16) / 255, int(b, 16) / 255)


if __name__ == "__main__":
    from gs_unmerge_langs import SUBSETS

    assert BUILD_DIR.is_dir(), "build directory does not exist"

    COLOR_DIR = BUILD_DIR / "colored"
    COLOR_DIR.mkdir(exist_ok=True)

    for ttf_path in BUILD_DIR.glob("*.ttf"):
        print(f"Coloring {ttf_path.name}")
        (subset_color,) = (
            subset.color for subset in SUBSETS if subset.name in ttf_path.name
        )
        ttf = TTFont(ttf_path)
        set_foreground(ttf, (*subset_color, 1))
        ttf.save(COLOR_DIR / ttf_path.name)
