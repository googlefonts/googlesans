# Copyright 2021 Google Sans Authors
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
