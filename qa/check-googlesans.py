import os

from fontbakery.checkrunner import Section, PASS, FAIL, WARN, ERROR, INFO, SKIP
from fontbakery.callable import condition, check, disable
from fontbakery.constants import PriorityLevel
from fontbakery.message import Message
from fontbakery.fonts_profile import profile_factory
from fontbakery.profiles.universal import UNIVERSAL_PROFILE_CHECKS

profile_imports = ("fontbakery.profiles.universal",)
profile = profile_factory(default_section=Section("Google Sans Custom Checks"))

GOOGLESANS_PROFILE_CHECKS = UNIVERSAL_PROFILE_CHECKS + [
    "com.google.fonts/check/googlesans/opentype/os2/fsselectionbit7",
    "com.google.fonts/check/googlesans/opentype/os2/winascent",
    "com.google.fonts/check/googlesans/opentype/os2/windescent",
    "com.google.fonts/check/googlesans/opentype/hhea/ascent",
    "com.google.fonts/check/googlesans/opentype/hhea/descent",
]

# define check ID's in the upstream `universal` profile
# that should be excluded here
excluded_check_ids = (
    "com.google.fonts/check/ftxvalidator_is_available",
    "com.google.fonts/check/dsig",
    "com.google.fonts/check/family/win_ascent_and_descent",  # replaced by custom checks
    # "com.google.fonts/check/os2_metrics_match_hhea",
    # "com.google.fonts/check/unwanted_tables",
)

ATTRIBUTES = {
    "os2_fsselection_bit7": 1,
    "ymax": 1115,  # defined at max across min + max opsz design space (from min opsz)
    "ymin": -292,  # defined at min across min + max opsz design space (from min opsz)
    "os2_win_ascent": 1115,  # must be defined at yMax value (https://github.com/Colophon-Foundry/google-sans/issues/160)
    "os2_win_descent": 292,  # must be defined at yMin value (https://github.com/Colophon-Foundry/google-sans/issues/160)
    "hhea_ascent": 966,
    "hhea_descent": -286,
    "os2_typoascender": 966,
    "os2_typodescender": -286,
}


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
        yield FAIL, f"The OS/2.fsSelection bit 7 (USE_TYPO_METRICS) was NOT set in the following fonts: {fail_list}."
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
        yield FAIL, f"The OS/2.winAscent value {ttFont['OS/2'].usWinAscent} does not match the required value {ATTRIBUTES['os2_win_ascent']}"
    else:
        yield PASS, f"The OS/2.winAscent value matches the required value."


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
        yield FAIL, f"The OS/2.winDescent value {ttFont['OS/2'].usWinDescent} does not match the required value {ATTRIBUTES['os2_win_descent']}"
    else:
        yield PASS, f"The OS/2.winDescent value matches the required value."


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
        yield FAIL, f"The hhea.ascent value {ttFont['hhea'].ascent} does not match the required value {ATTRIBUTES['hhea_ascent']}"
    else:
        yield PASS, f"The hhea.ascent value matches the required value."


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
        yield FAIL, f"The hhea.descent value {ttFont['hhea'].descent} does not match the required value {ATTRIBUTES['hhea_descent']}"
    else:
        yield PASS, f"The hhea.descent value matches the required value."


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
