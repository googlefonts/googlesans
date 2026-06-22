#!/usr/bin/env -S uv run --script

# Copyright 2020 Google Sans Authors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# /// script
# dependencies = [
#     "fontspectorapi",
#     "fontTools",
# ]
# ///

from difflib import unified_diff
from pathlib import Path

from fontspectorapi import (
    FAIL,
    PASS,
    CheckStatuses,
    Plugin,
    check,
    plugin_main,
)
from fontTools.ttLib import TTFont

GLYPH_DEFS_DIR = Path("qa", "definitions")


@check(
    id="charset/glyphset-contents",
    title="Check charset matches list",
    rationale="""
    Confirms that the fonts include all expected Unicode encoded and non-Unicode
    encoded glyph definitions. This test does not require the glyph order to
    match.
    """,
    runs_on_collection=True,
)
def glyphset_contents(font_paths: list[Path]) -> CheckStatuses:
    for font_path in font_paths:
        if (
            font_path.parent.parent.name == "android"
            or font_path.parent.name == "figma"
        ):
            continue

        ttf = TTFont(font_path)

        glyph_def_name = font_path.name + ".glyphsetdef"
        glyph_def_path = GLYPH_DEFS_DIR / glyph_def_name

        # Sort to compare without considering order.
        expected_glyphs = sorted(glyph_def_path.read_text().strip().splitlines())
        actual_glyphs = sorted(ttf.getGlyphOrder())

        if expected_glyphs == actual_glyphs:
            yield PASS, "Font glyphset matches its expected glyphset"
        else:
            diff = "\n".join(
                unified_diff(
                    expected_glyphs,
                    actual_glyphs,
                    fromfile="glyphsetdef",
                    tofile="ttFont.getGlyphOrder()",
                    lineterm="",
                )
            )
            yield (
                FAIL,
                (
                    "Font glyphset does not match its expected glyphset. "
                    f"Diffs:\n\n```diff\n{diff}\n```"
                ),
            )


def register(plugin: Plugin) -> None:
    plugin.register_simple_profile(
        "gs-charset",
        (glyphset_contents,),
        section_name="Google Sans Custom Character Set Checks",
    )


if __name__ == "__main__":
    raise SystemExit(plugin_main(register, plugin_name="gs-charset"))
