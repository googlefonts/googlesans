# Copyright 2022 Google Sans Authors
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

"""Compute per-script subset lists to prepare an Android subset without Telugu,
Odia, and Kannada.

https://github.com/googlefonts/googlesans/issues/646

How to run:

python scripts/one-off/make-subset-lists.py
"""

from __future__ import annotations

from pathlib import Path

from ufoLib2 import Font
from fontTools.unicodedata import script as unicodedata_script
from ufo2ft.featureCompiler import parseLayoutFeatures
from ufo2ft.util import (
    classifyGlyphs,
    makeOfficialGlyphOrder,
    compileGSUB,
    makeUnicodeToGlyphNameMapping,
)

TARGET_FOLDER = Path("source/GoogleSans/subsets")


def main():
    font = Font.open("source/GoogleSans/GoogleSans-opsz18-wght380-GRAD0.ufo")
    glyph_order = makeOfficialGlyphOrder(font)
    cmap = makeUnicodeToGlyphNameMapping(font, glyph_order)
    feature_file = parseLayoutFeatures(font)
    gsub = compileGSUB(feature_file, glyph_order)
    glyphs_by_script: dict[str, set[str]] = classifyGlyphs(
        unicodedata_script, cmap, gsub
    )

    TARGET_FOLDER.mkdir(parents=True, exist_ok=True)
    for script, glyphs in glyphs_by_script.items():
        path = TARGET_FOLDER / f"{script}.txt"
        path.write_text("\n".join(sorted(glyphs)))


if __name__ == "__main__":
    main()
