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

import difflib
import enum
import json
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

import uharfbuzz as hb
from fontbakery.callable import check, condition
from fontbakery.checkrunner import FAIL, PASS, Section
from fontbakery.fonts_profile import profile_factory
from fontTools.ttLib import TTFont

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


@check(id="com.google.fonts/check/googlesans/features/regression")
def com_google_fonts_check_googlesans_features_regression(ttFont):
    """But does it shape?"""
    tt = ttFont
    filename = Path(tt.reader.file.name)

    shaping_basedir = Path("qa", "shaping")
    for shaping_file in shaping_basedir.glob("*.json"):
        shaping_input_doc = json.loads(shaping_file.read_text())

        try:
            shaping_input = shaping_input_doc["input"]
        except KeyError:
            yield FAIL, (f"{shaping_file}: Must have an 'input' key dict.")
            return
        try:
            shaping_texts = shaping_input["text"]
            shaping_features = shaping_input["features"]
            shaping_script = shaping_input["script"]
            shaping_language = shaping_input["language"]
        except KeyError as e:
            yield FAIL, (f"{shaping_file}: 'input' key dict is missing {str(e)} key.")
            return
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
            shaping_texts_expected = shaping_output[filename.name]
        except KeyError:
            yield FAIL, f"{shaping_file}: No entry found for {filename.name}"
            return

        if "fvar" in tt:
            shaped_texts = shape_variable(
                tt,
                shaping_texts,
                shaping_script,
                shaping_language,
                shaping_direction,
                shaping_features,
                shaping_comparison_mode,
            )
        else:
            shaped_texts = shape_static(
                tt,
                shaping_texts,
                shaping_script,
                shaping_language,
                shaping_direction,
                shaping_features,
                shaping_comparison_mode,
            )

        if shaped_texts == shaping_texts_expected:
            yield PASS, f"{shaping_file}: No regression detected"
        else:
            shaped_texts_json = json.dumps(shaped_texts, indent=2).split("\n")
            shaping_texts_expected_json = json.dumps(
                shaping_texts_expected, indent=2
            ).split("\n")

            with tempfile.NamedTemporaryFile(
                mode="w+", suffix=".html", delete=False
            ) as f:
                f.write(
                    difflib.HtmlDiff().make_file(
                        shaping_texts_expected_json,
                        shaped_texts_json,
                        f"Expected for {filename.name}",
                        "Actual",
                    )
                )
            yield FAIL, (
                f"{shaping_file}: Expected and actual shaping not matching. "
                f"Open {f.name} in your browser for details."
            )


profile.auto_register(globals())
profile.test_expected_checks(GOOGLESANS_PROFILE_CHECKS, exclusive=True)


# XXX: Below is a copy-pasta of update_shaping_test_data.py because I can't
# seem to import it here.


class ComparisonMode(enum.Enum):
    FULL = "full"  # Record glyph names, offsets and advance widths.
    GLYPHSTREAM = "glyphstream"  # Just glyph names.


class Direction(enum.Enum):
    LTR = "ltr"
    RTL = "rtl"
    TTB = "ttb"
    BTT = "btt"


def shape_text(
    font_path: str,
    text: str,
    script: str,
    language: str,
    direction: Direction,
    features: Dict[str, bool],
    shaping_comparison_mode: ComparisonMode,
    variations: Optional[Dict[str, float]] = None,
) -> List[Dict[str, Any]]:
    with open(font_path, "rb") as fontfile:
        fontdata = fontfile.read()

    face = hb.Face(fontdata)
    font = hb.Font(face)
    upem = face.upem
    if variations is not None:
        font.set_variations(variations)

    font.scale = (upem, upem)
    hb.ot_font_set_funcs(font)

    buf = hb.Buffer()
    buf.add_str(text)
    buf.direction = direction.value
    buf.script = script
    buf.language = language
    buf.guess_segment_properties()
    hb.shape(font, buf, features)

    infos = buf.glyph_infos
    positions = buf.glyph_positions

    if shaping_comparison_mode is ComparisonMode.FULL:
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
    elif shaping_comparison_mode is ComparisonMode.GLYPHSTREAM:
        return [font.get_glyph_name(info.codepoint) for info in infos]
    else:
        raise ValueError(f"Unknown comparison mode {shaping_comparison_mode}.")


def shape_variable(
    font: TTFont,
    texts: List[str],
    script: str,
    language: str,
    direction: Direction,
    features: Dict[str, bool],
    shaping_comparison_mode: ComparisonMode,
) -> Dict[str, List[Dict[str, Any]]]:
    filename = Path(font.reader.file.name)
    fvar = font["fvar"]
    result = {}
    for instance in fvar.instances:
        coordinate_str = ",".join(f"{k}={v}" for k, v in instance.coordinates.items())
        result[coordinate_str] = [
            shape_text(
                filename,
                text,
                script,
                language,
                direction,
                features,
                shaping_comparison_mode,
                instance.coordinates,
            )
            for text in texts
        ]
    return result


def shape_static(
    font: TTFont,
    texts: List[str],
    script: str,
    language: str,
    direction: Direction,
    features: Dict[str, bool],
    shaping_comparison_mode: ComparisonMode,
) -> List[Dict[str, Any]]:
    filename = Path(font.reader.file.name)
    return [
        shape_text(
            filename,
            text,
            script,
            language,
            direction,
            features,
            shaping_comparison_mode,
        )
        for text in texts
    ]
