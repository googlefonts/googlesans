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

# flake8: noqa

import argparse
import sys
from pathlib import Path

from fontTools.subset import main as subset_main
from fontTools.ttLib import TTFont

parser = argparse.ArgumentParser()
parser.add_argument("upright_vf", type=Path)
parser.add_argument("upright_characters", type=Path)
parser.add_argument("italic_vf", type=Path)
parser.add_argument("italic_characters", type=Path)
parser.add_argument("output_dir", type=Path)
parsed_args = parser.parse_args()

# Taken from the v4 fonts.
V4_Y_MIN = -381
V4_Y_MAX = 1056

parsed_args.output_dir.mkdir(parents=True, exist_ok=True)

# Roman subset options
roman_output_filepath = parsed_args.output_dir / parsed_args.upright_vf.name
roman_subset_options = [
    f"{parsed_args.upright_vf}",
    f"--unicodes-file={parsed_args.upright_characters}",
    "--no-ignore-missing-glyphs",
    "--notdef-outline",
    "--layout-features+=c2sc,calt,case,ccmp,dlig,dnom,frac,jalt,liga,lnum,locl,numr,ordn,pnum,sinf,smcp,ss01,ss02,ss03,ss04,ss05,ss06,ss07,ss08,ss09,subs,sups,tnum,kern,mark,mkmk",
    "--layout-scripts=latn,grek,cyrl,hebr",
    "--drop-tables= ",
    "--name-IDs=*",
    "--name-languages=*",
    "--name-legacy",
    "--no-glyph-names",
    "--recalc-bounds",
    "--recalc-average-width",
    f"--output-file={roman_output_filepath}",
]

# Italic subset options
italic_output_filepath = parsed_args.output_dir / parsed_args.italic_vf.name
italic_subset_options = [
    f"{parsed_args.italic_vf}",
    f"--unicodes-file={parsed_args.italic_characters}",
    "--no-ignore-missing-glyphs",
    "--notdef-outline",
    "--layout-features+=c2sc,calt,case,ccmp,dlig,dnom,frac,jalt,liga,lnum,locl,numr,ordn,pnum,sinf,smcp,ss01,ss02,ss04,ss05,ss06,ss07,ss08,ss09,subs,sups,tnum,kern,mark,mkmk",
    "--layout-scripts=latn,grek,cyrl,hebr",
    "--drop-tables= ",
    "--name-IDs=*",
    "--name-languages=*",
    "--name-legacy",
    "--no-glyph-names",
    "--recalc-bounds",
    "--recalc-average-width",
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

    head.yMin = V4_Y_MIN
    head.yMax = V4_Y_MAX

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
