"""Convert Designspace to Glyphs.app file.

Saves output to same path as the Designspace with a `.glyphs` suffix. Disables
the lastChanged marker of glyphs, which we don't need with UFOs.
"""

import argparse
from pathlib import Path

import glyphsLib
from fontTools.designspaceLib import DesignSpaceDocument

ROOT_DIR = Path(__file__).parent.parent

parser = argparse.ArgumentParser()
parser.add_argument(
    "designspace", nargs="+", type=Path, help="Path to input Designspace."
)
parsed_args = parser.parse_args()

for designspace_path in parsed_args.designspace:
    designspace = DesignSpaceDocument.fromfile(designspace_path)
    font = glyphsLib.to_glyphs(designspace, minimize_ufo_diffs=True)
    font.customParameters["Disable Last Change"] = True
    font.save(designspace_path.with_suffix(".glyphs"))
