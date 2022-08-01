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

"""Print glyphs without Unicode value and which are unreachable via feature
substitutions and are not used as components."""

from __future__ import annotations

import argparse
from typing import Sequence, Set

import ufoLib2

from .internal.reachable_glyphs import reachable_glyphs, referenced_as_components


def main(args: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ufo", type=ufoLib2.Font.open, help="Path to UFO.")
    parser.add_argument(
        "--ignore-skipped",
        action="store_true",
        help="Skip printing glyphs skipped on export.",
    )
    parsed_args = parser.parse_args(args)
    ufo: ufoLib2.Font = parsed_args.ufo

    reachable_glyph_names = reachable_glyphs(ufo)
    reachable_glyph_names.update(referenced_as_components(ufo, reachable_glyph_names))
    skip_export_glyphs: Set[str] = set(ufo.lib.get("public.skipExportGlyphs", []))

    for glyph_name in ufo.keys():
        if parsed_args.ignore_skipped and glyph_name in skip_export_glyphs:
            continue
        if glyph_name not in reachable_glyph_names:
            print(glyph_name)


if __name__ == "__main__":
    main()
