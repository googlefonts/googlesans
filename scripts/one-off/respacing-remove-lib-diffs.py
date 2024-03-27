# Copyright 2024 Google Sans Authors
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
This restore each glyph's UFO <lib> to the value from another branch, which
needs to be checked out in the folder named `SOURCE_DIR` below.

The goal is to discard lib key changes from the respacing process.
"""

from __future__ import annotations

from ufoLib2 import Font
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
SOURCE_DIR = ROOT_DIR / "../googlesans-main/source/GoogleSans"
TARGET_DIR = ROOT_DIR / "source/GoogleSans"

ALL_UFOS = [
    "GoogleSans-opsz17-wght380-GRAD0.ufo",
    "GoogleSans-opsz17-wght734-GRAD0.ufo",
    "GoogleSans-opsz18-wght380-GRAD0.ufo",
    "GoogleSans-opsz18-wght734-GRAD0.ufo",
    "GoogleSansItalic-opsz17-wght380-GRAD0.ufo",
    "GoogleSansItalic-opsz17-wght734-GRAD0.ufo",
    "GoogleSansItalic-opsz18-wght380-GRAD0.ufo",
    "GoogleSansItalic-opsz18-wght734-GRAD0.ufo",
    "GoogleSans-opsz17-wght380-GRAD-50.ufo",
    "GoogleSans-opsz17-wght380-GRAD200.ufo",
    "GoogleSans-opsz18-wght380-GRAD-50.ufo",
    "GoogleSans-opsz18-wght380-GRAD200.ufo",
    "GoogleSansItalic-opsz17-wght380-GRAD-50.ufo",
    "GoogleSansItalic-opsz17-wght380-GRAD200.ufo",
    "GoogleSansItalic-opsz18-wght380-GRAD-50.ufo",
    "GoogleSansItalic-opsz18-wght380-GRAD200.ufo",
]


def main():
    for source_ufo_path in (SOURCE_DIR / u for u in ALL_UFOS):
        target_ufo_path = TARGET_DIR / source_ufo_path.name
        source_ufo = Font.open(source_ufo_path)
        target_ufo = Font.open(target_ufo_path)

        for source_glyph in source_ufo:
            if source_glyph.name not in target_ufo:
                continue
            target_glyph = target_ufo[source_glyph.name]
            target_glyph.lib = source_glyph.lib

        target_ufo.save(overwrite=True)


if __name__ == "__main__":
    main()
