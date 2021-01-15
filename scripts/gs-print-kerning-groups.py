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
