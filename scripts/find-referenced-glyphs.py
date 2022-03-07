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

"""Print glyphs in the glyph import list plus all glyphs they reference."""

import argparse
from typing import Set
from pathlib import Path

from ufoLib2.objects import Font, Glyph

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("ufo", type=Font.open, help="Path to UFO.")
parser.add_argument("import_glyphs_file", type=Path)
parsed_args = parser.parse_args()
ufo: Font = parsed_args.ufo
glyph_list: Set[str] = {
    name.strip()
    for name in parsed_args.import_glyphs_file.read_text().split("\n")
    if name
}


def referenced_as_components(ufo: Font, glyph_list: Set[str]) -> Set[str]:
    """Return set of glyph names of glyphs used as components by glyphs in
    reachable_glyphs."""

    def _recurse(glyph: Glyph, seen: Set[str]) -> None:
        for component in glyph.components:
            seen.add(component.baseGlyph)
            _recurse(ufo[component.baseGlyph], seen)

    referenced_components = set()
    for name in glyph_list:
        glyph = ufo[name]
        _recurse(glyph, referenced_components)

    return referenced_components


reachable_glyph_names = referenced_as_components(ufo, glyph_list)

print("\n".join(sorted(glyph_list.union(reachable_glyph_names))))
