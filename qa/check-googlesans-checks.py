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


from fontbakery.prelude import check, FAIL, PASS, WARN
from fontbakery.constants import UNICODERANGE_DATA
from fontbakery.message import Message
from fontbakery.utils import (
    chars_in_range,
    compute_unicoderange_bits,
    unicoderange_bit_name,
)


# ================================================
#
# Conditions
#
# ================================================


# removed custom conditions that duplicated upstream fontbakery
# condition names


# ================================================
#
# Example test implementation
#
# ================================================


# # Test failure template
# @check(
#     id="com.google.fonts/check/googlesans/testfail",
#     rationale="""
#         This is a test failure rationale.
#     """,
# )
# def com_google_fonts_check_googlesans_test_fail():
#     """A test failure example."""
#     yield FAIL, "test failure message"


# # Test pass template
# @check(
#     id="com.google.fonts/check/googlesans/testpass",
#     rationale="""
#         This is a test pass rationale.
#     """,
# )
# def com_google_fonts_check_googlesans_test_pass():
#     """A test pass example."""
#     yield PASS, "test pass message"

# ================================================
#
# Begin check definitions
#
# ================================================


# ================================================
# OpenType table attribute checks
# ================================================

# ::::::::::::::::::::::::::::::::::::::::::::::::
# Vertical metrics
# ::::::::::::::::::::::::::::::::::::::::::::::::


# OS/2.fsSelection bit 7 (USE_TYPO_METRICS) is set in all fonts
@check(
    id="com.google.fonts/check/googlesans/opentype/os2/fsselectionbit7",
    rationale="""
    Confirms that fonts have OS/2.fsSelection bit 7 (USE_TYPO_METRICS) set \
    for typo vertical metrics (instead of win vertical metrics)
    """,
)
def com_google_fonts_check_googlesans_opentype_os2_fsselectionbit7(ttFonts, config):
    """OS/2.fsSelection bit 7 (USE_TYPO_METRICS) is set in all fonts"""
    check_config = config[
        "com.google.fonts/check/googlesans/opentype/os2/fsselectionbit7"
    ]
    os2_fsselection_bit7_isset = check_config["os2_fsselection_bit7"] == 1

    found_fail = False
    fail_list = []
    for tt in ttFonts:
        fsselection_int = tt["OS/2"].fsSelection
        fsselection_bit_is_set_test = (fsselection_int & (1 << 7)) != 0
        if fsselection_bit_is_set_test is os2_fsselection_bit7_isset:
            pass
        else:
            found_fail = True
            fail_list.append(tt.reader.file.name)

    if found_fail:
        yield (
            FAIL,
            f"The OS/2.fsSelection bit 7 (USE_TYPO_METRICS) was NOT set "
            f"in the following fonts: {fail_list}.",
        )
    else:
        yield PASS, "The OS/2.fsSelection bit 7 (USE_TYPO_METRICS) was set in all fonts."


# Note: winAscent and winDescent bounds are defined above yMin and below yMax values
# OS/2.winAscent check
@check(
    id="com.google.fonts/check/googlesans/opentype/os2/winascent",
    rationale="""
    Confirms that the OS/2.winAscent value is defined above the yMax
    value across the full glyph repertoire.
    """,
)
def com_google_fonts_check_googlesans_opentype_os2_winascent(ttFont):
    """OS/2.winAscent is defined above yMax value across the glyph repertoire"""
    if ttFont["head"].yMax >= ttFont["OS/2"].usWinAscent:
        yield (
            FAIL,
            f"The OS/2.usWinAscent value must be larger "
            f"than the head.yMax value.  Received: OS/2.usWinAscent = "
            f"{ttFont['OS/2'].usWinAscent} head.yMax = {ttFont['head'].yMax}",
        )
    else:
        yield PASS, "The OS/2.winAscent definition is appropriate."


# OS/2.winDescent check
@check(
    id="com.google.fonts/check/googlesans/opentype/os2/windescent",
    rationale="""
    Confirms that the OS/2.winDescent value is defined below the yMin
    value across the full glyph repertoire.
    """,
)
def com_google_fonts_check_googlesans_opentype_os2_windescent(ttFont):
    """OS/2.winDescent is defined below yMin value across the glyph repertoire"""
    # note: WinDescent is expressed as a positive value even though the metric
    # extends below the baseline.  We must use unary neg operation for the
    # comparison here
    if ttFont["head"].yMin <= -ttFont["OS/2"].usWinDescent:
        yield (
            FAIL,
            f"The OS/2.usWinDescent value must be less "
            f"than the head.yMin value.  Received: OS/2.usWinDescent = "
            f"{ttFont['OS/2'].usWinDescent} head.yMin = {ttFont['head'].yMin}",
        )
    else:
        yield PASS, "The OS/2.winDescent value is appropriate."


# hhea.Ascent check
@check(
    id="com.google.fonts/check/googlesans/opentype/hhea/ascent",
    rationale="""
    Confirms that the hhea.ascent value is defined as expected
    """,
)
def com_google_fonts_check_googlesans_opentype_hhea_ascent(ttFont, config):
    """hhea.ascent is defined as expected"""
    check_config = config["com.google.fonts/check/googlesans/opentype/hhea/ascent"]
    hhea_ascent = check_config["hhea_ascent"]
    if ttFont["hhea"].ascent != hhea_ascent:
        yield (
            FAIL,
            f"The hhea.ascent value {ttFont['hhea'].ascent} does not "
            f"match the required value {hhea_ascent}",
        )
    else:
        yield PASS, "The hhea.ascent value matches the required value."


# hhea.Descent check
@check(
    id="com.google.fonts/check/googlesans/opentype/hhea/descent",
    rationale="""
    Confirms that the hhea.descent value is defined as expected
    """,
)
def com_google_fonts_check_googlesans_opentype_hhea_descent(ttFont, config):
    """hhea.descent is defined as expected"""
    check_config = config["com.google.fonts/check/googlesans/opentype/hhea/descent"]
    hhea_descent = check_config["hhea_descent"]
    if ttFont["hhea"].descent != hhea_descent:
        yield (
            FAIL,
            f"The hhea.descent value {ttFont['hhea'].descent} does not "
            f"match the required value {hhea_descent}",
        )
    else:
        yield PASS, "The hhea.descent value matches the required value."


# hhea.lineGap check
@check(
    id="com.google.fonts/check/googlesans/opentype/hhea/linegap",
    rationale="""
    Confirms that the hhea.lineGap value is defined as expected
    """,
)
def com_google_fonts_check_googlesans_opentype_hhea_linegap(ttFont, config):
    """hhea.linegap is defined as expected"""
    check_config = config["com.google.fonts/check/googlesans/opentype/hhea/linegap"]
    hhea_linegap = check_config["hhea_linegap"]
    if ttFont["hhea"].lineGap != hhea_linegap:
        yield (
            FAIL,
            f"The hhea.lineGap value {ttFont['hhea'].lineGap} does not "
            f"match the required value {hhea_linegap}",
        )
    else:
        yield PASS, "The hhea.lineGap value matches the required value."


# OS/2.typoDescender check
@check(
    id="com.google.fonts/check/googlesans/opentype/os2/typodescender",
    rationale="""
    Confirms that the OS/2.typoDescender value is defined as expected
    """,
)
def com_google_fonts_check_googlesans_opentype_os2_typodescender(ttFont, config):
    """OS/2.typoDescender is defined as expected"""
    check_config = config[
        "com.google.fonts/check/googlesans/opentype/os2/typodescender"
    ]
    os2_typodescender = check_config["os2_typodescender"]
    if ttFont["OS/2"].sTypoDescender != os2_typodescender:
        yield (
            FAIL,
            f"The OS/2.typoDescender value {ttFont['OS/2'].sTypoDescender} does not "
            f"match the required value {os2_typodescender}",
        )
    else:
        yield PASS, "The OS/2.typoDescender value matches the required value."


# OS/2.typoAscender check
@check(
    id="com.google.fonts/check/googlesans/opentype/os2/typoascender",
    rationale="""
    Confirms that the OS/2.typoAscender value is defined as expected
    """,
)
def com_google_fonts_check_googlesans_opentype_os2_typoascender(ttFont, config):
    """OS/2.typoAscender is defined as expected"""
    check_config = config["com.google.fonts/check/googlesans/opentype/os2/typoascender"]
    os2_typoascender = check_config["os2_typoascender"]
    if ttFont["OS/2"].sTypoAscender != os2_typoascender:
        yield (
            FAIL,
            f"The OS/2.typoAscender value {ttFont['OS/2'].sTypoAscender} does not "
            f"match the required value {os2_typoascender}",
        )
    else:
        yield PASS, "The OS/2.typoAscender value matches the required value."


# OS/2.typoLineGap check
@check(
    id="com.google.fonts/check/googlesans/opentype/os2/typolinegap",
    rationale="""
    Confirms that the OS/2.typoLineGap value is defined as expected
    """,
)
def com_google_fonts_check_googlesans_opentype_os2_typolinegap(ttFont, config):
    """OS/2.typoLineGap is defined as expected"""
    check_config = config["com.google.fonts/check/googlesans/opentype/os2/typolinegap"]
    os2_typolinegap = check_config["os2_typolinegap"]
    if ttFont["OS/2"].sTypoLineGap != os2_typolinegap:
        yield (
            FAIL,
            f"The OS/2.typoLineGap value {ttFont['OS/2'].sTypoLineGap} does not "
            f"match the required value {os2_typolinegap}",
        )
    else:
        yield PASS, "The OS/2.typoLineGap value matches the required value."


# ::::::::::::::::::::::::::::::::::::::::::::::::
# Other metrics
# ::::::::::::::::::::::::::::::::::::::::::::::::


# post underline checks
@check(
    id="com.google.fonts/check/googlesans/opentype/post/underline",
    rationale="""
    Confirms that the post table underline thickness and position are
    set to the correct values
    """,
)
def com_google_fonts_check_googlesans_opentype_post_underline(ttFont, config):
    """Post table underline thickness and position are set to correct values"""
    check_config = config["com.google.fonts/check/googlesans/opentype/post/underline"]
    post_underline_position = check_config["post_underline_position"]
    post_underline_thickness = check_config["post_underline_thickness"]

    # underline position
    if ttFont["post"].underlinePosition != post_underline_position:
        yield (
            FAIL,
            f"The post underline position value {ttFont['post'].underlinePosition} "
            f"does not match the required value {post_underline_position}",
        )
    else:
        yield PASS, "The post underline position value matches the required value."

    # underline thickness
    if ttFont["post"].underlineThickness != post_underline_thickness:
        yield (
            FAIL,
            f"The post underline thickness value {ttFont['post'].underlineThickness} "
            f"does not match the required value {post_underline_thickness}",
        )
    else:
        yield PASS, "The post underline thickness value matches the required value."


@check(
    id="com.google.fonts/check/googlesans/opentype/os2/strikeout",
    rationale="""
    Confirms that the OS/2 table strikeout size and position are
    set to the correct values
    """,
)
def com_google_fonts_check_googlesans_opentype_os2_strikeout(ttFont, config):
    """OS/2 table strikeout size and position are set to correct values"""
    check_config = config["com.google.fonts/check/googlesans/opentype/os2/strikeout"]
    os2_strikeout_position = check_config["os2_strikeout_position"]
    os2_strikeout_size = check_config["os2_strikeout_size"]

    # strikeout position
    if ttFont["OS/2"].yStrikeoutPosition != os2_strikeout_position:
        yield (
            FAIL,
            f"The OS/2 strikeout position value {ttFont['OS/2'].yStrikeoutPosition} "
            f"does not match the required value {os2_strikeout_position}",
        )
    else:
        yield PASS, "The OS/2 strikeout position value matches the required value."

    # strikeout thickness
    if ttFont["OS/2"].yStrikeoutSize != os2_strikeout_size:
        yield (
            FAIL,
            f"The OS/2 strikeout size value {ttFont['OS/2'].yStrikeoutSize} "
            f"does not match the required value {os2_strikeout_size}",
        )
    else:
        yield PASS, "The OS/2 strikeout size value matches the required value."


@check(
    id="com.google.fonts/check/googlesans/opentype/os2/unicode_range_bits",
    rationale="""
        When the UnicodeRange bits on the OS/2 table are not properly set, some programs
        running on Windows may not recognize the font and use a system fallback font
        instead. For that reason, this check calculates the proper settings by inspecting
        the glyphs declared on the cmap table and then ensures that their corresponding
        ranges are enabled.
    """,
    conditions=["unicoderange"],
)
def com_google_fonts_check_googlesans_unicode_range_bits(ttFont, unicoderange):
    """Ensure UnicodeRange bits are properly set."""
    expected_unicoderange = compute_unicoderange_bits(ttFont)
    difference = unicoderange ^ expected_unicoderange
    if not difference:
        yield PASS, "Unicode range bits are properly set"
    else:
        for bit in range(128):
            if difference & (1 << bit):
                range_name = unicoderange_bit_name(bit)
                num_chars = len(chars_in_range(ttFont, bit))
                range_size = sum(
                    entry[3] - entry[2] + 1 for entry in UNICODERANGE_DATA[bit]
                )
                if num_chars == 0:
                    set_unset = "0"
                    num_chars = "none"
                    yield FAIL, Message(
                        "bad-range-bit",
                        f"UnicodeRange bit {bit} '{range_name}' should be {set_unset} "
                        f"because cmap has {num_chars} of the {range_size} codepoints "
                        f"in this range.",
                    )
                else:
                    set_unset = "1"
                    yield WARN, Message(
                        "bad-range-bit",
                        f"UnicodeRange bit {bit} '{range_name}' should be {set_unset} "
                        f"because cmap has {num_chars} of the {range_size} codepoints "
                        f"in this range.",
                    )


# ================================================
# Variable build format specific
# ================================================


@check(
    id="com.google.fonts/check/googlesans/vf/fvaraxes",
    conditions=["is_variable_font"],
    rationale="""
    Confirms that the variable font format builds include
    all expected axis tags
    """,
)
def com_google_fonts_check_googlesans_variable_fvar_axes(ttFont, config):
    """Confirms that the variable font builds include expected axes."""
    check_config = config["com.google.fonts/check/googlesans/vf/fvaraxes"]
    expected_fvar_axes = check_config["expected_fvar_axes"]

    tt = ttFont
    observed_axis_list = []
    for axis in tt["fvar"].axes:
        observed_axis_list.append(axis.axisTag)

    if len(observed_axis_list) != len(expected_fvar_axes):
        yield (
            FAIL,
            f"{tt.reader.file.name} does not include the correct axis tags. \n"
            f"Observed: {observed_axis_list}\n"
            f"Expected: {expected_fvar_axes}",
        )

    has_all_tags = True
    for axis_tag in expected_fvar_axes:
        if axis_tag in observed_axis_list:
            pass
        else:
            has_all_tags = False
            yield (FAIL, f"{tt.reader.file.name} does not include axis tag {axis_tag}")

    if has_all_tags:
        yield (PASS, f"{tt.reader.file.name} includes all expected axis tags")


@check(
    id="com.google.fonts/check/googlesans/vf/fvardefault",
    conditions=["is_variable_font"],
    rationale="""
    Confirms that the variable font format builds include the expected fvar
    default definitions for the Google Sans design axes
    """,
)
def com_google_fonts_check_googlesans_variable_fvar_default(ttFont, config):
    """Confirms that the variable font builds include correct fvar default."""
    check_config = config["com.google.fonts/check/googlesans/vf/fvardefault"]
    axis_defaults = check_config["axis_defaults"]

    tt = ttFont

    for axis in tt["fvar"].axes:
        tag = axis.axisTag
        if tag in axis_defaults:
            if axis.defaultValue != axis_defaults[tag]:
                yield (
                    FAIL,
                    f"{tt.reader.file.name} does not include the correct "
                    f"fvar {tag} axis default.\n"
                    f"Found: `{axis.defaultValue}` and expected `{axis_defaults[tag]}`",
                )
            else:
                yield (
                    PASS,
                    f"{tt.reader.file.name} contains the expected fvar {tag} default.",
                )


# ================================================
#
# End check definitions
#
# ================================================
