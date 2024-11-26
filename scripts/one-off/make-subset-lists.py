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

We keep this script here instead of in the Pixel Fallback repo,
as it uses the sources present in googlesans repo and it needs the design names.
The output .txt files are needed in the Pixel Fallback repo:
https://github.com/googlefonts/pixel-brand-fallback-stack
"""

from __future__ import annotations

from pathlib import Path
import re

from ufoLib2 import Font
from fontTools import unicodedata
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
        # Script extension gives better results than just script but creates too
        # many lists, so we trim down the amount of lists to only the supported
        # scripts of Google Sans.
        unicodedata.script_extension,
        cmap,
        gsub,
    )

    # Basic scripts really supported by Google Sans
    scripts = set(unicodedata.script(chr(u)) for g in font for u in g.unicodes)
    for script in list(glyphs_by_script):
        if script not in scripts:
            del glyphs_by_script[script]

    # Fixup the data when we know more than the code point can tell
    pattern_to_scripts = {
        "Arab": {
            # There's only 1 Arabic glyph, move it to common.
            r".*": "Zyyy"
        },
        "Zinh": {
            # acute-deva and others with -deva in the name should be in the Deva
            # list
            r"-deva$": "Deva",
        },
        "Zyyy": {
            # Same in Zyyy
            r"-deva$": "Deva",
            # Zyyy glyphs with .loclXXXX suffix should move to that script's
            # list, e.g. colon.loclBENG should go to Beng.txt
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
        "Latn": {
            # All ending with '-georgian' needs to end up in Geor list only.
            # Their script extension is Latn + Geor so we remove from Latn
            r"-georgian": "Geor",
        },
        # Delete the locl[SOMETHING_ELSE] from each script's list
        "Beng": {r"\.locl(?!BENG)": None},
        "Deva": {r"\.locl(?!DEVA|MAR|NEP)": None},
        "Geor": {r"\.locl(?!GEO)": None},
        "Guru": {r"\.locl(?!GURM)": None},
        "Knda": {r"\.locl(?!KNDA)": None},
        "Mlym": {r"\.locl(?!MALM)": None},
        "Orya": {r"\.locl(?!ODIA)": None},
        "Sinh": {r"\.locl(?!SINH)": None},
        "Taml": {r"\.locl(?!TAML)": None},
        "Telu": {r"\.locl(?!TELU)": None},
        "Gujr": {r"\.locl": None},
    }
    for source, pattern_to_script in pattern_to_scripts.items():
        for pattern, script in pattern_to_script.items():
            script_glyphs = [
                g for g in glyphs_by_script[source] if re.search(pattern, g)
            ]
            if script is not None:
                glyphs_by_script[script].update(script_glyphs)
            glyphs_by_script[source].difference_update(script_glyphs)
            # Delete empty sets
            if not glyphs_by_script[source]:
                del glyphs_by_script[source]

    # Exceptions
    glyphs_to_add = {
        # We spotted /zerowidthjoiner is needed in Sinhala to make some conjuncts.
        # Should this be included in other scripts?
        "Sinh": ["zerowidthjoiner"],
        # Punctuation needed for some Thai ligatures.
        "Thai": ["quotedbl", "underscore"],
    }
    for script, glyphs in glyphs_to_add.items():
        glyphs_by_script[script].update(glyphs)

    # Sanity check: all glyphs with a code point should be in one list or the
    # other. Glyphs without code points might not be listed (e.g. components
    # used by other glyphs) and that's fine because they will automatically get
    # picked up by pyftsubset.
    unlisted = set(
        g.name for g in font if g.name is not None and g.unicode is not None
    ).difference(*list(glyphs_by_script.values()))
    assert not unlisted, f"Some glyphs were unlisted: {", ".join(sorted(unlisted))}"

    # Write out lists of code points. pyftsubset will do the GSUB closure too.
    TARGET_FOLDER.mkdir(parents=True, exist_ok=True)
    for script, glyphs in glyphs_by_script.items():
        lines = []
        for g in sorted(glyphs):
            lines.append(f"# {g}")
            for u in font[g].unicodes:
                lines.append(f"U+{u:04X}")
        path = TARGET_FOLDER / f"{script}.txt"
        path.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
