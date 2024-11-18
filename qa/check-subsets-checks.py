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
from typing import Literal

from fontbakery.callable import check, condition
from fontbakery.status import ERROR, FAIL, PASS
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
            "Subsets have the same codepoint coverage as the full font "
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
            "Subsets have different codepoint coverage than the full font "
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


@check(id="android_subsets/coverage/language_systems")
def check_coverage_langsys(ttFont: TTFont, subsets: dict[Path, TTFont], font: Font):
    """
    Check that language system coverage in the subsets matches the full font.
    """

    shaping_tags: tuple[ShapingTag, ...] = ("GPOS", "GSUB")
    for table in shaping_tags:
        in_full = get_langsys(ttFont, table)

        if in_full is None:
            yield (ERROR, f"Full font is does not have a {table} table")
            return

        in_subsets = {
            system
            for subset in subsets.values()
            if (lang_sys := get_langsys(subset, table)) is not None
            for system in lang_sys
        }

        if in_full == in_subsets:
            yield (
                PASS,
                f"Subsets have the same {table} language system coverage as "
                f"the full font `{font.file_displayname}`",
            )
        else:
            yield (
                FAIL,
                f"Subsets have different {table} language system coverage than "
                f"the full font {font.file_displayname}:\n\n```diff\n"
                + "\n".join(
                    difflib.unified_diff(
                        sorted(str(langsys) for langsys in in_full),
                        sorted(str(langsys) for langsys in in_subsets),
                        fromfile="Full Font",
                        tofile="Subsets",
                        lineterm="",
                    )
                )
                + "\n```",
            )


type ShapingTag = Literal["GPOS", "GSUB"]


def get_langsys(ttf: TTFont, table: ShapingTag) -> set[tuple[str, str]] | None:
    shaping = ttf.get(table)

    if shaping is None:
        return None

    return {
        (script_rec.ScriptTag, lang_tag)
        for script_rec in shaping.table.ScriptList.ScriptRecord  # type: ignore
        for lang_tag in [
            *(["dflt"] if script_rec.Script.DefaultLangSys else []),
            *(lang_rec.LangSysTag for lang_rec in script_rec.Script.LangSysRecord),
        ]
    }


@check(id="android_subsets/coverage/feature_tags")
def check_coverage_feature_tags(
    ttFont: TTFont, subsets: dict[Path, TTFont], font: Font
):
    """
    Check that feature tag coverage in the subsets matches the full font.

    NOTE: This does not check the content or quantity of features, only the
          presence of the same _types_ of feature before and after subsetting.
    """

    shaping_tags: tuple[ShapingTag, ...] = ("GPOS", "GSUB")
    for table in shaping_tags:
        in_full = {
            fea_rec.FeatureTag
            for fea_rec in ttFont[table].table.FeatureList.FeatureRecord
        }

        in_subsets = {
            fea_rec.FeatureTag
            for subset in subsets.values()
            for fea_rec in subset[table].table.FeatureList.FeatureRecord
        }

        if in_full == in_subsets:
            yield (
                PASS,
                f"Subsets have the same {table} feature tag coverage as "
                f"the full font `{font.file_displayname}`",
            )
        else:
            yield (
                FAIL,
                f"Subsets have different {table} feature tag coverage than "
                f"the full font {font.file_displayname}:\n\n```diff\n"
                + "\n".join(
                    difflib.unified_diff(
                        sorted(in_full),
                        sorted(in_subsets),
                        fromfile="Full Font",
                        tofile="Subsets",
                        lineterm="",
                    )
                )
                + "\n```",
            )
