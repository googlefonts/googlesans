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
    "com.google.fonts/check/googlesans/testpass",
]

# define check ID's in the upstream `universal` profile
# that should be excluded here
excluded_check_ids = (
    "com.google.fonts/check/ftxvalidator_is_available",
    # "com.google.fonts/check/os2_metrics_match_hhea",
    # "com.google.fonts/check/unwanted_tables",
    # "com.google.fonts/check/dsig",
)

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

# Test pass template
@check(
    id="com.google.fonts/check/googlesans/testpass",
    rationale="""
        This is a test pass rationale.
    """,
)
def com_google_fonts_check_googlesans_test_pass():
    """A test pass example."""
    yield PASS, "test pass message"


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
