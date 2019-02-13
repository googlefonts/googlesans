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

import os
import sys
import argparse

from fontTools.ttLib import TTFont
from fontTools.varLib.mutator import instantiateVariableFont

from gooey import Gooey, GooeyParser

SCRIPT_VERSION = "v0.3.0"

FONTNAME = "GS"

@Gooey(
    program_name="vf2s",
    description="A variable font to static instance generator for Google Sans.",
    default_size=(600,600),
    show_success_modal=False,
)
def main():
    parser = GooeyParser(
        description="A variable font to static instance generator for Google Sans."
    )
    filegroup = parser.add_argument_group("Variable Font")
    filegroup.add_argument("path", widget="FileChooser", help="Path to the variable font file")
    
    optionsgroup = parser.add_argument_group("Design Axes")
    optionsgroup.add_argument(
        "--weight", type=int, help="Weight axis value (300-400)"
    )  # wght
    optionsgroup.add_argument(
        "--xheight", type=int, help="xheight Axis Value (170-200)"
    )  # opsz
    optionsgroup.add_argument(
        "--spacing", type=int, help="Spacing Axis Value (100-200)"
    )  # ital
    optionsgroup.add_argument(
        "--charwidth", type=int, help="Character Width Axis Value (0-100-200)"
    )  # CUS2
    optionsgroup.add_argument(
        "--ascender", type=int, help="Ascender Axis Value (0-100)"
    )  # CUS3
    optionsgroup.add_argument(
        "--counter", type=int, help="Counter Axis Value (0-100)"
    )  # CUS4


    args = parser.parse_args()

    instance_location = {}
    # axis value validity testing and location definitions
    if args.weight is not None:
        if args.weight < 300 or args.weight > 400:
            sys.stderr.write(
                "Failed. Weight axis value must be in the range 300 - 400.{}".format(os.linesep)
            )
            sys.exit(1)
        else:
            instance_location["wght"] = args.weight
    if args.xheight is not None:
        if args.xheight < 170 or args.xheight > 200:
            sys.stderr.write(
                "Failed. X-height axis value must be in the range 170 - 200{}".format(
                    os.linesep
                )
            )
            sys.exit(1)
        else:
            instance_location["opsz"] = args.xheight
    if args.spacing is not None:
        if args.spacing < 100 or args.spacing > 200:
            sys.stderr.write(
                "Failed. Spacing axis value must be in the range 100 - 200{}".format(os.linesep)
            )
            sys.exit(1)
        else:
            instance_location["ital"] = args.spacing
    if args.charwidth is not None:
        if args.charwidth < 0 or args.charwidth > 200:
            sys.stderr.write(
                "Failed. Character width axis value must be 0, 100, or 200{}".format(os.linesep)
            )
            sys.exit(1)
        else:
            instance_location["CUS2"] = args.charwidth
    if args.ascender is not None:
        if args.ascender < 0 or args.ascender > 100:
            sys.stderr.write(
                "Failed. Ascender height axis value must be in the range 0 - 100{}".format(
                    os.linesep
                )
            )
            sys.exit(1)
        else:
            instance_location["CUS3"] = args.ascender
    if args.counter is not None:
        if args.counter < 0 or args.counter > 100:
            sys.stderr.write(
                "Failed. Counter axis value must be in the range 0 - 100{}".format(os.linesep)
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
