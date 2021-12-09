import copy

from pathlib import Path

import ufoLib2

GLYPH_NAMES = [
    "ta-khmer.below",
    "ta-khmer.below.ro",
    "ta-khmer.below2",
    "sso-khmer.post",
]

for p in [
    *Path("source/GoogleSans/staging/u").glob("*.ufo"),
    *Path("source/GoogleSans/staging/i").glob("*.ufo"),
]:
    print(p.name)

    u = ufoLib2.Font.open(p)
    for n in GLYPH_NAMES:
        g = u[n]
        if g.anchors:
            print("already anchored", n)
            continue
        if not g.components:
            print("no components?", n)
            continue
        b = u[g.components[0].baseGlyph]
        g.anchors = copy.deepcopy(b.anchors)
        for a in g.anchors:
            a.x += g.components[0].transformation.dx
    u.save()
