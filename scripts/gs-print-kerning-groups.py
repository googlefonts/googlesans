"""Print (kerning) groups in a Glyphs.app file from the perspective of a UFO
library.

Useful to get a list of groups you want to import from a Glyphs.app file into
the base sources.
"""

import argparse

import glyphsLib
import glyphsLib.builder

parser = argparse.ArgumentParser()
parser.add_argument("input", type=glyphsLib.GSFont, help="Path to source .glyphs file.")
parsed_args = parser.parse_args()

builder = glyphsLib.builder.UFOBuilder(
    parsed_args.input,
    propagate_anchors=False,
    minimize_glyphs_diffs=False,
    generate_GDEF=False,
    store_editor_state=False,
)

first_master = next(builder.masters)

print("\n".join(sorted(first_master.groups)))
