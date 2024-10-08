#!/usr/bin/env python3

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

# from argparse import ArgumentParser
from pathlib import Path

from ufoLib2 import Font

SUBSET_GROUP_ONE = [
    "LatnTall",
]
SUBSET_GROUP_TWO = [
    "LatnSmall",
]
SHOW_CLASHES = True

SOURCES_PATH = Path(__file__).parent.parent / "source" / "GoogleSans"
SUBSETS_PATH = SOURCES_PATH / "subsets"


def get_all_codepoints(subset_names: list[str]) -> set[int]:
    codepoints = set()
    for subset in subset_names:
        subset_path = SUBSETS_PATH / f"{subset}.txt"
        for line in subset_path.read_text().splitlines():
            if line == "" or line.startswith("#"):
                continue
            hex_str = line.strip("U+")
            try:
                codepoints.add(int(hex_str, 16))
            except ValueError:
                print(f"failed to convert line to codepoint: '{line}'")
    return codepoints


def main():
    assert (
        len(SUBSET_GROUP_ONE) > 0 and len(SUBSET_GROUP_TWO) > 0
    ), "no empty subset groups"

    # Consolidate all subsets into big lists of codepoints
    group_one_codepoints = get_all_codepoints(SUBSET_GROUP_ONE)
    print(
        f"Subsets {SUBSET_GROUP_ONE} have {len(group_one_codepoints)} codepoints total"
    )
    group_two_codepoints = get_all_codepoints(SUBSET_GROUP_TWO)
    print(
        f"Subsets {SUBSET_GROUP_TWO} have {len(group_two_codepoints)} codepoints total"
    )
    assert (
        len(group_one_codepoints & group_two_codepoints) == 0
    ), "overlapping subset groups"

    if not SHOW_CLASHES:
        print("Kerns between the two groups of codepoints:")
    for source_path in sorted(SOURCES_PATH.glob("*.ufo")):
        ufo = Font.open(source_path)

        group_one_names = {
            next(glyph.name for glyph in ufo if codepoint in glyph.unicodes)
            for codepoint in group_one_codepoints
        }
        group_two_names = {
            next(glyph.name for glyph in ufo if codepoint in glyph.unicodes)
            for codepoint in group_two_codepoints
        }
        assert (
            len(group_one_names & group_two_names) == 0
        ), "overlapping glyphs names across groups"

        external_kerns = 0
        for glyph_name in group_one_names:
            left_kern_group = next(
                (
                    group_name
                    for group_name, members in ufo.groups.items()
                    if glyph_name in members and group_name.startswith("public.kern1.")
                ),
                glyph_name,
            )
            right_kern_group = next(
                (
                    group_name
                    for group_name, members in ufo.groups.items()
                    if glyph_name in members and group_name.startswith("public.kern2.")
                ),
                glyph_name,
            )
            for (kern_left, kern_right), value in ufo.kerning.items():
                if kern_left == left_kern_group or kern_left == glyph_name:
                    other_first = False
                    other = kern_right
                elif kern_right == right_kern_group or kern_right == glyph_name:
                    other_first = True
                    other = kern_left
                else:
                    continue

                done = False
                for other_glyph_name in ufo.groups.get(other, [other]):
                    if other_glyph_name not in group_two_names:
                        continue
                    if SHOW_CLASHES and value >= 50:
                        if other_first:
                            print(
                                f"{source_path.stem}: /{other_glyph_name} /{glyph_name} -> {value}"
                            )
                        else:
                            print(
                                f"{source_path.stem}: /{glyph_name} /{other_glyph_name} -> {value}"
                            )
                    external_kerns += 1
                    if not SHOW_CLASHES:
                        done = True
                        break
                if done:
                    break

        if not SHOW_CLASHES:
            print(f"- {source_path.stem}: {external_kerns}")


if __name__ == "__main__":
    main()
