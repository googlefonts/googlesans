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

import os
import sys

from fontbakery.checkrunner import Section, PASS, FAIL, WARN, ERROR, INFO, SKIP
from fontbakery.callable import condition, check, disable
from fontbakery.constants import PriorityLevel
from fontbakery.message import Message
from fontbakery.fonts_profile import profile_factory
from fontbakery.profiles.universal import UNIVERSAL_PROFILE_CHECKS

profile_imports = ("fontbakery.profiles.universal",)
profile = profile_factory(default_section=Section("Google Sans Custom Checks"))

GOOGLESANS_PROFILE_CHECKS = UNIVERSAL_PROFILE_CHECKS + [
    "com.google.fonts/check/googlesans/glyphs/glyphset-contents",
    "com.google.fonts/check/googlesans/opentype/os2/fsselectionbit7",
    "com.google.fonts/check/googlesans/opentype/os2/winascent",
    "com.google.fonts/check/googlesans/opentype/os2/windescent",
    "com.google.fonts/check/googlesans/opentype/hhea/ascent",
    "com.google.fonts/check/googlesans/opentype/hhea/descent",
    "com.google.fonts/check/googlesans/opentype/hhea/linegap",
    "com.google.fonts/check/googlesans/opentype/os2/typodescender",
    "com.google.fonts/check/googlesans/opentype/os2/typoascender",
    "com.google.fonts/check/googlesans/opentype/os2/typolinegap",
    "com.google.fonts/check/googlesans/features/staticuprights",
    "com.google.fonts/check/googlesans/features/staticitalics",
    "com.google.fonts/check/googlesans/features/variableuprights",
    "com.google.fonts/check/googlesans/features/variableitalics",
]

# define check ID's in the upstream `universal` profile
# that should be excluded here
excluded_check_ids = (
    "com.google.fonts/check/ftxvalidator_is_available",
    "com.google.fonts/check/dsig",
    "com.google.fonts/check/family/win_ascent_and_descent",  # replaced by custom checks
    "com.google.fonts/check/varfont/regular_opsz_coord",  # we really do want our opsz definition on regular instance
    # "com.google.fonts/check/os2_metrics_match_hhea",
    # "com.google.fonts/check/unwanted_tables",
)

ATTRIBUTES = {
    "os2_fsselection_bit7": 1,
    "ymax": 1115,  # defined at max across min + max opsz design space (from min opsz)
    "ymin": -292,  # defined at min across min + max opsz design space (from min opsz)
    "os2_win_ascent": 1115,  # must be defined at yMax value (https://github.com/Colophon-Foundry/google-sans/issues/160)
    "os2_win_descent": 292,  # must be defined at yMin value (https://github.com/Colophon-Foundry/google-sans/issues/160)
    "hhea_ascent": 966,  # set to match typo metrics values
    "hhea_descent": -286,
    "hhea_linegap": 0,
    "os2_typoascender": 966,  # set to match hhea metrics values
    "os2_typodescender": -286,
    "os2_typolinegap": 0,
}

STATIC_UPRIGHT_FEA = [
    "aalt",
    "c2sc",
    "calt",
    "case",
    "ccmp",
    "dlig",
    "dnom",
    "frac",
    "kern",
    "liga",
    "lnum",
    "locl",
    "mark",
    "mkmk",
    "numr",
    "ordn",
    "pnum",
    "sinf",
    "smcp",
    "ss01",
    "ss02",
    "ss03",
    "ss04",
    "ss05",
    "ss06",
    "ss07",
    "ss08",
    "subs",
    "sups",
    "tnum",
]

STATIC_ITALICS_FEA = [
    "aalt",
    "c2sc",
    "calt",
    "case",
    "ccmp",
    "dlig",
    "dnom",
    "frac",
    "kern",
    "liga",
    "lnum",
    "locl",
    "mark",
    "mkmk",
    "numr",
    "ordn",
    "pnum",
    "sinf",
    "smcp",
    "ss01",
    "ss02",
    "ss04",
    "ss05",
    "ss06",
    "ss07",
    "ss08",
    "subs",
    "sups",
    "tnum",
]

VAR_UPRIGHT_FEA = [
    "aalt",
    "c2sc",
    "calt",
    "case",
    "ccmp",
    "dlig",
    "dnom",
    "frac",
    "kern",
    "liga",
    "lnum",
    "locl",
    "mark",
    "mkmk",
    "numr",
    "ordn",
    "pnum",
    "rvrn",
    "sinf",
    "smcp",
    "ss01",
    "ss02",
    "ss03",
    "ss04",
    "ss05",
    "ss06",
    "ss07",
    "ss08",
    "subs",
    "sups",
    "tnum",
]

VAR_ITALICS_FEA = [
    "aalt",
    "c2sc",
    "calt",
    "case",
    "ccmp",
    "dlig",
    "dnom",
    "frac",
    "kern",
    "liga",
    "lnum",
    "locl",
    "mark",
    "mkmk",
    "numr",
    "ordn",
    "pnum",
    "rvrn",
    "sinf",
    "smcp",
    "ss01",
    "ss02",
    "ss04",
    "ss05",
    "ss06",
    "ss07",
    "ss08",
    "subs",
    "sups",
    "tnum",
]

# ================================================
#
# Conditions
#
# ================================================


@condition
def is_italic(ttFont):
    return "Italic" in ttFont.reader.file.name


@condition
def is_not_italic(ttFont):
    return "Italic" not in ttFont.reader.file.name


@condition
def is_not_variable_font(ttFont):
    return "fvar" not in ttFont.keys()


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
# Glyph set checks
# ================================================

# ::::::::::::::::::::::::::::::::::::::::::::::::
# Glyph set support
# ::::::::::::::::::::::::::::::::::::::::::::::::
# compare against a newline-delimited list of expected glyph names
# this includes all Unicode encoded and non-Unicode encoded glyph definitions


@check(
    id="com.google.fonts/check/googlesans/glyphs/glyphset-contents",
    rationale="""
    Confirms that the fonts include all expected Unicode encoded and \
    non-Unicode encoded glyph definitions. This test also confirms that \
    fonts have the expected glyph order.
    """,
)
def com_google_fonts_check_googlesans_glyphs_glyphset_contents(ttFonts):
    """Confirm that fonts have all expected Unicode encoded and \
       non-Unicoded encoded glyph definitions.This test also confirms \
       that the glyph order is defined as expected."""
    try:
        glyph_definition_basedir = os.path.join("qa", "definitions")

        tests_passed = True
        for tt in ttFonts:
            glyph_list_raw = ""
            base_file_path = os.path.basename(tt.reader.file.name) + ".glyphsetdef"
            expected_glyph_definition_path = os.path.join(glyph_definition_basedir, base_file_path)
            with open(expected_glyph_definition_path, "r") as f:
                glyph_list_raw = f.read()

            glyph_list = glyph_list_raw.split("\n")
            # must have (1) glyph set contents & (2) glyph set order as defined in def file
            if not (tt.getGlyphOrder() == glyph_list):
                tests_passed = False
                yield FAIL, "{} failed expected glyph set check".format(tt.reader.file.name)
        if tests_passed:
            yield PASS, "All fonts passed the expected glyph set checks"
    except Exception as e:
        sys.stderr.write("[ERROR]: {}".format(str(e)))
        sys.exit(1)


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
        yield FAIL, f"The hhea.lineGap value {ttFont['hhea'].lineGap} does not match the required value {ATTRIBUTES['hhea_linegap']}"
    else:
        yield PASS, f"The hhea.lineGap value matches the required value."


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
        yield FAIL, f"The OS/2.typoDescender value {ttFont['OS/2'].sTypoDescender} does not match the required value {ATTRIBUTES['os2_typodescender']}"
    else:
        yield PASS, f"The OS/2.typoDescender value matches the required value."


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
        yield FAIL, f"The OS/2.typoAscender value {ttFont['OS/2'].sTypoAscender} does not match the required value {ATTRIBUTES['os2_typoascender']}"
    else:
        yield PASS, f"The OS/2.typoAscender value matches the required value."


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
        yield FAIL, f"The OS/2.typoLineGap value {ttFont['OS/2'].sTypoLineGap} does not match the required value {ATTRIBUTES['os2_typolinegap']}"
    else:
        yield PASS, f"The OS/2.typoLineGap value matches the required value."


# ================================================
# Feature support
# ================================================

# statics
@check(
    id="com.google.fonts/check/googlesans/features/staticuprights",
    conditions=["is_not_italic", "is_not_variable_font"],
    rationale="""
    Confirms that the upright builds contain expected feature tags.
    """,
)
def com_google_fonts_check_googlesans_features_static_uprights(ttFont):
    """Confirms that the upright builds contain expected feature tags."""
    tt = ttFont
    gpos = tt["GPOS"]
    gsub = tt["GSUB"]

    fea_tags = set()

    for gpos_record in gpos.table.FeatureList.FeatureRecord:
        fea_tags.add(gpos_record.FeatureTag)

    for gsub_record in gsub.table.FeatureList.FeatureRecord:
        fea_tags.add(gsub_record.FeatureTag)

    if sorted(fea_tags) == STATIC_UPRIGHT_FEA:
        yield PASS, f"{tt.reader.file.name} contains the expected feature tags"
    else:
        yield FAIL, f"{tt.reader.file.name} does not contain the expected feature tags.\nFound:{sorted(fea_tags)}\nExpected:{STATIC_UPRIGHT_FEA}"


@check(
    id="com.google.fonts/check/googlesans/features/staticitalics",
    conditions=["is_italic", "is_not_variable_font"],
    rationale="""
    Confirms that the italics builds contain expected feature tags.
    """,
)
def com_google_fonts_check_googlesans_features_static_italics(ttFont):
    """Confirms that the italics builds contain expected feature tags."""
    tt = ttFont
    gpos = tt["GPOS"]
    gsub = tt["GSUB"]

    fea_tags = set()

    for gpos_record in gpos.table.FeatureList.FeatureRecord:
        fea_tags.add(gpos_record.FeatureTag)

    for gsub_record in gsub.table.FeatureList.FeatureRecord:
        fea_tags.add(gsub_record.FeatureTag)

    if sorted(fea_tags) == STATIC_ITALICS_FEA:
        yield PASS, f"{tt.reader.file.name} contains the expected feature tags"
    else:
        yield FAIL, f"{tt.reader.file.name} does not contain the expected feature tags.\nFound:{sorted(fea_tags)}\nExpected:{STATIC_ITALICS_FEA}"


# VF
@check(
    id="com.google.fonts/check/googlesans/features/variableuprights",
    conditions=["is_not_italic", "is_variable_font"],
    rationale="""
    Confirms that the variable upright builds contain expected feature tags.
    """,
)
def com_google_fonts_check_googlesans_features_variable_uprights(ttFont):
    """Confirms that the upright builds contain expected feature tags."""
    tt = ttFont
    gpos = tt["GPOS"]
    gsub = tt["GSUB"]

    fea_tags = set()

    for gpos_record in gpos.table.FeatureList.FeatureRecord:
        fea_tags.add(gpos_record.FeatureTag)

    for gsub_record in gsub.table.FeatureList.FeatureRecord:
        fea_tags.add(gsub_record.FeatureTag)

    if sorted(fea_tags) == VAR_UPRIGHT_FEA:
        yield PASS, f"{tt.reader.file.name} contains the expected feature tags"
    else:
        yield FAIL, f"{tt.reader.file.name} does not contain the expected feature tags.\nFound:{sorted(fea_tags)}\nExpected:{VAR_UPRIGHT_FEA}"


@check(
    id="com.google.fonts/check/googlesans/features/variableitalics",
    conditions=["is_italic", "is_variable_font"],
    rationale="""
    Confirms that the variable italics builds contain expected feature tags.
    """,
)
def com_google_fonts_check_googlesans_features_variable_italics(ttFont):
    """Confirms that the italics builds contain expected feature tags."""
    tt = ttFont
    gpos = tt["GPOS"]
    gsub = tt["GSUB"]

    fea_tags = set()

    for gpos_record in gpos.table.FeatureList.FeatureRecord:
        fea_tags.add(gpos_record.FeatureTag)

    for gsub_record in gsub.table.FeatureList.FeatureRecord:
        fea_tags.add(gsub_record.FeatureTag)

    if sorted(fea_tags) == VAR_ITALICS_FEA:
        yield PASS, f"{tt.reader.file.name} contains the expected feature tags"
    else:
        yield FAIL, f"{tt.reader.file.name} does not contain the expected feature tags.\nFound:{sorted(fea_tags)}\nExpected:{VAR_ITALICS_FEA}"


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
