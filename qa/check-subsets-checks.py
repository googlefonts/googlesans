# Copyright 2024 Google Sans authors
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

"""
Checks for comparing the coverage of subsets with their full originating font.
"""

import difflib
import unicodedata
from pathlib import Path

from fontbakery.callable import check, condition
from fontbakery.status import FAIL, PASS
from fontbakery.testable import Font
from fontTools.ttLib import TTFont

SUBSET_DIR = Path("build", "GoogleSans", "android")


@condition(Font)
def subsets(font: Font) -> dict[Path, TTFont]:
    subset_prefix = Path(font.file).stem

    subsets = [
        ttf for ttf in SUBSET_DIR.glob("*.ttf") if ttf.stem.startswith(subset_prefix)
    ]
    assert subsets, f"Could not find subsets for '{font.file}'"

    return {path: TTFont(path) for path in subsets}


@check(id="android_subsets/coverage/codepoints")
def check_coverage_codepoints(ttFont: TTFont, subsets: dict[Path, TTFont], font: Font):
    """Check that codepoint coverage in the subsets matches the full font."""

    in_full = set(ttFont.getBestCmap())
    in_subsets = {
        codepoint
        for subset in subsets.values()
        if (cmap := subset.getBestCmap()) is not None
        for codepoint in cmap
    }

    if in_full == in_subsets:
        yield (
            PASS,
            "Subsets have the same codepoint coverage as the full font",
            f"`{font.file_displayname}`",
        )
    else:

        def format_cmap(codepoints):
            summaries: list[str] = []

            for codepoint in sorted(codepoints):
                try:
                    name = unicodedata.name(chr(codepoint))
                except ValueError:
                    name = "???"
                summaries.append(f"U+{codepoint:04x} {name}")

            return summaries

        yield (
            FAIL,
            "Subsets have different codepoint coverage than the full font",
            f"{font.file_displayname}:\n\n```diff\n"
            + "\n".join(
                difflib.unified_diff(
                    format_cmap(in_full),
                    format_cmap(in_subsets),
                    fromfile="Full Font",
                    tofile="Subsets",
                    lineterm="",
                )
            )
            + "\n```",
        )
