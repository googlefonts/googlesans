#!/usr/bin/env python3
# Copyright 2020 Google Sans Authors
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

import argparse
import logging
import sys
from pathlib import Path

from fontTools.designspaceLib import DesignSpaceDocument, InstanceDescriptor
from fontTools.misc.fixedTools import otRound
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import main as instancer_main

from internal.clean_font import main as main_clean_font

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("font_source", type=Path, help="Font to cut instance from.")
    parser.add_argument("font_target", type=Path, help="Path to save output.")
    parser.add_argument(
        "designspace",
        type=DesignSpaceDocument.fromfile,
        help="Source Designspace.",
    )
    parsed_args = parser.parse_args()
    font_source: Path = parsed_args.font_source
    font_target: Path = parsed_args.font_target
    designspace: DesignSpaceDocument = parsed_args.designspace

    # Take the instance location from the instance with the same filename stem.
    instance: InstanceDescriptor = next(
        (i for i in designspace.instances if Path(i.filename).stem == font_target.stem),
        None,
    )
    if instance is None:
        logging.error(
            "Cannot find instance information for '%s', output filename and "
            "Designspace instance filename must have the same stem.",
            font_target.stem,
        )
        sys.exit(1)
    axes = {a.name: a for a in designspace.axes}
    instance_location_args = [
        f"{axes[k].tag}={axes[k].map_backward(v)}" for k, v in instance.location.items()
    ]

    instancer_args = [
        "--quiet",
        f"--output={str(font_target)}",
        "--remove-overlaps",
        "--update-name-table",
        str(font_source),
        *instance_location_args,
    ]

    try:
        instancer_main(instancer_args)
    except Exception as e:
        logging.error(f"Failed to cut instance: {str(e)}")
        sys.exit(1)

    # Post-processing:
    font = TTFont(font_target)

    # 1. Set OS/2.fsSelection:
    os2 = font["OS/2"]
    head = font["head"]
    if instance.styleMapStyleName == "bold":
        os2.fsSelection &= ~0b1000000
        os2.fsSelection |= 0b100000
        head.macStyle |= 0b1
    elif instance.styleMapStyleName == "bold italic":
        os2.fsSelection &= ~0b1000000
        os2.fsSelection |= 0b100001
        head.macStyle |= 0b11
    elif instance.styleMapStyleName == "italic":
        os2.fsSelection &= ~0b1000000
        os2.fsSelection |= 0b1
        head.macStyle |= 0b10

    # 2. Recompute xAvgCharWidth
    hmtx = font.get("hmtx")
    if hmtx is not None:
        widths = [width for width, _ in hmtx.metrics.values() if width > 0]
        if widths:
            os2.xAvgCharWidth = otRound(sum(widths) / len(widths))

    font.save(font_target)

    # 3. Subset again
    main_clean_font([str(font_target)])
