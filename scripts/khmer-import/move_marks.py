import collections
from pathlib import Path

import ufoLib2

MARKS = [
    "ka-khmer.below",
    "kha-khmer.below",
    "ko-khmer.below",
    "ngo-khmer.below",
    "ca-khmer.below",
    "cha-khmer.below",
    "co-khmer.below",
    "nyo-khmer.below",
    "nyo-khmer.full.below",
    "da-khmer.below",
    "ttha-khmer.below",
    "do-khmer.below",
    "nno-khmer.below",
    "ta-khmer.below",
    "tha-khmer.below",
    "to-khmer.below",
    "tho-khmer.below",
    "no-khmer.below",
    "pha-khmer.below",
    "po-khmer.below",
    "pho-khmer.below",
    "mo-khmer.below",
    "lo-khmer.below",
    "vo-khmer.below",
    "sha-khmer.below",
    "ha-khmer.below",
    "qa-khmer.below",
    "qi-khmer.below",
    "qu-khmer.below",
    "quu-khmer.below",
    "ry-khmer.below",
    "ly-khmer.below",
    "qe-khmer.below",
    "qoo-khmer.below",
    "ka-khmer.below2",
    "kha-khmer.below2",
    "ko-khmer.below2",
    "ngo-khmer.below2",
    "ca-khmer.below2",
    "cha-khmer.below2",
    "co-khmer.below2",
    "nyo-khmer.below2",
    "da-khmer.below2",
    "ttha-khmer.below2",
    "do-khmer.below2",
    "nno-khmer.below2",
    "ta-khmer.below2",
    "tha-khmer.below2",
    "to-khmer.below2",
    "tho-khmer.below2",
    "no-khmer.below2",
    "pha-khmer.below2",
    "po-khmer.below2",
    "pho-khmer.below2",
    "mo-khmer.below2",
    "lo-khmer.below2",
    "vo-khmer.below2",
    "sha-khmer.below2",
    "ha-khmer.below2",
    "qa-khmer.below2",
    "iMark-khmer",
    "iiMark-khmer",
    "yMark-khmer",
    "yyMark-khmer",
    "iMark_toandakhiat-khmer",
    "iMark-khmer.narrow",
    "iiMark-khmer.narrow",
    "yMark-khmer.narrow",
    "yyMark-khmer.narrow",
    "iMark_toandakhiat-khmer.narrow",
    "uMark-khmer",
    "uuMark-khmer",
    "uaMark-khmer",
    "uMark-khmer.below2",
    "uuMark-khmer.below2",
    "uaMark-khmer.below2",
    "oeSign-khmer",
    "nikahit-khmer",
    "muusikatoan-khmer",
    "triisap-khmer",
    "bantoc-khmer",
    "robat-khmer",
    "toandakhiat-khmer",
    "kakabat-khmer",
    "ahsda-khmer",
    "samyoksannya-khmer",
    "viriam-khmer",
    "coeng-khmer",
    "bathamasat-khmer",
    "atthacan-khmer",
    "ahsda-khmer.narrow",
    "toandakhiat-khmer.narrow",
    "samyoksannya-khmer.narrow",
    "nyo-khmer.full.below.narrow",
    "nno-khmer.below.narrow1",
    "nno-khmer.below.narrow2",
    "da-khmer.below.ro",
    "ta-khmer.below.ro",
    "po-khmer.below.ro",
    "pho-khmer.below.ro",
    "mo-khmer.below.ro",
    "uuMark-khmer.ro",
    "uaMark-khmer.ro",
    "muusikatoan-khmer.ro",
    "muusikatoan-khmer.roLiga",
    "nikahit-khmer.small",
    "kakabat-khmer.small",
    "samyoksannya-khmer.small",
]


def move_marks(composite_graph, ufo_path):
    print(ufo_path.name)

    ufo = ufoLib2.Font.open(ufo_path)
    for name in MARKS:
        glyph = ufo[name]
        ow = glyph.lib.get("com.schriftgestaltung.Glyphs.originalWidth")
        if ow is None:
            if glyph.width:
                ow = glyph.width
            else:
                print("no orig width:", name)
                continue
        glyph.move((-ow, 0))

        # If the glyph is used as a component in any other glyph, move that component
        # in the opposite direction (measured to the left, to the origin) to ensure
        # that existing components stay as before.
        if glyph.name in composite_graph:
            left_diff = ow
            if isinstance(left_diff, float) and left_diff.is_integer():
                left_diff = round(left_diff)
            if not ow:
                continue
            for composite_name in composite_graph[glyph.name]:
                composite = ufo[composite_name]
                for c in composite.components:
                    if c.baseGlyph != glyph.name:
                        continue
                    c.transformation = c.transformation.translate(left_diff, 0)
    ufo.save()


def scan_composites(ufo):
    """Note down which glyphs are used as components in which other glyphs.

    Moving them for spacing needs counter-moving them where they are used as
    components to have them stay put.
    """
    composite_graph = collections.defaultdict(set)
    for glyph in ufo:
        if glyph.name is None:
            continue
        for c in glyph.components:
            composite_graph[c.baseGlyph].add(glyph.name)
    return composite_graph


ufo_reference_upright = ufoLib2.Font.open(
    "source/GoogleSans/staging/u/GoogleSansKHLooped-TextRegular.ufo"
)
composite_graph = scan_composites(ufo_reference_upright)
for ufo_path in Path("source/GoogleSans/staging/u").glob("*.ufo"):
    move_marks(composite_graph, ufo_path)


ufo_reference_italic = ufoLib2.Font.open(
    "source/GoogleSans/staging/i/GoogleSansKHLooped-TextRegularItalic.ufo"
)
composite_graph = scan_composites(ufo_reference_italic)
for ufo_path in Path("source/GoogleSans/staging/i").glob("*.ufo"):
    move_marks(composite_graph, ufo_path)
