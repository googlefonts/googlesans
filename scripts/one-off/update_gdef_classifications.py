from pathlib import Path
from typing import Literal

from ufoLib2 import Font

type GlyphsGlyphCategory = Literal[
    "Letter", "Mark", "Number", "Punctuation", "Symbol", "Separator", "Space", "Other"
]


UFO_PATHS = sorted(Path("source/GoogleSans").glob("*.ufo"))

# The data to update!
# Fontspector gives postscript names, so that's the key.
# The normalisation script we use takes overrides from the glyph lib key
# specific to Glyphs.app (com.schriftgestaltung.Glyphs.category), so I've mapped
# base -> Letter and mark -> Mark. These are the values
UPDATA: dict[str, GlyphsGlyphCategory] = {
    # https://github.com/googlefonts/googlesans/issues/739#issuecomment-4783812706
    "oeSignkhmer": "Letter",
    "uni0C41": "Letter",
    "uni0C42": "Letter",
    "uni0C43": "Letter",
    "uni0C44": "Letter",
    "uni0B48": "Letter",
    "uni0B4B": "Letter",
    "uni0B4C": "Letter",
    "uni0CBE": "Letter",
    "uni0CC0": "Letter",
    "uni0CC1": "Letter",
    "uni0CC2": "Letter",
    "uni0CC3": "Letter",
    "uni0CC4": "Letter",
    "uni0CC7": "Letter",
    "uni0CC8": "Letter",
    "uni0CCA": "Letter",
    "uni0CCB": "Letter",
    "uni0C82": "Letter",
    "uni0C83": "Letter",
    "uni0C3E": "Mark",
    "uni0C4A": "Mark",
    "uni0C4B": "Mark",
    "uni0C4C": "Mark",
    "uni0CCD": "Mark",
    "uni0CCC": "Mark",
}

for ufo_path in UFO_PATHS:
    print(f"updating {ufo_path.name}")
    ufo = Font.open(ufo_path)
    reverse_ps_names: dict[str, str] = {
        ps_name: glyph_name
        for (glyph_name, ps_name) in ufo.lib["public.postscriptNames"].items()
    }

    for ps_name, glyphs_category in UPDATA.items():
        glyph_name = reverse_ps_names.get(ps_name, ps_name)
        glyph = ufo[glyph_name]
        current = glyph.lib.get("com.schriftgestaltung.Glyphs.category")
        if current != glyphs_category:
            print(f"fixed /{glyph_name} ({ps_name})")
            glyph.lib["com.schriftgestaltung.Glyphs.category"] = glyphs_category
        else:
            print(f"skipping /{glyph_name} ({ps_name}): already {glyphs_category}")

    ufo.save(ufo_path, overwrite=True)
    print()
print("now run scripts/gs-normalize-designspace.py")
