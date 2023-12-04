# Copyright 2022 Google Sans Authors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Remove variable font instances that are not in the default position on the
optical sizing axis.

This is a workaround for Figma: if it identifies such instances, it will not
enable automatic optical sizing by default.
"""

from argparse import ArgumentParser
from pathlib import Path
from typing import Any

from fontTools.ttLib import TTFont  # pyright: ignore

FVAR_TABLE_NAME = "fvar"
OPTICAL_SIZE_TAG = "opsz"


def remove_non_default(ttf: TTFont) -> None:
    fvar: Any = ttf[FVAR_TABLE_NAME]

    # Get default optical size.
    for axis in fvar.axes:
        if axis.axisTag == OPTICAL_SIZE_TAG:
            default_opsz = axis.defaultValue
            break
    else:
        raise ValueError("Font has no 'opsz' axis")

    # Only keep instances that are at the default optical size.
    fvar.instances = [
        instance
        for instance in fvar.instances
        if instance.coordinates[OPTICAL_SIZE_TAG] == default_opsz
    ]

    # Modifications have been performed in-place.
    return


def main():
    # Parse arguments.
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("ttf", type=Path, help="Path to variable TTF.")
    parser.add_argument(
        "-o", "--output", type=Path, help="Path to write patched TTF to."
    )
    args = parser.parse_args()

    # Patch provided fonts, and write out.
    with TTFont(args.ttf) as ttf:
        remove_non_default(ttf)
        ttf.save(  # pyright: ignore
            args.output if args.output is not None else args.ttf
        )


if __name__ == "__main__":
    main()
