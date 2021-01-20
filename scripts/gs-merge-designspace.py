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

"""Merge an incoming Designspace into an existing Designspace.

This script will import glyphs amd groups specified in import text files
(one name per line) and kerning pairs that mention either of them. It will
also update each UFO's public.glyphOrder and public.postscriptNames lib keys
with entries for all imported glyphs, as well as public.skipExportGlyphs in
Designspace and UFOs.

It does not import any font info, global or local guidelines or features.
Designspace rules are also left untouched. Glyphs.app brace layers are not
supported.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, List

import ufoLib2
from fontTools.designspaceLib import DesignSpaceDocument

MASTER_ID_KEY = "com.schriftgestaltung.fontMasterID"
SKIP_EXPORT_GLYPHS_KEY = "public.skipExportGlyphs"

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")


parser = argparse.ArgumentParser()
parser.add_argument(
    "--source",
    type=Path,
    help="Path to source .designspace file.",
    required=True,
)
parser.add_argument(
    "--target",
    type=Path,
    help="Path to target .designspace file.",
    required=True,
)
parser.add_argument(
    "--import-glyphs-file",
    type=Path,
    help=(
        "Path to text file with glyph names to import (one per line). "
        "Also imports any kerning pair that mentions them."
    ),
)
parser.add_argument(
    "--import-groups-file",
    type=Path,
    help=(
        "Path to text file with group names to import (one per line). "
        "Also imports any kerning pair that mentions them."
    ),
)
parsed_args = parser.parse_args()


# Read in stuff to import.
if parsed_args.import_glyphs_file is not None:
    import_glyphs = {
        name.strip()
        for name in parsed_args.import_glyphs_file.read_text().split("\n")
        if name
    }
else:
    import_glyphs = set()

if parsed_args.import_groups_file is not None:
    import_groups = {
        name.strip()
        for name in parsed_args.import_groups_file.read_text().split("\n")
        if name
    }
else:
    import_groups = set()

if not import_glyphs and not import_groups:
    logging.error("You should provide at least one file with stuff to import.")
    sys.exit(1)


# Load all sources.
designspace_import = DesignSpaceDocument.fromfile(parsed_args.source)
designspace_import.loadSourceFonts(ufoLib2.Font.open)
designspace_target = DesignSpaceDocument.fromfile(parsed_args.target)
designspace_target.loadSourceFonts(ufoLib2.Font.open)


# Update skip export glyphs list.
skip_export_glyphs_import = set(designspace_import.lib.get(SKIP_EXPORT_GLYPHS_KEY, []))
skip_export_glyphs_target = set(designspace_target.lib.get(SKIP_EXPORT_GLYPHS_KEY, []))
skip_export_glyphs_target.update(
    n for n in skip_export_glyphs_import if n in import_glyphs
)
skip_export_glyphs = sorted(skip_export_glyphs_target)
if skip_export_glyphs_target:
    designspace_target.lib[SKIP_EXPORT_GLYPHS_KEY] = skip_export_glyphs


# Actually import now.
for import_source in designspace_import.sources:
    if import_source.layerName is not None:
        logging.error("Brace layers not supported currently.")
        sys.exit(1)

    # Match import to target UFO.
    try:
        target_source = next(
            s
            for s in designspace_target.sources
            if s.location == import_source.location
        )
    except StopIteration:
        try:
            target_source = next(
                s
                for s in designspace_target.sources
                if s.font.lib[MASTER_ID_KEY] == import_source.font.lib[MASTER_ID_KEY]
            )
        except (StopIteration, KeyError):
            logging.error(
                "Cannot find target for source %s because there's no target location %s "
                "and no target with a matching master ID.",
                import_source.name,
                import_source.location,
            )
            sys.exit(1)

    import_font: ufoLib2.Font = import_source.font
    target_font: ufoLib2.Font = target_source.font

    # Snatch up any bracket glyphs for glyphs without them being explicitly
    # listed in the import file. ".BRACKET." is a glyphsLib convention.
    for glyph in import_font:
        if ".BRACKET." not in glyph.name:
            continue
        base = glyph.name.split(".BRACKET.")[0]
        if base in import_glyphs:
            import_glyphs.add(glyph.name)
            logging.warning(
                "Added bracket glyph '%s', manually add to the Designspace rules.",
                glyph.name,
            )

    for glyph_name in import_glyphs:
        try:
            target_font[glyph_name] = import_font[glyph_name]
        except KeyError as e:
            logging.error(
                "Glyph '%s' does not exist in the source UFO %s, aborting.",
                str(e),
                str(import_source.filename),
            )
            sys.exit(1)

    for group_name in import_groups:
        try:
            target_font.groups[group_name] = import_font.groups[group_name]
        except KeyError as e:
            logging.warning(
                "Kerning group %s does not exist in the source UFO %s, skipping.",
                str(e),
                str(import_source.filename),
            )
            continue

    # Import kerning where either side of a pair is an imported glyph or group:
    for key, value in import_font.kerning.items():
        first, second = key
        if (
            first in import_groups
            or first in import_glyphs
            or second in import_groups
            or second in import_glyphs
        ):
            target_font.kerning[key] = value

    # Import public.glyphOrder while keeping order:
    target_glyph_order: List[str] = target_font.lib["public.glyphOrder"]
    target_glyph_order_set = set(target_glyph_order)
    for name in import_font.lib["public.glyphOrder"]:
        if name not in target_glyph_order_set and name in import_glyphs:
            target_glyph_order.append(name)

    # Import public.postscriptNames for imported glyphs:
    target_ps_names: Dict[str, str] = target_font.lib["public.postscriptNames"]
    for key, value in import_font.lib["public.postscriptNames"].items():
        if key in import_glyphs:
            target_ps_names[key] = value

    # Write global public.skipExportGlyphs list to all UFOs.
    target_font.lib[SKIP_EXPORT_GLYPHS_KEY] = skip_export_glyphs

    target_font.save()

designspace_target.write(parsed_args.target)
