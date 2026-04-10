# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "tomli-w",
# ]
# ///

from pathlib import Path
from typing import Literal, Required, TypedDict, cast, overload

import tomli_w
import tomllib


class ArabicTestDefinition(TypedDict, total=False):
    input: Required[str]
    note: str
    script: str
    language: str
    features: dict[str, bool]


class ArabicTestFile(TypedDict, total=False):
    # TODO: not handled [configuration.defaults]
    tests: list[ArabicTestDefinition]


class GSTestInput(TypedDict, total=False):
    script: str
    language: str
    comparison_mode: Literal["full", "glyphstream"]
    text: Required[list[str]]
    features: dict[str, bool]


class GSTestFile(TypedDict):
    # TODO: meta
    input: GSTestInput


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
ARABIC_TEST_PATH = Path("../Subfamilies/Arabic/qa")

# Consolidate tests by script, language, features
grouped_tests: dict[
    tuple[str | None, str | None, tuple[tuple[str, bool], ...] | None],
    list[str],
] = {}
for test_definition_path in ARABIC_TEST_PATH.glob("*.toml"):
    toml = cast(
        ArabicTestFile, tomllib.loads(test_definition_path.read_text(encoding="utf-8"))
    )

    if "tests" not in toml:
        print(f"Skipped {test_definition_path.name}: no tests")
        continue

    for test in toml["tests"]:
        if (features := test.get("features")) is not None:
            features_tup = tuple(features.items())
        else:
            features_tup = None

        key = (test.get("script"), test.get("language"), features_tup)
        grouped_tests.setdefault(
            key, []
        ).append(test["input"])
        if note := test.get("note"):
            # Comments are copied manually as tomli-w doesn't support them
            print(key, test["input"], "# " + note)

for (script, language, features), strings in grouped_tests.items():
    new_file = GSTestFile(
        input=GSTestInput(
            **remove_none(  # type: ignore
                dict(
                    script=script,
                    language=language,
                    text=strings,
                    features=dict(features) if features is not None else None,
                )
            )
        )
    )
    name_parts = [
        script,
        language,
        *[feature_name for feature_name, enabled in (features or []) if enabled],
    ]
    name_suffix = "-".join(part for part in name_parts if part is not None)
    if name_suffix != "":
        file_name = f"arabic-{name_suffix}.toml"
    else:
        file_name = "arabic.toml"
    new_file_path = GS_TEST_PATH / file_name
    # tomli-w doesn't support None values, prune them
    new_file_path.write_text(tomli_w.dumps(remove_none(new_file)), encoding="utf-8")
    print(f"Wrote {new_file_path.name}")
