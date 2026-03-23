from __future__ import annotations

from ufoLib2 import Font
from ufoLib2.objects import Layer
from fontTools.designspaceLib import DesignSpaceDocument
from pathlib import Path

SKIP = {
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "zero.tf",
    "one.tf",
    "two.tf",
    "three.tf",
    "four.tf",
    "five.tf",
    "six.tf",
    "seven.tf",
    "eight.tf",
    "nine.tf",
    "space",
    "thinspace",
    "hairspace",
    "mark-ar",
    "parenleft",
    "parenright",
    "percentbar",
    "question",
    "radical",
    "slash",
    "dottedCircle",
}


def dependencies(name: str, layer: Layer) -> set[str]:
    return {name} | set(
        dependency
        for component in layer[name].components
        for dependency in dependencies(component.baseGlyph, layer)
    )


ds_from = DesignSpaceDocument.fromfile(
    Path("..", "googlesans-arabic", "masters", "GoogleSansArabic.designspace")
)
ds_from.loadSourceFonts(Font.open)

found = set()
for source in ds_from.sources:
    assert isinstance(source.font, Font)
    assert source.layerName is None

    for name in source.font.keys():
        if dependencies(name, source.font.layers.defaultLayer) & SKIP:
            found.add(name)

default = ds_from.findDefault().font
assert isinstance(default, Font)

for glyph in sorted(found):
    print(
        glyph,
        *(f"(U+{codepoint:04X})" for codepoint in default[glyph].unicodes),
    )
