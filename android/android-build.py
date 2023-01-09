# flake8: noqa
# Copyright 2023 Google Sans Authors
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

"""Defines the Android release build target for the Google Sans family
variable fonts."""

import sys
from pathlib import Path

from fontTools.subset import main as subset_main
from fontTools.ttLib import TTFont


def run():
    # ==================================================
    # v10.001 definitions
    # ==================================================

    # input file path definitions for subsetting
    v10_roman_input_filepath = Path("v10/GoogleSans[GRAD,opsz,wght].ttf")
    v10_italic_input_filepath = Path("v10/GoogleSans-Italic[GRAD,opsz,wght].ttf")

    # Android subset output file path definitions
    # these are the target production files
    roman_output_filepath = "GoogleSans-Android.ttf"
    italic_output_filepath = "GoogleSans-Android-Italic.ttf"

    # ==================================================
    # v4.000 definitions
    # ==================================================

    # input filepaths
    v4_roman_fontpath = Path("v4/GoogleSans[GRAD,opsz,wght].ttf")
    v4_italic_fontpath = Path("v4/GoogleSans-Italic[GRAD,opsz,wght].ttf")

    # TTFont instantiation
    v4_roman_tt = TTFont(v4_roman_fontpath)
    v4_italic_tt = TTFont(v4_italic_fontpath)

    # define the v4.000 target yMin and yMax metrics
    # we are intentionally mocking the values here to address an Android-
    # specific metrics issue)
    v4_head = v4_roman_tt["head"]
    v4_y_min = v4_head.yMin
    v4_y_max = v4_head.yMax

    # ==================================================
    # Encoded glyph list generation
    # ==================================================

    # local Roman and Italic encoded glyph set definition file paths
    roman_glyph_list_path = Path("roman_subset_glyph_list.txt")
    italic_glyph_list_path = Path("italic_subset_glyph_list.txt")

    # define the subset glyph list from the v4.000 build
    define_subset_glyph_list(v4_roman_tt, roman_glyph_list_path)
    define_subset_glyph_list(v4_italic_tt, italic_glyph_list_path)

    # ==================================================
    # fonttools subsetter options
    # ==================================================

    # Roman subset options
    roman_subset_options = [
        f"{v10_roman_input_filepath}",
        f"--unicodes-file={roman_glyph_list_path}",
        "--no-ignore-missing-glyphs",
        "--notdef-outline",
        "--layout-features+=c2sc,calt,case,ccmp,dlig,dnom,frac,jalt,liga,lnum,locl,numr,ordn,pnum,sinf,smcp,ss01,ss02,ss03,ss04,ss05,ss06,ss07,ss08,ss09,subs,sups,tnum,kern,mark,mkmk",
        "--drop-tables= ",
        "--name-IDs=*",
        "--name-languages=*",
        "--name-legacy",
        "--glyph-names",
        "--recalc-bounds",
        f"--output-file={roman_output_filepath}",
    ]

    # Italic subset options
    italic_subset_options = [
        f"{v10_italic_input_filepath}",
        f"--unicodes-file={italic_glyph_list_path}",
        "--no-ignore-missing-glyphs",
        "--notdef-outline",
        "--layout-features+=c2sc,calt,case,ccmp,dlig,dnom,frac,jalt,liga,lnum,locl,numr,ordn,pnum,sinf,smcp,ss01,ss02,ss04,ss05,ss06,ss07,ss08,ss09,subs,sups,tnum,kern,mark,mkmk",
        "--drop-tables= ",
        "--name-IDs=*",
        "--name-languages=*",
        "--name-legacy",
        "--glyph-names",
        "--recalc-bounds",
        f"--output-file={italic_output_filepath}",
    ]

    # ==================================================
    # Execute binary edits
    # ==================================================

    # Subset fonts
    for options in [roman_subset_options, italic_subset_options]:
        try:
            subset_main(options)
            print(f"Subset of '{options[0]}' complete")
        except Exception as e:
            sys.stderr.write(
                f"ERROR: subsetting error during attempt to subset {options[0]}: {e}"
            )
            sys.exit(1)

    # 1. Edit metrics in the subset fonts:
    # - yMin and yMax metrics in the subset fonts to the v4.000 values
    # - Win Ascent and Win Descent metrics to actual y-min and -max values from compiler
    # 2. Edit name table record ID5 to include "Android build"
    for fontpath in [roman_output_filepath, italic_output_filepath]:
        tt = TTFont(fontpath, recalcBBoxes=False)
        head = tt["head"]
        os2 = tt["OS/2"]

        os2.usWinAscent = head.yMax + 1
        os2.usWinDescent = abs(head.yMin) + 1

        head.yMin = v4_y_min
        head.yMax = v4_y_max

        for record in tt["name"].names:
            if record.nameID == 5:
                version_record_string = record.toUnicode()
                version_record_string += ";Android build"
                record.string = version_record_string

        tt.save(fontpath)
        print(
            f"Metrics updated to: yMin={head.yMin}, yMax={head.yMax}, "
            f"winDescent={os2.usWinDescent}, winAscent={os2.usWinAscent} in {fontpath}"
        )


def define_subset_glyph_list(target_tt, outpath):
    # Define a list of glyphs to be included in the subset from Google Sans v4.000
    cmap = target_tt.getBestCmap()
    uni_list_raw = list(cmap.keys())
    uni_list = []

    # new glyphs that were added in
    # https://github.com/googlefonts/googlesans/pull/517
    add_list = [
        "0181",  # LATIN CAPITAL LETTER B WITH HOOK
        "0253",  # LATIN SMALL LETTER B WITH HOOK
        "018A",  # LATIN CAPITAL LETTER D WITH HOOK
        "0257",  # LATIN SMALL LETTER D WITH HOOK
        "0190",  # LATIN CAPITAL LETTER OPEN E
        "025B",  # LATIN SMALL LETTER OPEN E
        "24BC",  # CIRCLED LATIN CAPITAL LETTER G
        "0132",  # LATIN CAPITAL LIGATURE IJ
        "0133",  # LATIN SMALL LIGATURE IJ
        "0198",  # LATIN CAPITAL LETTER K WITH HOOK
        "0199",  # LATIN SMALL LETTER K WITH HOOK
        "0186",  # LATIN CAPITAL LETTER OPEN O
        "0254",  # LATIN SMALL LETTER OPEN O
        "018F",  # LATIN CAPITAL LETTER SCHWA
        "1E62",  # LATIN CAPITAL LETTER S WITH DOT BELOW
        "1E63",  # LATIN SMALL LETTER S WITH DOT BELOW
        "01B3",  # LATIN CAPITAL LETTER Y WITH HOOK
        "01B4",  # LATIN SMALL LETTER Y WITH HOOK
        "25CC",  # DOTTED CIRCLE (for combining diacritics) - fontbakery fail
    ]

    # format code point values as hexadecimal number
    # code point number strings and append to uni_list
    for codepoint_int in uni_list_raw:
        uni_list.append(f"{codepoint_int:0x}")

    # append new encoded code point strings from
    # https://github.com/googlefonts/googlesans/pull/517 to uni_list
    for codepoint_str in add_list:
        uni_list.append(codepoint_str)

    # write to local comma-delimited files for use by fonttools
    with open(outpath, "w") as f:
        for uni in uni_list:
            f.write(f"{uni},")


if __name__ == "__main__":
    run()
