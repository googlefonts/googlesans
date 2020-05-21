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
from ufo2ft.filters.transformations import TransformationsFilter


__all__ = ["scale_ufo"]


# fontinfo.plist attributes to include in scaling operation
INCLUDE_INFO_ATTRIBUTES = {
    "unitsPerEm",
    "descender",
    "xHeight",
    "capHeight",
    "ascender",
    "openTypeHheaAscender",
    "openTypeHheaDescender",
    "openTypeHheaLineGap",
    "openTypeHheaCaretOffset",
    "openTypeOS2TypoAscender",
    "openTypeOS2TypoDescender",
    "openTypeOS2TypoLineGap",
    "openTypeOS2WinAscent",
    "openTypeOS2WinDescent",
    "openTypeOS2SubscriptXSize",
    "openTypeOS2SubscriptYSize",
    "openTypeOS2SubscriptXOffset",
    "openTypeOS2SubscriptYOffset",
    "openTypeOS2SuperscriptXSize",
    "openTypeOS2SuperscriptYSize",
    "openTypeOS2SuperscriptXOffset",
    "openTypeOS2SuperscriptYOffset",
    "openTypeOS2StrikeoutSize",
    "openTypeOS2StrikeoutPosition",
    "openTypeVheaVertTypoAscender",
    "openTypeVheaVertTypoDescender",
    "openTypeVheaVertTypoLineGap",
    "openTypeVheaCaretOffset",
    "postscriptUnderlineThickness",
    "postscriptUnderlinePosition",
    "postscriptBlueValues",
    "postscriptOtherBlues",
    "postscriptFamilyBlues",
    "postscriptFamilyOtherBlues",
    "postscriptStemSnapH",
    "postscriptStemSnapV",
    "postscriptBlueShift",
    "postscriptDefaultWidthX",
    "postscriptNominalWidthX",
}


def _scale_info(font, scale_factor):

    def scale(v):
        v *= scale_factor
        if attr.startswith("openType"):
            # ufoLib validators strictly require these to be formatted as integers
            return round(v)
        return v

    for attr in INCLUDE_INFO_ATTRIBUTES:
        value = getattr(font.info, attr)
        if isinstance(value, list):
            setattr(font.info, attr, [scale(v) for v in value])
        elif value is not None:
            setattr(font.info, attr, scale(value))


def _scale_kerning(font, scale_factor):
    for pair, value in font.kerning.items():
        font.kerning[pair] = value * scale_factor


def _scale_glyphs(font, scale_factor):
    # ufo2ft transformations filter uses percentages for scale.
    # NOTE: Make sure to use ufo2ft 2.14 as it fixes a bug with transformations of
    # composite glyphs: https://github.com/googlefonts/ufo2ft/issues/378
    scale = TransformationsFilter(ScaleX=scale_factor * 100, ScaleY=scale_factor * 100)
    scale(font)

    for glyph in font:
        glyph.width *= scale_factor
        glyph.height *= scale_factor


def scale_ufo(font, scale_factor, inplace=True):
    if not inplace:
        font = deepcopy(font)

    _scale_info(font, scale_factor)
    _scale_kerning(font, scale_factor)
    _scale_glyphs(font, scale_factor)

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
    options = parser.parse_args(args)

    logging.basicConfig(level="INFO")

    font = Font.open(options.input_ufo, lazy=False)

    scale_factor = options.upem / font.info.unitsPerEm
    if scale_factor.is_integer():
        scale_factor = int(scale_factor)

    logging.info("scale factor: %s", scale_factor)

    scale_ufo(font, scale_factor)

    if options.output:
        font.save(options.output, overwrite=True)
    else:
        font.save()


if __name__ == "__main__":
    main()
