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

from __future__ import annotations

import argparse

from ufoLib2 import Font


def main(args: list[str] | None = None):
    parser = argparse.ArgumentParser()
    parser.add_argument("fonts", nargs="+", type=Font.open, help="Fonts to recalc in-place.")
    parsed_args = parser.parse_args(args)

    ascent = 0
    descent = 0

    font: Font
    for font in parsed_args.fonts:
        skip_glyphs = set(font.lib.get("public.skipExportGlyphs", []))
        ascent = max(ascent, font.info.openTypeOS2WinAscent)
        descent = min(descent, -font.info.openTypeOS2WinDescent)
        for glyph in font:
            if glyph.name in skip_glyphs:
                continue
            bounds = glyph.getBounds(font)
            if bounds is None:
                continue
            ascent = max(ascent, bounds.yMax)
            descent = min(descent, bounds.yMin)

    assert ascent != 0 and descent != 0
    for font in parsed_args.fonts:
        font.info.openTypeOS2WinAscent = ascent + 1
        font.info.openTypeOS2WinDescent = abs(descent) + 1
        font.save()


if __name__ == "__main__":
    main()
