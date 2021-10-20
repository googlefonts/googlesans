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


from fontbakery.checkrunner import Section, PASS, FAIL, WARN
from fontbakery.callable import check
from fontbakery.fonts_profile import profile_factory
from fontbakery.profiles.universal import UNIVERSAL_PROFILE_CHECKS
from fontbakery.constants import UNICODERANGE_DATA
from fontbakery.utils import (
    compute_unicoderange_bits,
    unicoderange_bit_name,
    chars_in_range,
)
from fontbakery.message import Message

profile_imports = ("fontbakery.profiles.universal",)
profile = profile_factory(default_section=Section("Google Sans Custom Checks"))

GOOGLESANS_PROFILE_CHECKS = UNIVERSAL_PROFILE_CHECKS + [
    "com.google.fonts/check/googlesans/opentype/os2/fsselectionbit7",
    "com.google.fonts/check/googlesans/opentype/os2/winascent",
    "com.google.fonts/check/googlesans/opentype/os2/windescent",
    "com.google.fonts/check/googlesans/opentype/hhea/ascent",
    "com.google.fonts/check/googlesans/opentype/hhea/descent",
    "com.google.fonts/check/googlesans/opentype/hhea/linegap",
    "com.google.fonts/check/googlesans/opentype/os2/strikeout",
    "com.google.fonts/check/googlesans/opentype/os2/typodescender",
    "com.google.fonts/check/googlesans/opentype/os2/typoascender",
    "com.google.fonts/check/googlesans/opentype/os2/typolinegap",
    "com.google.fonts/check/googlesans/opentype/os2/unicode_range_bits",
    "com.google.fonts/check/googlesans/opentype/post/underline",
    "com.google.fonts/check/googlesans/vf/fvaraxes",
    "com.google.fonts/check/googlesans/vf/fvardefault",
]

# define check ID's in the upstream `universal` profile
# that should be excluded here
excluded_check_ids = (
    "com.google.fonts/check/ftxvalidator_is_available",
    "com.google.fonts/check/dsig",
    "com.google.fonts/check/family/win_ascent_and_descent",  # replaced by custom checks
    "com.google.fonts/check/varfont/regular_opsz_coord",  # we do want our opsz definition
    # "com.google.fonts/check/os2_metrics_match_hhea",
    # "com.google.fonts/check/unwanted_tables",
    "com.google.fonts/check/outline_jaggy_segments",  # too many unactionable warnings
    "com.google.fonts/check/outline_semi_vertical",  # design rather than QA problem
)

ATTRIBUTES = {
    "os2_fsselection_bit7": 1,
    "ymax": 1115,  # defined at max across min + max opsz design space (from min opsz)
    "ymin": -292,  # defined at min across min + max opsz design space (from min opsz)
    "os2_win_ascent": 1115,  # must be defined at yMax value
    "os2_win_descent": 292,  # must be defined at yMin value
    "hhea_ascent": 966,  # set to match typo metrics values
    "hhea_descent": -286,
    "hhea_linegap": 0,
    "os2_strikeout_position": 306,
    "os2_strikeout_size": 84,
    "os2_typoascender": 966,  # set to match hhea metrics values
    "os2_typodescender": -286,
    "os2_typolinegap": 0,
    "expected_fvar_axes": ["opsz", "wght", "GRAD"],
    "opsz_axis_default": 18.0,
    "post_underline_position": -160,
    "post_underline_thickness": 84,
    "wght_axis_default": 400.0,
    "grad_axis_default": 0.0,
}


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
def com_google_fonts_check_googlesans_opentype_os2_fsselectionbit7(ttFonts):
    """OS/2.fsSelection bit 7 (USE_TYPO_METRICS) is set in all fonts"""
    os2_fsselection_bit7_isset = ATTRIBUTES["os2_fsselection_bit7"] == 1

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


# Note: winAscent and winDescent are defined at yMin and yMax values across the
# entire design space
# OS/2.winAscent check
@check(
    id="com.google.fonts/check/googlesans/opentype/os2/winascent",
    rationale="""
    Confirms that the OS/2.winAscent value is defined at the yMax
    value across the entire design space
    """,
)
def com_google_fonts_check_googlesans_opentype_os2_winascent(ttFont):
    """OS/2.winAscent is defined at yMax value across the entire design space"""
    if ttFont["OS/2"].usWinAscent != ATTRIBUTES["os2_win_ascent"]:
        yield (
            FAIL,
            f"The OS/2.winAscent value {ttFont['OS/2'].usWinAscent} does not "
            f"match the required value {ATTRIBUTES['os2_win_ascent']}",
        )
    else:
        yield PASS, "The OS/2.winAscent value matches the required value."


# OS/2.winDescent check
@check(
    id="com.google.fonts/check/googlesans/opentype/os2/windescent",
    rationale="""
    Confirms that the OS/2.winDescent value is defined at the yMin
    value across the entire design space
    """,
)
def com_google_fonts_check_googlesans_opentype_os2_windescent(ttFont):
    """OS/2.winDescent is defined at yMin value across the entire design space"""
    if ttFont["OS/2"].usWinDescent != ATTRIBUTES["os2_win_descent"]:
        yield (
            FAIL,
            f"The OS/2.winDescent value {ttFont['OS/2'].usWinDescent} does not "
            f"match the required value {ATTRIBUTES['os2_win_descent']}",
        )
    else:
        yield PASS, "The OS/2.winDescent value matches the required value."


# hhea.Ascent check
@check(
    id="com.google.fonts/check/googlesans/opentype/hhea/ascent",
    rationale="""
    Confirms that the hhea.ascent value is defined as expected
    """,
)
def com_google_fonts_check_googlesans_opentype_hhea_ascent(ttFont):
    """hhea.ascent is defined as expected"""
    if ttFont["hhea"].ascent != ATTRIBUTES["hhea_ascent"]:
        yield (
            FAIL,
            f"The hhea.ascent value {ttFont['hhea'].ascent} does not "
            f"match the required value {ATTRIBUTES['hhea_ascent']}",
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
def com_google_fonts_check_googlesans_opentype_hhea_descent(ttFont):
    """hhea.descent is defined as expected"""
    if ttFont["hhea"].descent != ATTRIBUTES["hhea_descent"]:
        yield (
            FAIL,
            f"The hhea.descent value {ttFont['hhea'].descent} does not "
            f"match the required value {ATTRIBUTES['hhea_descent']}",
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
def com_google_fonts_check_googlesans_opentype_hhea_linegap(ttFont):
    """hhea.linegap is defined as expected"""
    if ttFont["hhea"].lineGap != ATTRIBUTES["hhea_linegap"]:
        yield (
            FAIL,
            f"The hhea.lineGap value {ttFont['hhea'].lineGap} does not "
            f"match the required value {ATTRIBUTES['hhea_linegap']}",
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
def com_google_fonts_check_googlesans_opentype_os2_typodescender(ttFont):
    """OS/2.typoDescender is defined as expected"""
    if ttFont["OS/2"].sTypoDescender != ATTRIBUTES["os2_typodescender"]:
        yield (
            FAIL,
            f"The OS/2.typoDescender value {ttFont['OS/2'].sTypoDescender} does not "
            f"match the required value {ATTRIBUTES['os2_typodescender']}",
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
def com_google_fonts_check_googlesans_opentype_os2_typoascender(ttFont):
    """OS/2.typoAscender is defined as expected"""
    if ttFont["OS/2"].sTypoAscender != ATTRIBUTES["os2_typoascender"]:
        yield (
            FAIL,
            f"The OS/2.typoAscender value {ttFont['OS/2'].sTypoAscender} does not "
            f"match the required value {ATTRIBUTES['os2_typoascender']}",
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
def com_google_fonts_check_googlesans_opentype_os2_typolinegap(ttFont):
    """OS/2.typoLineGap is defined as expected"""
    if ttFont["OS/2"].sTypoLineGap != ATTRIBUTES["os2_typolinegap"]:
        yield (
            FAIL,
            f"The OS/2.typoLineGap value {ttFont['OS/2'].sTypoLineGap} does not "
            f"match the required value {ATTRIBUTES['os2_typolinegap']}",
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
def com_google_fonts_check_googlesans_opentype_post_underline(ttFont):
    """Post table underline thickness and position are set to correct values"""

    # underline position
    if ttFont["post"].underlinePosition != ATTRIBUTES["post_underline_position"]:
        yield (
            FAIL,
            f"The post underline position value {ttFont['post'].underlinePosition} "
            f"does not match the required value {ATTRIBUTES['post_underline_position']}",
        )
    else:
        yield PASS, "The post underline position value matches the required value."

    # underline thickness
    if ttFont["post"].underlineThickness != ATTRIBUTES["post_underline_thickness"]:
        yield (
            FAIL,
            f"The post underline thickness value {ttFont['post'].underlineThickness} "
            f"does not match the required value {ATTRIBUTES['post_underline_thickness']}",
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
def com_google_fonts_check_googlesans_opentype_os2_strikeout(ttFont):
    """OS/2 table strikeout size and position are set to correct values"""

    # strikeout position
    if ttFont["OS/2"].yStrikeoutPosition != ATTRIBUTES["os2_strikeout_position"]:
        yield (
            FAIL,
            f"The OS/2 strikeout position value {ttFont['OS/2'].yStrikeoutPosition} "
            f"does not match the required value {ATTRIBUTES['os2_strikeout_position']}",
        )
    else:
        yield PASS, "The OS/2 strikeout position value matches the required value."

    # strikeout thickness
    if ttFont["OS/2"].yStrikeoutSize != ATTRIBUTES["os2_strikeout_size"]:
        yield (
            FAIL,
            f"The OS/2 strikeout size value {ttFont['OS/2'].yStrikeoutSize} "
            f"does not match the required value {ATTRIBUTES['os2_strikeout_size']}",
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
def com_google_fonts_check_googlesans_variable_fvar_axes(ttFont):
    """Confirms that the variable font builds include expected axes."""
    tt = ttFont
    observed_axis_list = []
    for axis in tt["fvar"].axes:
        observed_axis_list.append(axis.axisTag)

    if len(observed_axis_list) != len(ATTRIBUTES["expected_fvar_axes"]):
        yield (
            FAIL,
            f"{tt.reader.file.name} does not include the correct axis tags. \n"
            f"Observed: {observed_axis_list}\n"
            f"Expected: {ATTRIBUTES['expected_fvar_axes']}",
        )

    has_all_tags = True
    for axis_tag in ATTRIBUTES["expected_fvar_axes"]:
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
def com_google_fonts_check_googlesans_variable_fvar_default(ttFont):
    """Confirms that the variable font builds include correct fvar default."""
    tt = ttFont
    EXPECTED_OPSZ = ATTRIBUTES["opsz_axis_default"]
    EXPECTED_WGHT = ATTRIBUTES["wght_axis_default"]
    EXPECTED_GRAD = ATTRIBUTES["grad_axis_default"]

    for axis in tt["fvar"].axes:
        if axis.axisTag == "opsz":
            if axis.defaultValue != EXPECTED_OPSZ:
                yield (
                    FAIL,
                    f"{tt.reader.file.name} does not include the correct "
                    f"fvar opsz axis default.\n"
                    f"Found: `{axis.defaultValue}` and expected `{EXPECTED_OPSZ}`",
                )
            else:
                yield (
                    PASS,
                    f"{tt.reader.file.name} contains the expected fvar " f"opsz default.",
                )
        elif axis.axisTag == "wght":
            if axis.defaultValue != EXPECTED_WGHT:
                yield (
                    FAIL,
                    f"{tt.reader.file.name} does not include the correct "
                    f"fvar wght axis default.\n"
                    f"Found: `{axis.defaultValue}` and expected `{EXPECTED_WGHT}`",
                )
            else:
                yield (
                    PASS,
                    f"{tt.reader.file.name} contains the expected fvar " f"opsz default.",
                )
        elif axis.axisTag == "GRAD":
            if axis.defaultValue != EXPECTED_GRAD:
                yield (
                    FAIL,
                    f"{tt.reader.file.name} does not include the correct "
                    f"fvar GRAD axis default.\n"
                    f"Found: `{axis.defaultValue}` and expected `{EXPECTED_GRAD}`",
                )
            else:
                yield (
                    PASS,
                    f"{tt.reader.file.name} contains the expected fvar " f"GRAD default.",
                )


# ================================================
#
# End check definitions
#
# ================================================

# skip filter function to exclude checks defined in the
# fontbakery universal profile
def check_skip_filter(checkid, font=None, **iterargs):
    if font and checkid in excluded_check_ids:
        return False, ("Check skipped in Google Sans profile")
    return True, None


profile.check_skip_filter = check_skip_filter
profile.auto_register(globals())
profile.test_expected_checks(GOOGLESANS_PROFILE_CHECKS, exclusive=True)
