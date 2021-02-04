import ufoLib2
import ufoLib2.objects
from fontTools.designspaceLib import DesignSpaceDocument

affected_glyphs = [
    "Gcommaaccent.alt",
    "Kcommaaccent.alt",
    "Rcommaaccent.alt",
    "g.sc",
    "g.sc.ss04",
    "kcommaaccent.alt",
    "rcommaaccent.alt",
    "tcommaaccent.alt",
    "apostrophe-arm.case",
    "apostrophe-arm.sc",
    "ca-arm.sc",
    "eh-arm.sc",
    "gim-arm.sc",
    "jheh-arm.sc",
    "semicolon.loclARM",
    "za-arm.sc",
    # Innocent caught-up bystanders below
    "tcedilla"
]


for p in (
    "source/GoogleSans/GoogleSans.designspace",
    "source/GoogleSans/GoogleSans-Italic.designspace",
):
    d = DesignSpaceDocument.fromfile(p)
    d.loadSourceFonts(ufoLib2.Font.open)
    for s in d.sources:
        for name in affected_glyphs:
            name_base = name.split(".")[0]
            name_new = f"{name_base}.rvrn"
            if name_new in s.font:
                continue
            g = s.font.newGlyph(name_new)
            g.components.append(ufoLib2.objects.Component(name_base))
            g.width = s.font[name_base].width
        s.font.save()
