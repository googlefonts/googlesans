# Copyright 2022 Google Sans Authors
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

from pathlib import Path

from fontTools.designspaceLib import DesignSpaceDocument
from ufoLib2 import Font

from internal.reachable_glyphs import reachable_glyphs, referenced_as_components

SOURCE_DIR = Path(__file__).parent.parent / "source" / "GoogleSans"

for path in SOURCE_DIR.glob("*.designspace"):
    designspace = DesignSpaceDocument.fromfile(path)
    skipped_glyphs = set(designspace.lib.get("public.skipExportGlyphs"))
    if skipped_glyphs is None:
        continue

    designspace.loadSourceFonts(Font.open)
    reachable_glyph_names = reachable_glyphs(designspace.default.font)
    reachable_glyph_names.update(
        referenced_as_components(designspace.default.font, reachable_glyph_names)
    )
    skipped_glyphs_unreachable = skipped_glyphs - reachable_glyph_names

    for source in designspace.sources:
        for layer in source.font.layers:
            for skipped_glyph in skipped_glyphs_unreachable:
                if skipped_glyph in layer:
                    del layer[skipped_glyph]
        source.font.save()

    if skipped_glyphs_unreachable == skipped_glyphs:
        del designspace.lib["public.skipExportGlyphs"]
    else:
        designspace.lib["public.skipExportGlyphs"] = sorted(
            set(designspace.lib["public.skipExportGlyphs"]) - skipped_glyphs_unreachable
        )
    designspace.write(path)
