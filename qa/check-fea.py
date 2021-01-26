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

from pathlib import Path

from fontbakery.checkrunner import Section, PASS, FAIL, SKIP
from fontbakery.callable import check, condition
from fontbakery.fonts_profile import profile_factory

profile_imports = ()
profile = profile_factory(
    default_section=Section("Google Sans Custom Feature Support Checks")
)

GOOGLESANS_PROFILE_CHECKS = [
    "com.google.fonts/check/googlesans/features/staticuprights",
    "com.google.fonts/check/googlesans/features/staticitalics",
    "com.google.fonts/check/googlesans/features/variableuprights",
    "com.google.fonts/check/googlesans/features/variableitalics",
    "com.google.fonts/check/googlesans/features/armenian/min_opsz",
]

STATIC_UPRIGHT_FEA = [
    "aalt",
    "c2sc",
    "calt",
    "case",
    "ccmp",
    "dlig",
    "dnom",
    "frac",
    "jalt",
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
    "jalt",
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
    "jalt",
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
    "jalt",
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


@condition
def is_variable_font(ttFont):
    return "fvar" in ttFont.keys()


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


@check(id="com.google.fonts/check/googlesans/features/armenian/min_opsz",
    conditions=["is_not_italic", "is_not_variable_font"],
)
def com_google_fonts_check_googlesans_features_armenian_min_opsz(ttFont):
    """But does it shape?"""
    tt = ttFont
    
    # if not tt.reader.file.name.endswith("GoogleSansText-Regular.ttf"):
    #     yield SKIP, "..."
    #     return
    
    import json
    armn_shaping_basedir = Path("qa", "shaping", "armenian")
    for input_file in armn_shaping_basedir.glob("*.txt"):
        shaped_text = shape_text(tt.reader.file.name, input_file, {"ccmp": True})
        shaped_text_expected = json.loads(input_file.with_suffix(".json").read_text())
        if shaped_text == shaped_text_expected:
            yield PASS, "..."
        else:
            yield FAIL, "..."


profile.auto_register(globals())
profile.test_expected_checks(GOOGLESANS_PROFILE_CHECKS, exclusive=True)

from typing import Any, Dict, List

import uharfbuzz as hb


def shape_text(
    font_path: str, text_path: str, features: Dict[str, bool]
) -> List[Dict[str, Any]]:
    """Return Harfbuzz-shaped text from input for font.
    
    NOTE: copy-pasta from harfbuzz.py because fontbakery doesn't knwo how to import it.
    """

    with open(font_path, "rb") as fontfile:
        fontdata = fontfile.read()

    with open(text_path, "r") as textfile:
        text = textfile.read()

    face = hb.Face(fontdata)
    font = hb.Font(face)
    upem = face.upem

    font.scale = (upem, upem)
    hb.ot_font_set_funcs(font)

    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, features)

    infos = buf.glyph_infos
    positions = buf.glyph_positions

    return [
        {
            "glyph": font.get_glyph_name(info.codepoint),
            "cluster": info.cluster,
            "x_offset": pos.x_offset,
            "y_offset": pos.y_offset,
            "x_advance": pos.x_advance,
            "y_advance": pos.y_advance,
        }
        for info, pos in zip(infos, positions)
    ]