#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ========================================================
# vf2s-gui.py
# Copyright 2019 Google, LLC
# Apache License, v2.0
#
# A variable font to static font instance generator
# + unique name table writer for the Google Sans typeface
# This script supports a Gooey Python library GUI
#
# Dependencies: fontTools, Gooey (both available on PyPI)
# Usage: python3 vf2s-gui.py
#
# =======================================================

# PyInstaller build for macOS architecture
#
# pyinstaller -c --onefile --hidden-import=fontTools --clean --distpath="dist/macos64" -n vf2s vf2s.py

import os
import sys

from fontTools.ttLib import TTFont
from fontTools.varLib.mutator import instantiateVariableFont

from gooey import Gooey, GooeyParser

SCRIPT_VERSION = "v0.6.0"

FONTNAME = "GS"

# Default values
DEFAULT_WEIGHT = 400
DEFAULT_WIDTH = 300
FIXED_OPSZ = 14

# Min/Max of design axis range values
WEIGHT_MIN = 380
WEIGHT_MAX = 734

WIDTH_MIN = 0
WIDTH_MAX = 400

OPSZ_MIN = 14
OPSZ_MAX = 24

# macOS rendering bit
# used for workaround fix for fontTools varLib.mutator bug
MAC_OVERLAP_RENDERING_BIT = 1 << 6


def set_mac_overlap_rendering_bit(font):
    """Sets the bit6 macOS overlap rendering bit."""
    glyf = font["glyf"]
    for glyph_name in glyf.keys():
        glyph = glyf[glyph_name]
        # Only needs to be set for glyphs with contours
        if glyph.numberOfContours > 0:
            glyph.flags[0] |= MAC_OVERLAP_RENDERING_BIT
    return font


@Gooey(
    program_name="vf2s",
    description="A variable font to static instance generator for Google Sans.",
    default_size=(600, 600),
    show_success_modal=False,
)
def main():
    parser = GooeyParser(
        description="A variable font to static instance generator for Google Sans."
    )
    filegroup = parser.add_argument_group("Variable Font")
    filegroup.add_argument(
        "path", widget="FileChooser", help="Path to the variable font file"
    )

    optionsgroup = parser.add_argument_group("Design Axes")
    optionsgroup.add_argument(
        "--weight",
        type=int,
        default=DEFAULT_WEIGHT,
        help="Weight axis value ({}-{})".format(WEIGHT_MIN, WEIGHT_MAX),
    )  # wght
    optionsgroup.add_argument(
        "--width",
        type=int,
        default=DEFAULT_WIDTH,
        help="Width axis value ({}-{})".format(WIDTH_MIN, WIDTH_MAX),
    )  # wght

    args = parser.parse_args()

    instance_location = {}
    # axis value validity testing and location definitions
    if args.weight is not None:
        if args.weight < WEIGHT_MIN or args.weight > WEIGHT_MAX:
            sys.stderr.write(
                "Weight axis value must be in the range {} - {}{}".format(
                    WEIGHT_MIN, WEIGHT_MAX, os.linesep
                )
            )
            sys.exit(1)
        else:
            instance_location["wght"] = args.weight
    if args.width is not None:
        if args.width < WIDTH_MIN or args.width > WIDTH_MAX:
            sys.stderr.write(
                "Width axis value must be in the range {} - {}{}".format(
                    WIDTH_MIN, WIDTH_MAX, os.linesep
                )
            )
            sys.exit(1)
        else:
            instance_location["wdth"] = args.width
    
    # define opsz axis with fixed value as per discussion with Edd Harrington
    #  Note that the opsz axis is actually defined using the slnt axis due to technical issues
    #  with the build engineering
    if FIXED_OPSZ < OPSZ_MIN or FIXED_OPSZ > OPSZ_MAX:
        sys.stderr.write(
                "Optical size axis value must be in the range {} - {}{}".format(
                    OPSZ_MIN, OPSZ_MAX, os.linesep
                )
            )
        sys.exit(1)
    else:
        instance_location["slnt"] = FIXED_OPSZ

    # variable font path check
    if not os.path.exists(args.path):
        sys.stderr.write(
            "Failed. {} does not appear to be a valid path to a variable font{}".format(
                args.path, os.linesep
            )
        )
        sys.exit(1)

    # instantiate the variable font with the requested values
    font = TTFont(args.path)
    instantiateVariableFont(font, instance_location, inplace=True)

    # ---------------------------------------------------------------
    # rewrite name table records with new name values for A/B testing
    # ---------------------------------------------------------------

    namerecord_list = font["name"].names

    # create a name string from the axis location parameters
    axis_param_string = ""
    for axis_value in instance_location:
        axis_param_string += "{}{}".format(axis_value, instance_location[axis_value])

    axis_param_string = axis_param_string.replace("wght", "wt")
    axis_param_string = axis_param_string.replace("wdth", "wd")
    axis_param_string = axis_param_string.replace("slnt", "op")

    # name definitions
    # note: removed the weight name as of v0.6.0
    nameID1_name = "GS {}".format(axis_param_string)
    nameID4_name = "GS {}".format(axis_param_string)
    nameID6_name = "GS-{}".format(axis_param_string)
    outfont_name = "GS-{}.ttf".format(axis_param_string)
    outfont_path = os.path.join(
        os.path.dirname(os.path.abspath(args.path)), outfont_name
    )

    for record in namerecord_list:
        if record.nameID == 1:
            record.string = nameID1_name
        elif record.nameID == 4:
            record.string = nameID4_name
        elif record.nameID == 6:
            record.string = nameID6_name

    # Set the macOS overlap rendering bit
    # addresses bug in overlap path rendering on macOS web browsers
    # see https://github.com/Colophon-Foundry/google-sans/pull/39#issuecomment-463152268
    font = set_mac_overlap_rendering_bit(font)

    # write the instance font to disk
    try:
        font.save(outfont_path)
        print("[New instance]: {}".format(outfont_path))
    except Exception as e:
        sys.stderr.write(
            "Failed to write font file {} with error: {}{}".format(
                outfont_name, str(e), os.linesep
            )
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
