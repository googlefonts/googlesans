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


from pathlib import Path
from typing import cast

from fontspectorapi import (
    FAIL,
    PASS,
    SKIP,
    WARN,
    CheckStatuses,
    Message,
    Plugin,
    check,
    plugin_main,
)
from fontspectorapi.utils import (
    UNICODERANGE_DATA,
    chars_in_range,
    compute_unicoderange_bits,
    unicoderange,
    unicoderange_bit_name,
)
from fontTools.ttLib import TTFont

FVAR_DEFAULTS = {
    "opsz": 18.0,
    "wght": 400.0,
    "GRAD": 0.0,
}


# ================================================
#
# Begin check definitions
#
# ================================================


# ================================================
# OpenType table attribute checks
# ================================================


@check(
    id="googlesans/os2/fsselectionbit7",
    title="Use typo metrics",
    rationale="""
    Confirms that fonts have OS/2.fsSelection bit 7 (USE_TYPO_METRICS) set \
    for typo vertical metrics (instead of win vertical metrics)
    """,
    runs_on_collection=True,
)
def opentype_os2_fsselectionbit7(font_paths: list[Path]) -> CheckStatuses:
    found_fail = False
    fail_list = []
    for font_path in font_paths:
        ttf = TTFont(font_path)
        fsselection_int = cast(int, ttf["OS/2"].fsSelection)  # type: ignore
        fsselection_bit_is_set_test = (fsselection_int & (1 << 7)) != 0
        if not fsselection_bit_is_set_test:
            found_fail = True
            fail_list.append(font_path)

    if found_fail:
        yield (
            FAIL,
            f"The OS/2.fsSelection bit 7 (USE_TYPO_METRICS) was NOT set "
            f"in the following fonts: {' '.join(fail_list)}.",
        )
    else:
        yield (
            PASS,
            "The OS/2.fsSelection bit 7 (USE_TYPO_METRICS) was set in all fonts.",
        )


@check(
    id="googlesans/opentype/BASE",
    title="Font has BASE table",
    rationale="Checks that the font has a BASE table",
)
def has_base_table(font_path: Path) -> CheckStatuses:
    ttf = TTFont(font_path)

    if "BASE" in ttf:
        yield PASS, "BASE table present in font"
    else:
        yield FAIL, "Missing BASE table"


# ::::::::::::::::::::::::::::::::::::::::::::::::
# Other metrics
# ::::::::::::::::::::::::::::::::::::::::::::::::


@check(
    id="googlesans/opentype/os2/unicode_range_bits",
    title="Ensure UnicodeRange bits are properly set",
    rationale="""
        When the UnicodeRange bits on the OS/2 table are not properly set, some programs
        running on Windows may not recognize the font and use a system fallback font
        instead. For that reason, this check calculates the proper settings by inspecting
        the glyphs declared on the cmap table and then ensures that their corresponding
        ranges are enabled.
    """,
)
def unicode_range_bits(font_path: Path) -> CheckStatuses:
    ttf = TTFont(font_path)
    unicode_range = unicoderange(ttf)
    expected_unicoderange = compute_unicoderange_bits(ttf)
    difference = unicode_range ^ expected_unicoderange
    if not difference:
        yield PASS, "Unicode range bits are properly set"
    else:
        for bit in range(128):
            if difference & (1 << bit):
                range_name = unicoderange_bit_name(bit)
                num_chars = len(chars_in_range(ttf, bit))
                range_size = sum(
                    entry[3] - entry[2] + 1 for entry in UNICODERANGE_DATA[bit]
                )
                if num_chars == 0:
                    status = FAIL
                    set_unset = "0"
                    num_chars = "none"
                else:
                    status = WARN
                    set_unset = "1"
                yield (
                    status,
                    Message(
                        "bad-range-bit",
                        f"UnicodeRange bit {bit} '{range_name}' should be {set_unset} "
                        f"because cmap has {num_chars} of the {range_size} codepoints "
                        f"in this range.",
                    ),
                )


# ================================================
# Variable build format specific
# ================================================


@check(
    id="googlesans/vf/fvaraxes",
    title="Ensure all expected axes are present",
    rationale="""
    Confirms that the variable font format builds include
    all expected axis tags
    """,
)
def variable_fvar_axes(font_path: Path) -> CheckStatuses:
    ttf = TTFont(font_path)

    if "fvar" not in ttf:
        yield SKIP, "Not a VF"
        return

    observed_axis_list = []
    for axis in ttf["fvar"].axes:  # type: ignore
        observed_axis_list.append(axis.axisTag)

    if len(observed_axis_list) != len(FVAR_DEFAULTS):
        yield (
            FAIL,
            f"{font_path.name} does not include the correct axis tags. \n"
            f"Observed: {observed_axis_list}\n"
            f"Expected: {FVAR_DEFAULTS.keys()}",
        )

    has_all_tags = True
    for axis_tag in FVAR_DEFAULTS.keys():
        if axis_tag not in observed_axis_list:
            has_all_tags = False
            yield FAIL, f"{font_path.name} does not include axis tag {axis_tag}"

    if has_all_tags:
        yield PASS, f"{font_path.name} includes all expected axis tags"


@check(
    id="googlesans/vf/fvardefault",
    title="Ensure correct axis defaults",
    rationale="""
    Confirms that the variable font format builds include the expected fvar
    default definitions for the Google Sans design axes
    """,
)
def variable_fvar_default(font_path: Path) -> CheckStatuses:
    ttf = TTFont(font_path)

    if "fvar" not in ttf:
        yield SKIP, "Not a VF"
        return

    for axis in ttf["fvar"].axes:  # type: ignore
        tag = axis.axisTag
        if tag not in FVAR_DEFAULTS:
            continue
        if axis.defaultValue != FVAR_DEFAULTS[tag]:
            yield (
                FAIL,
                f"{font_path.name} does not include the correct "
                f"fvar {tag} axis default.\n"
                f"Found: `{axis.defaultValue}` and expected `{FVAR_DEFAULTS[tag]}`",
            )
        else:
            yield (
                PASS,
                f"{font_path.name} contains the expected fvar {tag} default.",
            )


# ================================================
#
# End check definitions
#
# ================================================


def register(plugin: Plugin) -> None:
    CHECKS = (
        opentype_os2_fsselectionbit7,
        has_base_table,
        unicode_range_bits,
        variable_fvar_axes,
        variable_fvar_default,
    )
    plugin.register_simple_profile(
        "gs-custom", CHECKS, section_name="Google Sans Custom Checks"
    )


if __name__ == "__main__":
    raise SystemExit(plugin_main(register, plugin_name="gs-custom"))
