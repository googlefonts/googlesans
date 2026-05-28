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

# dependencies = [
#     "fontspectorapi",
#     "fontTools",
#     "uharfbuzz",
# ]
# ///

import json
import sys
import textwrap
from pathlib import Path

import uharfbuzz
from fontspectorapi import (
    FAIL,
    PASS,
    SKIP,
    CheckStatuses,
    Plugin,
    check,
    plugin_main,
)
from fontTools.ttLib import TTFont

# Make Fontspector able to find the update_shaping_test_data package.
sys.path.append(str(Path(__file__).parent.parent))

from qa.update_shaping_test_data import (  # noqa: E402
    ComparisonMode,
    Direction,
    shape_texts,
)

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
    "fina",
    "frac",
    "half",
    "haln",
    "hist",
    "init",
    "isol",
    "jalt",
    "kern",
    "liga",
    "lnum",
    "locl",
    "mark",
    "medi",
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
    "rtlm",
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
    "zero",
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
    "zero",
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
    "fina",
    "frac",
    "half",
    "haln",
    "hist",
    "init",
    "isol",
    "jalt",
    "kern",
    "liga",
    "lnum",
    "locl",
    "mark",
    "medi",
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
    "rtlm",
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
    "zero",
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
    "zero",
]


@check(
    id="fea/included_features",
    title="Check feature inclusion",
    rationale="Confirms that the font builds contain expected feature tags.",
)
def included_features(font_path: Path) -> CheckStatuses:
    ttf = TTFont(font_path)

    match ("fvar" in ttf, "Italic" in font_path.stem):
        case (False, False):
            expectation = STATIC_UPRIGHT_FEA
        case (False, True):
            expectation = STATIC_ITALICS_FEA
        case (True, False):
            expectation = VAR_UPRIGHT_FEA
        case (True, True):
            expectation = VAR_ITALICS_FEA

    gpos = ttf.get("GPOS")
    gsub = ttf.get("GSUB")

    if gpos is None or gsub is None:
        yield FAIL, "Font must contain a 'GPOS' and 'GSUB' table"
        return

    fea_tags = set()

    for gpos_record in gpos.table.FeatureList.FeatureRecord:  # type: ignore
        fea_tags.add(gpos_record.FeatureTag)

    for gsub_record in gsub.table.FeatureList.FeatureRecord:  # type: ignore
        fea_tags.add(gsub_record.FeatureTag)

    if sorted(fea_tags) == expectation:
        yield PASS, "Font contains the expected feature tags"
    else:
        yield (
            FAIL,
            "Font does not contain the expected feature tags.\n"
            f"Found:{sorted(fea_tags)}\nExpected:{expectation}",
        )


@check(
    id="shaping/regression",
    title="Check feature code behaviour",
    rationale="But does it still shape the same?",
)
def features_regression(font_path: Path) -> CheckStatuses:
    ttf = TTFont(font_path)
    hb_font = uharfbuzz.Face(font_path.read_bytes())  # type: ignore

    if "Google Sans Flex TV" in ttf["name"].getDebugName(1):  # type: ignore
        yield SKIP, "Font is not interesting to check."
        return

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
            shaped_texts_expected = shaping_output[font_path.name]
        except KeyError:
            yield FAIL, f"{shaping_file}: No entry found for {font_path.name}"
            return

        shaped_texts = shape_texts(
            ttf,
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
        elif "fvar" in ttf:
            assert isinstance(shaped_texts, dict)
            assert isinstance(shaped_texts_expected, dict)

            for key, shaped_text in shaped_texts.items():
                try:
                    expected = shaped_texts_expected[key]
                except KeyError as e:
                    yield (
                        FAIL,
                        (
                            f"{shaping_file}: No entry found for {font_path.name}, "
                            f" instance {e}"
                        ),
                    )
                    continue
                if shaped_text == expected:
                    yield PASS, f"{shaping_file}: No regression detected"
                else:
                    shaped_texts_str = textwrap.indent("\n".join(shaped_text), "\t  ")
                    shaped_texts_expected_str = textwrap.indent(
                        "\n".join(expected), "\t  "
                    )
                    yield (
                        FAIL,
                        (
                            f"{shaping_file}: Expected and actual shaping not matching."
                            f"\n\tExpected for {key}:\n"
                            f"{shaped_texts_expected_str}"
                            "\n\tActual:\n"
                            f"{shaped_texts_str}"
                        ),
                    )
        else:
            assert isinstance(shaped_texts, list)
            assert isinstance(shaped_texts_expected, list)

            shaped_texts_str = textwrap.indent("\n".join(shaped_texts), "\t  ")
            shaped_texts_expected_str = textwrap.indent(
                "\n".join(shaped_texts_expected), "\t  "
            )
            yield (
                FAIL,
                (
                    f"{shaping_file}: Expected and actual shaping not matching."
                    "\n\tExpected:\n"
                    f"{shaped_texts_expected_str}"
                    "\n\tActual:\n"
                    f"{shaped_texts_str}"
                ),
            )

    if not shaping_file_found:
        yield SKIP, "No test files found."


def register(plugin: Plugin) -> None:
    plugin.register_simple_profile(
        "gs-fea",
        (included_features, features_regression),
        section_name="Google Sans Custom Feature & Shaping Checks",
    )


if __name__ == "__main__":
    raise SystemExit(plugin_main(register, plugin_name="gs-fea"))
