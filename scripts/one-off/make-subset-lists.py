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
import re

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

    # Start from a mechanical sorting based on GSUB closure
    cmap = makeUnicodeToGlyphNameMapping(font, glyph_order)
    feature_file = parseLayoutFeatures(font)
    gsub = compileGSUB(feature_file, glyph_order)
    glyphs_by_script: dict[str, set[str]] = classifyGlyphs(
        unicodedata_script, cmap, gsub
    )

    # Fixup the data when we know more than the code point can tell
    pattern_to_scripts = {
        "Zinh": {
            # acute-deva and others with -deva in the name should be in the Deva list
            r"-deva$": "Deva",
        },
        "Zyyy": {
            # Same in Zyyy
            r"-deva$": "Deva",
            # Zyyy glyphs with .loclXXXX suffix should move to that script's list, e.g.
            # colon.loclBENG should go to Beng.txt
            r"\.loclBENG": "Beng",
            r"\.loclDEVA": "Deva",
            r"\.loclGEO": "Geor",
            r"\.loclGURM": "Guru",
            r"\.loclKNDA": "Knda",
            r"\.loclMALM": "Mlym",
            r"\.loclODIA": "Orya",
            r"\.loclSINH": "Sinh",
            r"\.loclTAML": "Taml",
            r"\.loclTELU": "Telu",
        },
    }
    for source, pattern_to_script in pattern_to_scripts.items():
        for pattern, script in pattern_to_script.items():
            script_glyphs = [
                g for g in glyphs_by_script[source] if re.search(pattern, g)
            ]
            glyphs_by_script[script].update(script_glyphs)
            glyphs_by_script[source].difference_update(script_glyphs)

    TARGET_FOLDER.mkdir(parents=True, exist_ok=True)
    for script, glyphs in glyphs_by_script.items():
        path = TARGET_FOLDER / f"{script}.txt"
        path.write_text("\n".join(sorted(glyphs)) + "\n")


if __name__ == "__main__":
    main()
