#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ========================================================
# vf2s.py
# Copyright 2019 Google, LLC
# Apache License, v2.0
#
# A variable font to static font instance generator
# + unique name table writer for the Google Sans typeface
# =======================================================

import os
import sys
import argparse

from fontTools.ttLib import TTFont
from fontTools.varLib.mutator import instantiateVariableFont

SCRIPT_VERSION = "v0.1.0"

FONTNAME = "GS"

# PyInstaller build
#
# pyinstaller -c --onefile --hidden-import=fontTools --clean --distpath="dist/macos64" -n vf2s vf2s.py
#


def main():
    parser = argparse.ArgumentParser(
        description="A variable font to static instance generator for Google Sans."
    )
    parser.add_argument(
        "--weight", type=int, help="Weight axis value (300-400)"
    )  # wght
    parser.add_argument(
        "--xheight", type=int, help="X-height axis value (170-200)"
    )  # opsz
    parser.add_argument(
        "--spacing", type=int, help="Spacing axis value (100-200)"
    )  # ital
    parser.add_argument(
        "--charwidth", type=int, help="Character width axis value (0-100-200)"
    )  # CUS2
    parser.add_argument(
        "--ascender", type=int, help="Ascender height axis value (0-100)"
    )  # CUS3
    parser.add_argument(
        "--counter", type=int, help="Counter axis value (0-100)"
    )  # CUS4
    parser.add_argument(
        "--version", action="version", version="vf2s {}".format(SCRIPT_VERSION)
    )
    parser.add_argument("path", help="Variable font path")

    args = parser.parse_args()

    # Version string
    if args.version:
        print("vf2s {}".format(SCRIPT_VERSION))
        sys.exit(0)

    instance_location = {}
    # axis value validity testing and location definitions
    if args.weight:
        if args.weight < 300 or args.weight > 400:
            sys.stderr.write(
                "Weight axis value must be in the range 300 - 400{}".format(os.linesep)
            )
            sys.exit(1)
        else:
            instance_location["wght"] = args.weight
    if args.xheight:
        if args.xheight < 170 or args.xheight > 200:
            sys.stderr.write(
                "X-height axis value must be in the range 170 - 200{}".format(
                    os.linesep
                )
            )
            sys.exit(1)
        else:
            instance_location["opsz"] = args.xheight
    if args.spacing:
        if args.spacing < 100 or args.spacing > 200:
            sys.stderr.write(
                "Spacing axis value must be in the range 100 - 200{}".format(os.linesep)
            )
            sys.exit(1)
        else:
            instance_location["ital"] = args.spacing
    if args.charwidth:
        if args.charwidth < 0 or args.charwidth > 200:
            sys.stderr.write(
                "Character width axis value must be 0, 100, or 200{}".format(os.linesep)
            )
            sys.exit(1)
        else:
            instance_location["CUS2"] = args.charwidth
    if args.ascender:
        if args.ascender < 0 or args.ascender > 100:
            sys.stderr.write(
                "Ascender height axis value must be in the range 0 - 100{}".format(
                    os.linesep
                )
            )
            sys.exit(1)
        else:
            instance_location["CUS3"] = args.ascender
    if args.counter:
        if args.counter < 0 or args.counter > 100:
            sys.stderr.write(
                "Counter axis value must be in the range 0 - 100{}".format(os.linesep)
            )
            sys.exit(1)
        else:
            instance_location["CUS4"] = args.counter

    # variable font path check
    if not os.path.exists(args.path):
        sys.stderr.write(
            "{} does not appear to be a valid path to a variable font{}".format(
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
