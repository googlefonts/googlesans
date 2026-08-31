# Copyright 2026 Google Sans Authors
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

"""
fontvi, "the one after font-v".

Adds the Git SHA to the font's version string(s).
"""

from argparse import ArgumentParser
from pathlib import Path

from fontTools.ttLib import TTFont
from git import Repo


def get_git_sha() -> str:
    repo = Repo(search_parent_directories=True)
    return repo.git.rev_parse("--short", "HEAD")


def apply_version(font: TTFont, sha: str) -> None:
    name = font["name"]
    for record in name.names:  # type: ignore
        if record.nameID == 5:
            new_record = record.toStr() + f";[{sha}]"
            print(
                "set name record "
                f"({record.platformID}, {record.platEncID}, {record.langID}) "
                f'to "{new_record}"'
            )
            record.string = record.toStr() + f";[{sha}]"


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "font_path",
        type=Path,
    )
    output = parser.add_mutually_exclusive_group(required=True)
    output.add_argument(
        "-o",
        "--output",
        type=Path,
    )
    output.add_argument(
        "--in-place",
        action="store_true",
    )
    args = parser.parse_args()

    sha = get_git_sha()
    font = TTFont(args.font_path)
    apply_version(font, sha)

    save_to = args.output or args.font_path
    font.save(save_to)
    print(f"saved {save_to}")
