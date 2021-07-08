#!/usr/bin/env python3
# Copyright 2017 The Font Bakery Authors.
# Copyright 2017 The Google Font Tools Authors
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
#
#
# The magic is in two places:
#
# 1. The GASP table. Vern Adams <vern@newtypography.co.uk>
#    suggests it should have value 15 for all sizes.
#
# 2. The PREP table. Raph Levien <firstname.lastname@gmail.com>
#    suggests using his code to turn on 'drop out control'
#    Learn more:
#    https://developer.apple.com/fonts/TrueType-Reference-Manual/RM05/Chap5.html#SCANCTRL
#    https://developer.apple.com/fonts/TrueType-Reference-Manual/RM05/Chap5.html#SCANTYPE
#
# PUSHW_1
#  511
# SCANCTRL
# PUSHB_1
#  4
# SCANTYPE
#
# This script depends on fontTools Python library, available
# in most packaging systems and sf.net/projects/fonttools/
#
# Usage:
#
# $ gftools fix-nonhinting FontIn.ttf FontOut.ttf

"""
Fixes TTF GASP table so that its program
contains the minimal recommended instructions.
"""

import argparse
import logging
import os

from fontTools import ttLib
from fontTools.ttLib.tables import ttProgram


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("fonts", nargs="+")
    parser.add_argument("--verbose", action="store_true")
    parsed_args = parser.parse_args(argv)

    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.WARNING)
    LOGGER = logging.getLogger(__name__)
    if parsed_args.verbose:
        LOGGER.setLevel(logging.INFO)

    for fontpath in parsed_args.fonts:
        fontfile_in = os.path.abspath(fontpath)
        font = ttLib.TTFont(fontfile_in)

        # Save a backup
        backupfont = "{}-backup-fonttools-prep-gasp{}".format(
            fontfile_in[0:-4], fontfile_in[-4:]
        )
        font.save(backupfont)
        LOGGER.info("%s saved.", backupfont)

        # Print the Gasp table
        if "gasp" in font:
            LOGGER.info("GASP was: %s", font["gasp"].gaspRange)
        else:
            LOGGER.info("GASP wasn't there")

        # Print the PREP table
        if "prep" in font:
            old_program = ttProgram.Program.getAssembly(font["prep"].program)
            LOGGER.info("PREP was:\n\t%s", "\n\t".join(old_program))
        else:
            LOGGER.info("PREP wasn't there")

        # Create a new GASP table
        gasp = ttLib.newTable("gasp")

        # Set GASP to the magic number
        gasp.gaspRange = {0xFFFF: 15}

        # Create a new hinting program
        program = ttProgram.Program()

        assembly = ["PUSHW[]", "511", "SCANCTRL[]", "PUSHB[]", "4", "SCANTYPE[]"]
        program.fromAssembly(assembly)

        # Create a new PREP table
        prep = ttLib.newTable("prep")

        # Insert the magic program into it
        prep.program = program

        # Add the tables to the font, replacing existing ones
        font["gasp"] = gasp
        font["prep"] = prep

        # Print the Gasp table
        LOGGER.info("GASP now: %s", font["gasp"].gaspRange)

        # Print the PREP table
        current_program = ttProgram.Program.getAssembly(font["prep"].program)
        LOGGER.info("PREP now:\n\t%s", "\n\t".join(current_program))

        # Save the new file with the name of the input file
        fontfile_out = os.path.abspath(fontpath)
        font.save(fontfile_out)
        LOGGER.info("%s saved.", fontfile_out)


if __name__ == "__main__":
    main()
