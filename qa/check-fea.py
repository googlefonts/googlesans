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

import json
import sys
import textwrap
from pathlib import Path

import uharfbuzz
from fontbakery.callable import check, condition
from fontbakery.checkrunner import FAIL, PASS, SKIP, Section
from fontbakery.fonts_profile import profile_factory

# Make FontBakery able to find the update_shaping_test_data package.
sys.path.append(str(Path(__file__).parent.parent))

from qa.update_shaping_test_data import (  # noqa: E402
    ComparisonMode,
    Direction,
    shape_texts,
)


profile_imports = ()
profile = profile_factory(
    default_section=Section("Google Sans Custom Feature Support Checks")
)

GOOGLESANS_PROFILE_CHECKS = [
    "com.google.fonts/check/googlesans/features/staticuprights",
    "com.google.fonts/check/googlesans/features/staticitalics",
    "com.google.fonts/check/googlesans/features/variableuprights",
    "com.google.fonts/check/googlesans/features/variableitalics",
    "com.google.fonts/check/googlesans/features/regression",
]

STATIC_UPRIGHT_FEA = [
    "abvf",
    "abvm",
    "abvs",
    "akhn",
    "blwf",
    "blwm",
    "blws",
    "c2sc",
    "calt",
    "case",
    "ccmp",
    "cjct",
    "clig",
    "dist",
    "dlig",
    "dnom",
    "frac",
    "half",
    "haln",
    "hist",
    "init",
    "jalt",
    "kern",
    "liga",
    "lnum",
    "locl",
    "mark",
    "mkmk",
    "nukt",
    "numr",
    "ordn",
    "pnum",
    "pref",
    "pres",
    "pstf",
    "psts",
    "rclt",
    "rkrf",
    "rlig",
    "rphf",
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
    "ss09",
    "subs",
    "sups",
    "tnum",
    "vatu",
]

STATIC_ITALICS_FEA = [
    "abvf",
    "abvm",
    "abvs",
    "akhn",
    "blwf",
    "blwm",
    "blws",
    "c2sc",
    "calt",
    "case",
    "ccmp",
    "cjct",
    "clig",
    "dist",
    "dlig",
    "dnom",
    "frac",
    "half",
    "haln",
    "hist",
    "init",
    "jalt",
    "kern",
    "liga",
    "lnum",
    "locl",
    "mark",
    "mkmk",
    "nukt",
    "numr",
    "ordn",
    "pnum",
    "pref",
    "pres",
    "pstf",
    "psts",
    "rclt",
    "rkrf",
    "rlig",
    "rphf",
    "sinf",
    "smcp",
    "ss01",
    "ss02",
    "ss04",
    "ss05",
    "ss06",
    "ss07",
    "ss08",
    "ss09",
    "subs",
    "sups",
    "tnum",
    "vatu",
]

VAR_UPRIGHT_FEA = [
    "abvf",
    "abvm",
    "abvs",
    "akhn",
    "blwf",
    "blwm",
    "blws",
    "c2sc",
    "calt",
    "case",
    "ccmp",
    "cjct",
    "clig",
    "dist",
    "dlig",
    "dnom",
    "frac",
    "half",
    "haln",
    "hist",
    "init",
    "jalt",
    "kern",
    "liga",
    "lnum",
    "locl",
    "mark",
    "mkmk",
    "nukt",
    "numr",
    "ordn",
    "pnum",
    "pref",
    "pres",
    "pstf",
    "psts",
    "rclt",
    "rkrf",
    "rlig",
    "rphf",
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
    "ss09",
    "subs",
    "sups",
    "tnum",
    "vatu",
]

VAR_ITALICS_FEA = [
    "abvf",
    "abvm",
    "abvs",
    "akhn",
    "blwf",
    "blwm",
    "blws",
    "c2sc",
    "calt",
    "case",
    "ccmp",
    "cjct",
    "clig",
    "dist",
    "dlig",
    "dnom",
    "frac",
    "half",
    "haln",
    "hist",
    "init",
    "jalt",
    "kern",
    "liga",
    "lnum",
    "locl",
    "mark",
    "mkmk",
    "nukt",
    "numr",
    "ordn",
    "pnum",
    "pref",
    "pres",
    "pstf",
    "psts",
    "rclt",
    "rkrf",
    "rlig",
    "rphf",
    "sinf",
    "smcp",
    "ss01",
    "ss02",
    "ss04",
    "ss05",
    "ss06",
    "ss07",
    "ss08",
    "ss09",
    "subs",
    "sups",
    "tnum",
    "vatu",
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


@condition
def is_variable_font(ttFont):
    return "fvar" in ttFont.keys()


@condition
def hb_font(font):
    with open(font, "rb") as fontfile:
        hb_face = uharfbuzz.Face(fontfile.read())
    return hb_face


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
        yield (
            FAIL,
            f"{tt.reader.file.name} does not contain the expected feature tags.\n"
            f"Found:{sorted(fea_tags)}\nExpected:{STATIC_UPRIGHT_FEA}",
        )


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
        yield (
            FAIL,
            f"{tt.reader.file.name} does not contain the expected feature tags.\n"
            f"Found:{sorted(fea_tags)}\nExpected:{STATIC_ITALICS_FEA}",
        )


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
        yield (
            FAIL,
            f"{tt.reader.file.name} does not contain the expected feature tags.\n"
            f"Found:{sorted(fea_tags)}\nExpected:{VAR_UPRIGHT_FEA}",
        )


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
        yield (
            FAIL,
            f"{tt.reader.file.name} does not contain the expected feature tags.\n"
            f"Found:{sorted(fea_tags)}\nExpected:{VAR_ITALICS_FEA}",
        )


@check(id="com.google.fonts/check/googlesans/features/regression")
def com_google_fonts_check_googlesans_features_regression(ttFont, hb_font):
    """But does it shape?"""
    tt = ttFont
    filename = Path(tt.reader.file.name)

    shaping_file_found = False
    shaping_basedir = Path("qa", "shaping")
    for shaping_file in shaping_basedir.glob("*.json"):
        shaping_file_found = True
        shaping_input_doc = json.loads(shaping_file.read_text())

        try:
            shaping_input = shaping_input_doc["input"]
        except KeyError:
            yield FAIL, (f"{shaping_file}: Must have an 'input' key dict.")
            return
        try:
            shaping_texts = shaping_input["text"]
        except KeyError as e:
            yield FAIL, (f"{shaping_file}: 'input' key dict is missing {str(e)} key.")
            return
        shaping_features = shaping_input.get("features", {})
        shaping_script = shaping_input.get("script")
        shaping_language = shaping_input.get("language")
        shaping_comparison_mode = ComparisonMode(
            shaping_input.get("comparison_mode", "full")
        )
        shaping_direction = Direction(shaping_input.get("direction", "ltr"))
        try:
            shaping_output = shaping_input_doc["output"]
        except KeyError:
            yield FAIL, (f"{shaping_file}: Must have an 'output' key dict.")
            return
        try:
            shaped_texts_expected = shaping_output[filename.name]
        except KeyError:
            yield FAIL, f"{shaping_file}: No entry found for {filename.name}"
            return

        shaped_texts = shape_texts(
            tt,
            hb_font,
            shaping_texts,
            shaping_script,
            shaping_language,
            shaping_direction,
            shaping_features,
            shaping_comparison_mode,
        )

        if shaped_texts == shaped_texts_expected:
            yield PASS, f"{shaping_file}: No regression detected"
        else:
            if "fvar" in tt:
                assert isinstance(shaped_texts, dict)
                assert isinstance(shaped_texts_expected, dict)

                for key, shaped_text in shaped_texts.items():
                    try:
                        expected = shaped_texts_expected[key]
                    except KeyError as e:
                        yield FAIL, (
                            f"{shaping_file}: No entry found for {filename.name}, "
                            f" instance {e}"
                        )
                        continue
                    if shaped_text != expected:
                        shaped_texts_str = textwrap.indent("\n".join(shaped_text), "\t  ")
                        shaped_texts_expected_str = textwrap.indent(
                            "\n".join(expected), "\t  "
                        )
                        yield FAIL, (
                            f"{shaping_file}: Expected and actual shaping not matching."
                            f"\n\tExpected for {key}:\n"
                            f"{shaped_texts_expected_str}"
                            "\n\tActual:\n"
                            f"{shaped_texts_str}"
                        )
            else:
                assert isinstance(shaped_texts, list)
                assert isinstance(shaped_texts_expected, list)

                shaped_texts_str = textwrap.indent("\n".join(shaped_texts), "\t  ")
                shaped_texts_expected_str = textwrap.indent(
                    "\n".join(shaped_texts_expected), "\t  "
                )
                yield FAIL, (
                    f"{shaping_file}: Expected and actual shaping not matching."
                    "\n\tExpected:\n"
                    f"{shaped_texts_expected_str}"
                    "\n\tActual:\n"
                    f"{shaped_texts_str}"
                )

    if not shaping_file_found:
        yield SKIP, "No test files found."


profile.auto_register(globals())
profile.test_expected_checks(GOOGLESANS_PROFILE_CHECKS, exclusive=True)
