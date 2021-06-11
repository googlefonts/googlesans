# Copyright 2021 Google Sans Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tool to help evaluate spacing and kerning changes in Google Sans binaries.

Prints a command line for https://github.com/sharkdp/hyperfine for the actual testing.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, List, Set

from fontTools.ttLib.ttFont import TTFont

from . import TEST_LOCATIONS, filter_all_code_points_covered, get_sentences_and_words


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("reference_font", type=TTFont, help="Path to reference TTF.")
    parser.add_argument(
        "fonts",
        type=TTFont,
        nargs="+",
        help="Path to TTFs to measure against the reference.",
    )
    parsed_args = parser.parse_args()
    reference: TTFont = parsed_args.reference_font
    fonts: List[TTFont] = parsed_args.fonts

    if not Path("sentences.txt").exists():
        all_sentences, _ = get_sentences_and_words()
        code_points = get_code_points(reference)
        sentences = filter_all_code_points_covered(code_points, all_sentences)

        with open("sentences.txt", "w") as f:
            f.write("\n".join(s.strip() for s in sentences))

    hyperfine_cmd = "hyperfine --warmup 1 --min-runs 2 {cmds}"
    cmd_line = 'hb-shape --text-file sentences.txt -n 100 -O "" -o /dev/null --variations {variations} "{font}"'
    for location in TEST_LOCATIONS:
        variations = ",".join(f"{k}={v}" for k, v in location.location)
        cmd_lines = [
            cmd_line.format(variations=variations, font=reference.reader.file.name)
        ]
        for font in fonts:
            cmd_lines.append(
                cmd_line.format(variations=variations, font=font.reader.file.name)
            )

        print(hyperfine_cmd.format(cmds=" ".join(f"'{cmd}'" for cmd in cmd_lines)))


class DummyDesignspace:
    """Placeholder for use when we don't care about source level changes."""

    @property
    def sources(self) -> List[Any]:
        return []


def get_code_points(font: TTFont) -> Set[int]:
    return set(font.getBestCmap())


if __name__ == "__main__":
    main()
