#!/usr/bin/env python3
# Copyright 2020 Google Sans Authors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import logging
from pathlib import Path

from fontTools.otlLib.builder import buildStatTable
from fontTools.ttLib import TTFont

UPRIGHT_AXES = [
    dict(
        tag="opsz",
        name="Optical Size",
        ordering=0,
        values=[
            dict(
                rangeMinValue=18, nominalValue=18, name="Max", flags=0x2
            ),  # Max opsz, use elided name of "Google Sans" without opsz identifier
            dict(
                rangeMinValue=6, nominalValue=17, rangeMaxValue=17, name="Text"
            ),  # Text
        ],
    ),
    dict(
        tag="wght",
        name="Weight",
        ordering=1,
        values=[
            dict(value=400, name="Regular", flags=0x2),  # Regular
            dict(value=500, name="Medium"),  # Medium
            dict(value=700, name="Bold"),  # Bold
        ],
    ),
    {
        "tag": "GRAD",
        "name": "Grade",
        "ordering": 2,
        "values": [
            {"value": -50, "name": "Grade-50"},
            {"value": 0, "name": "0", "flags": 0x2},
            {"value": 200, "name": "Grade200"},
        ],
    },
    dict(
        tag="ital",
        name="Italic",
        ordering=3,
        values=[dict(value=0, name="Regular", flags=0x2, linkedValue=1)],  # Regular
    ),
]

ITALIC_AXES = [
    dict(
        tag="opsz",
        name="Optical Size",
        ordering=0,
        values=[
            dict(
                rangeMinValue=18, nominalValue=18, name="Max", flags=0x2
            ),  # Max opsz, use elided name of "Google Sans" without opsz identifier
            dict(
                rangeMinValue=6, nominalValue=17, rangeMaxValue=17, name="Text"
            ),  # Text
        ],
    ),
    dict(
        tag="wght",
        name="Weight",
        ordering=1,
        values=[
            dict(value=400, name="Regular", flags=0x2),  # Regular
            dict(value=500, name="Medium"),  # Medium
            dict(value=700, name="Bold"),  # Bold
        ],
    ),
    {
        "tag": "GRAD",
        "name": "Grade",
        "ordering": 2,
        "values": [
            {"value": -50, "name": "Grade-50"},
            {"value": 0, "name": "0", "flags": 0x2},
            {"value": 200, "name": "Grade200"},
        ],
    },
    dict(
        tag="ital",
        name="Italic",
        ordering=3,
        values=[dict(value=1, name="Italic")],  # Italic
    ),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("font", type=Path)
    parser.add_argument("--verbose", action="store_true")
    parsed_args = parser.parse_args()
    font_path = parsed_args.font
    font: TTFont = TTFont(font_path)

    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.WARNING)
    LOGGER = logging.getLogger(__name__)
    if parsed_args.verbose:
        LOGGER.setLevel(logging.INFO)

    if font["name"].getDebugName(nameID=2) == "Italic":
        buildStatTable(font, ITALIC_AXES)
        LOGGER.info("[STAT TABLE] Added italic STAT table to %s", font_path)
    else:
        buildStatTable(font, UPRIGHT_AXES)
        LOGGER.info("[STAT TABLE] Added upright STAT table to %s", font_path)

    font.save(font_path)


if __name__ == "__main__":
    main()
