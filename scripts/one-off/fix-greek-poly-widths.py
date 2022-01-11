# Copyright 2021 Google Sans Authors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Match the width of Greek polytonic glyphs in other grades to the width in GRAD0.

See:
https://github.com/googlefonts/googlesans/issues/421
https://github.com/googlefonts/googlesans/pull/425
"""
from __future__ import annotations

# This script requires Python 3.9+ for graphlib
from graphlib import TopologicalSorter
from pathlib import Path
from textwrap import indent
from typing import Dict, FrozenSet, List

import ufoLib2

DEPENDENT_UFOS = {
    "GoogleSans-opsz17-wght380-GRAD0.ufo": [
        "GoogleSans-opsz17-wght380-GRAD-50.ufo",
        "GoogleSans-opsz17-wght380-GRAD200.ufo",
    ],
    "GoogleSans-opsz18-wght380-GRAD0.ufo": [
        "GoogleSans-opsz18-wght380-GRAD-50.ufo",
        "GoogleSans-opsz18-wght380-GRAD200.ufo",
    ],
    "GoogleSansItalic-opsz17-wght380-GRAD0.ufo": [
        "GoogleSansItalic-opsz17-wght380-GRAD-50.ufo",
        "GoogleSansItalic-opsz17-wght380-GRAD200.ufo",
    ],
    "GoogleSansItalic-opsz18-wght380-GRAD0.ufo": [
        "GoogleSansItalic-opsz18-wght380-GRAD-50.ufo",
        "GoogleSansItalic-opsz18-wght380-GRAD200.ufo",
    ],
}


def topo_sort(font: ufoLib2.Font) -> List[str]:
    # Build a cache of what glyphs are used as components where, to keep them
    # in place when moving the base.
    glyph_graph: Dict[str, FrozenSet[str]] = {}
    for g in font:
        if g.name is None:
            continue
        glyph_graph[g.name] = frozenset(c.baseGlyph for c in g.components)

    # Make sure outline glyphs are first in the list, then those that use these
    # outlines as components, then those that use these composite glyphs as
    # components etc. This ensures changing bearings does not change glyphs
    # we already processed.
    ts = TopologicalSorter(glyph_graph)
    return list(ts.static_order())


ROOT_DIR = Path(__file__).parent.parent.parent
SOURCE_DIR = ROOT_DIR / "source" / "GoogleSans"


def main():
    topo = None
    fixed_glyphs = set()
    not_fixed = set()

    for grad0, other_grades in DEPENDENT_UFOS.items():
        source_ufo_path = SOURCE_DIR / grad0
        source_ufo = ufoLib2.Font.open(source_ufo_path)

        if topo is None:
            # Same order for all UFOs because they're compatible so have the
            # same components
            topo = topo_sort(source_ufo)

        for other_grade in other_grades:
            target_ufo_path = SOURCE_DIR / other_grade
            target_ufo = ufoLib2.Font.open(target_ufo_path)

            for glyph_name in topo:
                try:
                    source_glyph = source_ufo[glyph_name]  # Width 800
                    target_glyph = target_ufo[glyph_name]  # Width 700
                except KeyError:
                    pass
                width_diff = source_glyph.width - target_glyph.width  # Diff 100
                if width_diff:
                    if any(
                        part in glyph_name for part in ("loclARM", "-arm", "baht.tf")
                    ):
                        not_fixed.add(glyph_name)
                        continue
                    # Apply the source width to the LSB of the target glyph
                    target_lsb = target_glyph.getLeftMargin(target_ufo)  # LSB 50
                    if target_lsb is not None:
                        target_glyph.setLeftMargin(
                            target_lsb + width_diff, target_ufo
                        )  # New LSB 150
                    else:
                        target_glyph.width += width_diff
                    fixed_glyphs.add(glyph_name)
                assert source_glyph.width == target_glyph.width
            target_ufo.save()

        print()
        print(f"{str(grad0)} - fixed glyphs:")
        print(indent("\n".join(sorted(fixed_glyphs)), "    "))
        print(f"{str(grad0)} - NOT fixed glyphs:")
        print(indent("\n".join(sorted(not_fixed)), "    "))


if __name__ == "__main__":
    main()
