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

SCRIPT_VERSION = "v0.5.0"

FONTNAME = "GS"

# Default values
DEFAULT_WEIGHT = 400
DEFAULT_XHEIGHT = 190
DEFAULT_SPACING = 150
DEFAULT_CHARWIDTH = 60
DEFAULT_ASCENDER = 100
DEFAULT_COUNTER = 50

# Min/Max of design axis range values
WEIGHT_MIN = 300
WEIGHT_MAX = 400

XHEIGHT_MIN = 170
XHEIGHT_MAX = 200

SPACING_MIN = 100
SPACING_MAX = 200

CHARWIDTH_MIN = 0
CHARWIDTH_MAX = 200

ASCENDER_MIN = 0
ASCENDER_MAX = 100

COUNTER_MIN = 0
COUNTER_MAX = 100

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
        "--xheight",
        type=int,
        default=DEFAULT_XHEIGHT,
        help="X-height axis value ({}-{})".format(XHEIGHT_MIN, XHEIGHT_MAX),
    )  # opsz
    optionsgroup.add_argument(
        "--spacing",
        type=int,
        default=DEFAULT_SPACING,
        help="Spacing axis value ({}-{})".format(SPACING_MIN, SPACING_MAX),
    )  # ital
    optionsgroup.add_argument(
        "--charwidth",
        type=int,
        default=DEFAULT_CHARWIDTH,
        help="Character width axis value ({}-{})".format(CHARWIDTH_MIN, CHARWIDTH_MAX),
    )  # CUS2
    optionsgroup.add_argument(
        "--ascender",
        type=int,
        default=DEFAULT_ASCENDER,
        help="Ascender height axis value ({}-{})".format(ASCENDER_MIN, ASCENDER_MAX),
    )  # CUS3
    optionsgroup.add_argument(
        "--counter",
        type=int,
        default=DEFAULT_COUNTER,
        help="Counter axis value ({}-{})".format(COUNTER_MIN, COUNTER_MAX),
    )  # CUS4

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
    if args.xheight is not None:
        if args.xheight < XHEIGHT_MIN or args.xheight > XHEIGHT_MAX:
            sys.stderr.write(
                "X-height axis value must be in the range {} - {}{}".format(
                    XHEIGHT_MIN, XHEIGHT_MAX, os.linesep
                )
            )
            sys.exit(1)
        else:
            instance_location["opsz"] = args.xheight
    if args.spacing is not None:
        if args.spacing < SPACING_MIN or args.spacing > SPACING_MAX:
            sys.stderr.write(
                "Spacing axis value must be in the range {} - {}{}".format(
                    SPACING_MIN, SPACING_MAX, os.linesep
                )
            )
            sys.exit(1)
        else:
            instance_location["ital"] = args.spacing
    if args.charwidth is not None:
        if args.charwidth < CHARWIDTH_MIN or args.charwidth > CHARWIDTH_MAX:
            sys.stderr.write(
                "Character width axis value must be in the range {} - {}{}".format(
                    CHARWIDTH_MIN, CHARWIDTH_MAX, os.linesep
                )
            )
            sys.exit(1)
        else:
            instance_location["CUS2"] = args.charwidth
    if args.ascender is not None:
        if args.ascender < ASCENDER_MIN or args.ascender > ASCENDER_MAX:
            sys.stderr.write(
                "Ascender height axis value must be in the range {} - {}{}".format(
                    ASCENDER_MIN, ASCENDER_MAX, os.linesep
                )
            )
            sys.exit(1)
        else:
            instance_location["CUS3"] = args.ascender
    if args.counter is not None:
        if args.counter < COUNTER_MIN or args.counter > COUNTER_MAX:
            sys.stderr.write(
                "Counter axis value must be in the range {} - {}{}".format(
                    COUNTER_MIN, COUNTER_MAX, os.linesep
                )
            )
            sys.exit(1)
        else:
            instance_location["CUS4"] = args.counter

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

    axis_param_string = axis_param_string.replace("wght", "w")
    axis_param_string = axis_param_string.replace("opsz", "x")
    axis_param_string = axis_param_string.replace("ital", "s")
    axis_param_string = axis_param_string.replace("CUS2", "cw")
    axis_param_string = axis_param_string.replace("CUS3", "a")
    axis_param_string = axis_param_string.replace("CUS4", "co")

    # name definitions
    nameID1_name = "GS {}".format(axis_param_string)
    nameID4_name = "GS {} Regular".format(axis_param_string)
    nameID6_name = "GS-{}-Regular".format(axis_param_string)
    outfont_name = "GS-{}-Regular.ttf".format(axis_param_string)
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
