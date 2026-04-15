# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "tomli-w",
# ]
# ///

import json
from pathlib import Path
from typing import Literal, Mapping, Required, TypedDict, cast, overload

import tomli_w
import tomllib

type Direction = Literal["ltr", "rtl"]


class ArabicTestDefinition(TypedDict, total=False):
    input: Required[str]
    note: str
    script: str
    language: str
    direction: Direction
    features: dict[str, bool]


class ArabicTestDefaults(TypedDict, total=False):
    direction: Direction


class ArabicTestConfig(TypedDict):
    defaults: ArabicTestDefaults


class ArabicTestFile(TypedDict, total=False):
    configuration: ArabicTestConfig
    tests: list[ArabicTestDefinition]


class ArabicTestExpectation(TypedDict):
    input: str
    # TTF name (or "default") -> shaped string
    expectation: dict[str, str]


class ArabicTestExpectations(TypedDict):
    tests: list[ArabicTestExpectation]
    # TODO: not handled [configuration]


class GSTestInput(TypedDict, total=False):
    script: str
    language: str
    direction: Literal["ltr", "rtl"]
    comparison_mode: Literal["full", "glyphstream"]
    text: Required[list[str]]
    features: dict[str, bool]


class GSTestFile(TypedDict):
    # TODO: meta
    input: GSTestInput


class GSTestExpectations(TypedDict, total=False):
    input: GSTestInput
    # TTF name -> shaped strings, or for VFs there's a sub-dict for the location
    output: Mapping[str, list[str] | dict[str, list[str]]]


@overload
def remove_none[K, V](obj: dict[K, V | None]) -> dict[K, V]: ...


@overload
def remove_none[V](obj: V) -> V: ...


def remove_none(obj):
    if isinstance(obj, dict):
        return {k: remove_none(v) for k, v in obj.items() if v is not None}
    else:
        return obj


GS_TEST_PATH = Path("qa/shaping_input")
GS_EXPECTATION_PATH = Path("qa/shaping")
ARABIC_TEST_PATH = Path("../Subfamilies/Arabic/qa")

type ScriptLangDirectionFeatures = tuple[
    str | None,
    str | None,
    Direction | None,
    tuple[tuple[str, bool], ...] | None,
]

# Consolidate by script, language, features
grouped_tests: dict[
    ScriptLangDirectionFeatures,
    list[
        tuple[
            # Test string
            str,
            # Expectations
            dict[str, str],
        ]
    ],
] = {}
for test_definition_path in sorted(ARABIC_TEST_PATH.glob("*.toml")):
    test_expectation_path = test_definition_path.with_suffix(".json")
    toml = cast(
        ArabicTestFile, tomllib.loads(test_definition_path.read_text(encoding="utf-8"))
    )

    if "tests" not in toml:
        print(f"Skipped {test_definition_path.name}: no tests")
        continue

    json_expectation = cast(
        ArabicTestExpectations,
        json.loads(test_expectation_path.read_text(encoding="utf-8")),
    )
    expectation_cases = json_expectation["tests"]

    file_direction = None
    if config := toml.get("configuration"):
        if defaults := config.get("defaults"):
            file_direction = defaults.get("direction")

    for test in toml["tests"]:
        if (features := test.get("features")) is not None:
            features_tup = tuple(features.items())
        else:
            features_tup = None

        test_input = test["input"]
        expectation_dict = next(
            test_case["expectation"]
            for test_case in expectation_cases
            if test_case["input"] == test_input
        )

        sldf = (
            test.get("script"),
            test.get("language"),
            test.get("direction", file_direction),
            features_tup,
        )
        grouped_tests.setdefault(sldf, []).append((test_input, expectation_dict))
        if note := test.get("note"):
            # Comments are copied manually as tomli-w doesn't support them
            print(sldf, test["input"], "# " + note)

for (script, language, direction, features), tests in grouped_tests.items():
    strings, expectations = zip(*tests)
    test_input = GSTestInput(
        **remove_none(  # type: ignore
            dict(
                script=script or "arab",
                language=language,
                direction=direction or "rtl",
                features=dict(features) if features else None,
                text=list(strings),
            )
        )
    )

    new_file = GSTestFile(input=test_input)

    expectations_reshaped: dict[str, list[str]] = {
        ttf_name.replace("Arabic", "", 1): [
            expectation_dict.get(ttf_name, "MISSING")
            for expectation_dict in expectations
        ]
        for ttf_name in expectations[0]
    }
    # VF at default location, just disregard it for simplicity as it doesn't
    # match the way GS' expectations are structured
    del expectations_reshaped["default"]

    new_expectations = GSTestExpectations(
        input=test_input, output=expectations_reshaped
    )
    name_parts = [
        script,
        language,
        direction or "rtl",
        *[feature_name for feature_name, enabled in (features or []) if enabled],
    ]
    name_suffix = "-".join(part for part in name_parts if part is not None)
    file_name = f"arabic-{name_suffix}.toml"
    new_toml_path = GS_TEST_PATH / file_name
    # tomli-w doesn't support None values, prune them
    new_toml_path.write_text(tomli_w.dumps(new_file), encoding="utf-8")
    print(f"Wrote {new_toml_path.name}")
    new_json_path = GS_EXPECTATION_PATH / f"{new_toml_path.stem}.json"
    new_json_path.write_text(
        json.dumps(new_expectations, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Wrote {new_json_path.name}")
