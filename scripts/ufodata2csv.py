# pyright: strict

# Copyright 2021 Google Sans Authors
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

"""Export global glpyh data of UFOs to a CSV file."""

from __future__ import annotations

import argparse
import csv
import logging
from dataclasses import dataclass

from ufoLib2 import Font

parser = argparse.ArgumentParser()
parser.add_argument("ufos", nargs="+", type=Font.open)
parser.add_argument("output")
parsed_args = parser.parse_args()


@dataclass
class GlyphData:
    export: bool
    opentype_category: str | None
    postscript_name: str | None
    unicodes: list[int]


glyph_data: dict[str, GlyphData] = {}
for ufo in parsed_args.ufos:
    psn: dict[str, str] = ufo.lib.get("public.postscriptNames", {})
    otc: dict[str, str] = ufo.lib.get("public.openTypeCategories", {})
    seg: list[str] = ufo.lib.get("public.skipExportGlyphs", [])

    for glyph in ufo:
        data = GlyphData(
            export=glyph.name not in seg,
            opentype_category=otc.get(glyph.name),
            postscript_name=psn.get(glyph.name),
            unicodes=glyph.unicodes,
        )
        if glyph.name in glyph_data:
            if glyph_data[glyph.name] != data:
                logging.warning(
                    "data mismatch for glyph '%s', have %s, found %s in %s",
                    glyph.name,
                    glyph_data[glyph.name],
                    data,
                    ufo._path,
                )
        else:
            glyph_data[glyph.name] = data

header = ("name", "postscript_name", "unicodes", "opentype_category", "export")
with open(parsed_args.output, "w+") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    for glyph, data in glyph_data.items():
        csvwriter.writerow(
            (
                glyph,
                data.postscript_name or "",
                " ".join(f"{v:04X}" for v in data.unicodes),
                data.opentype_category or "",
                data.export,
            )
        )
