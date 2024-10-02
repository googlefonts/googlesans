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
Aggregate coverage and file size statistics across several TTFs.

Initially developed for comparison of a full VF and a collection of subsets that
aim to reproduce it.
"""

from __future__ import annotations

from argparse import ArgumentParser

from fontTools.ttLib import TTFont


def sum(ttfs: list[TTFont]) -> dict[str, int]:
    glyphs: set[str] = set()
    codepoints: set[int] = set()
    tables: dict[str, int] = {}

    # Include each TTFs contributions to totals.
    for ttf in ttfs:
        glyphs |= set(ttf.getGlyphSet())
        codepoints |= set(ttf["cmap"].getBestCmap())  # type: ignore

        # Same approach for tables as fontsize:
        #     https://github.com/source-foundry/font-size/blob/a8056c559/lib/fontsize/size.py
        tags = [tag for tag in ttf.keys() if tag != "GlyphOrder"]
        for tag in tags:
            tables[tag] = tables.get(tag, 0) + ttf.reader.tables[tag].length  # type: ignore

    # Summarise glyphs and codepoints as counts, and include table bytes too.
    return {
        "glyphs": len(glyphs),
        "codepoints": len(codepoints),
    } | {f"table_{tag}": size for tag, size in tables.items()}


def main():
    parser = ArgumentParser()
    parser.add_argument("ttf", type=TTFont, nargs="+")
    args = parser.parse_args()

    # Collect totals.
    totals = sum(args.ttf)

    # Print as a table.
    for label, count in sorted(totals.items()):
        print(label, count, sep="\t")


if __name__ == "__main__":
    main()
