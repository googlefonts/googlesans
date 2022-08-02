# Copyright 2021 Google Sans Authors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pyright: strict

"""Provide an easy way to convert test strings - copy-pasted from a test
document - into TOML files."""

from __future__ import annotations

import copy
import re
import string
from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path
from typing import Any

import tomli_w

TEMPLATE: dict[str, Any] = {
    "meta": {"build_commit": ""},
    "input": {
        "script": None,
        "language": "dflt",
        "comparison_mode": "full",
        "text": None,
    },
}


def load_inputs_from_text(text: str) -> defaultdict[str, list[str]]:
    """Parse a test file with non-Latin test strings listed under Latin category names."""
    test_sections: defaultdict[str, list[str]] = defaultdict(list)
    last_heading = None
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        # Crude check; for our test files, the header can be identified by its Latin script
        if line[0] in string.ascii_letters:
            last_heading = line
        else:
            assert last_heading is not None
            test_sections[last_heading].append(line)
    return test_sections


def make_shaping_input(test_strings: list[str], script: str):
    """Create a shaping input TOML from a list of test strings and script."""
    new_dict = copy.deepcopy(TEMPLATE)
    new_dict["input"]["text"] = test_strings
    if script == "odia":
        new_dict["input"]["script"] = "ory2"
    else:
        raise NotImplemented("Only the script tag of the 'odia' language is known")
    return new_dict


def get_file_name(
    category_name: str,
    script: str,
    language: str = "default",
    prefix: str | None = None,
) -> str:
    """Get the file name of a shaping input TOML based on its script, language, and scope."""
    lower_name = category_name.lower()
    swapped_and = lower_name.replace("&", "and")
    name_parts = re.split("[ -]", swapped_and)
    if prefix is not None:
        name_parts = [prefix, *name_parts]
    joined = "_".join([script, language, *name_parts])
    return joined + ".toml"


def convert_to_toml(text_file: Path, script: str, prefix: str | None = None):
    """Convert headed lines of test strings into a TOML shaping input file."""
    test_text = text_file.read_text()
    test_sections = load_inputs_from_text(test_text)

    for category, test_strings in test_sections.items():
        output_path = Path("./qa/shaping_input") / get_file_name(
            category, script, prefix=prefix
        )
        shaping_input = make_shaping_input(test_strings, script)
        output_path.write_text(tomli_w.dumps(shaping_input))


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        "text_tests",
        type=Path,
        help="Text file to parse test categories and strings from",
    )

    parser.add_argument(
        "--script", type=str, help="Name of script that the test strings are for"
    )

    parser.add_argument(
        "--prefix",
        type=str,
        help="An extra tag to begin the file name, beyond script and language",
    )

    args = parser.parse_args()

    convert_to_toml(args.text_tests, args.script, prefix=args.prefix)
