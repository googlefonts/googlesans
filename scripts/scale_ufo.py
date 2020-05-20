# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from copy import deepcopy
import logging
from ufoLib2 import Font
from fontMath import MathInfo, MathKerning, MathGlyph


__all__ = ["scale_ufo"]


# fontinfo.plist attributes to exclude from fontMath's scaling operation
EXCLUDE_INFO_ATTRIBUTES = {
    "postscriptWeightName",
    "openTypeHeadLowestRecPPEM",
    "openTypeOS2WidthClass",
    "openTypeOS2WeightClass",
    "postscriptSlantAngle",
    "postscriptBlueFuzz",
    "postscriptBlueScale",
    # TODO: check if other postcript hinting-related attributes should not be scaled
}


def _scale_info(font, scale_factor, rounded=True):
    minfo = MathInfo(font.info)
    minfo *= scale_factor
    if rounded:
        minfo = minfo.round()

    excluded = {attr: getattr(font.info, attr) for attr in EXCLUDE_INFO_ATTRIBUTES}
    minfo.extractInfo(font.info)
    for attr, value in excluded.items():
        setattr(font.info, attr, value)


def _scale_kerning(font, scale_factor, rounded=True):
    mkern = MathKerning(font.kerning)
    mkern *= scale_factor
    if rounded:
        mkern.round()
    mkern.extractKerning(font)


def _scale_glyphs(font, scale_factor, rounded=True):
    for glyph_name in font.keys():
        glyph = font[glyph_name]
        # NOTE: 'scaleComponentTransform' option was added with fontMath 0.6.0
        # https://github.com/robotools/fontMath/issues/193
        mglyph = MathGlyph(glyph, scaleComponentTransform=False)
        mglyph *= scale_factor
        if rounded:
            mglyph = mglyph.round()
        mglyph.extractGlyph(glyph, onlyGeometry=True)


def scale_ufo(font, scale_factor, rounded=True, inplace=True):
    if not inplace:
        font = deepcopy(font)

    _scale_info(font, scale_factor, rounded=rounded)
    _scale_kerning(font, scale_factor, rounded=rounded)
    _scale_glyphs(font, scale_factor, rounded=rounded)

    return font


def main(args=None):
    import argparse

    parser = argparse.ArgumentParser("scale_ufo")
    parser.add_argument(
        "--output", metavar="OUTPUT_UFO", help="If omitted, save UFO in place"
    )
    parser.add_argument(
        "input_ufo", metavar="INPUT_UFO", help="Path to input UFO to be scaled"
    )
    parser.add_argument(
        "upem", metavar="UPEM", type=int, help="Units Per EM of the scaled UFO"
    )
    parser.add_argument("--no-round", dest="rounded", action="store_false")
    options = parser.parse_args(args)

    logging.basicConfig(level="INFO")

    font = Font.open(options.input_ufo, lazy=False)

    scale_factor = options.upem / font.info.unitsPerEm

    logging.info("scale factor: %s", scale_factor)

    scale_ufo(font, scale_factor, rounded=options.rounded)

    if options.output:
        font.save(options.output, overwrite=True)
    else:
        font.save()


if __name__ == "__main__":
    main()
