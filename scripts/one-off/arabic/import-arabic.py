# Copyright 2026 Google Sans Authors
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

import re
from io import StringIO
from pathlib import Path
from typing import Literal

from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.feaLib.ast import (
    Element,
    FeatureBlock,
    FeatureFile,
    GlyphClass,
    GlyphClassDefStatement,
    GlyphName,
    LanguageStatement,
    LanguageSystemStatement,
    LigatureCaretByPosStatement,
    LookupBlock,
    LookupReferenceStatement,
    MarkClass,
    ScriptStatement,
    SinglePosStatement,
    TableBlock,
    ValueRecord,
)
from fontTools.feaLib.parser import Parser
from fontTools.misc.visitor import Visitor
from ufoLib2 import Font
from ufoLib2.objects import Anchor

# These glyphs have outlines in both.
# TODO: Which need kerning or components adjusting?
SKIP = {
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "zero.tf",
    "one.tf",
    "two.tf",
    "three.tf",
    "four.tf",
    "five.tf",
    "six.tf",
    "seven.tf",
    "eight.tf",
    "nine.tf",
    "space",
    "thinspace",
    "hairspace",
    "mark-ar",
    "parenleft",
    "parenright",
    "question",
    "radical",
    "dottedCircle",
    # This isn't referenced by any features or glyphs, and is on the skip export
    # list, so ignore.
    "slash",
}

# NOTE: Only renames the glyph and references to it in composites. This is
# sufficient for the glyphs currently defined here.
RENAME = {
    # Slightly different outlines; preserve as an alternate unless composites
    # are updated.
    "percentbar": "percentbar-ar",
}

# Define sources and targets.
ds_from = DesignSpaceDocument.fromfile(
    Path("../Subfamilies/Arabic", "masters", "GoogleSansArabic.designspace")
)
ds_to = DesignSpaceDocument.fromfile(
    Path("source", "GoogleSans", "GoogleSans.designspace")
)
fea_from = Path(
    "..", "Subfamilies/Arabic", "build", "arabic", "GoogleSansArabic.fea"
).read_text()

name_to_tag = {
    **{axis.name: axis.tag for axis in ds_from.axes},
    **{axis.name: axis.tag for axis in ds_to.axes},
}

ds_from.loadSourceFonts(Font.open)
ufos_to = ds_to.loadSourceFonts(Font.open)

space_changes: dict[
    # DI name (file stem)
    str,
    # Glyph name -> width change amount
    dict[Literal["space", "thinspace", "hairspace"], float],
] = {}

# Copy every glyph to every target location that is a superset of the source axes.
for source_from in ds_from.sources:
    assert isinstance(source_from.font, Font)
    assert source_from.layerName is None, "unexpected sparse layer"

    loc_from = {
        name_to_tag[name]: value
        for name, value in source_from.getFullDesignLocation(ds_from).items()
    }

    # for glyph_name in ("space", "thinspace", "hairspace"):
    space_from = {
        glyph_name: source_from.font[glyph_name].width
        for glyph_name in ("space", "thinspace", "hairspace")
    }
    spaces_to: dict[Literal["space", "thinspace", "hairspace"], set[float]] = {}

    for source_to in ds_to.sources:
        assert isinstance(source_to.font, Font)
        if source_to.layerName is not None:
            continue

        loc_to = {
            name_to_tag[name]: value
            for name, value in source_to.getFullDesignLocation(ds_to).items()
        }
        matches = all(loc_from[tag] == loc_to[tag] for tag in loc_from)

        if not matches:
            continue

        for glyph_name in ("space", "thinspace", "hairspace"):
            spaces_to.setdefault(glyph_name, set()).add(
                source_to.font[glyph_name].width
            )

        for glyph in source_from.font:
            assert glyph.name is not None

            if glyph.name in SKIP:
                continue

            # Rename if required, while copying to allow mutation.
            glyph = glyph.copy(RENAME.get(glyph.name, glyph.name))
            assert glyph.name is not None
            assert glyph.name not in source_to.font, glyph.name

            glyph.clearAnchors()  # Handled by feature code
            for component in glyph.components:
                component.baseGlyph = RENAME.get(
                    component.baseGlyph, component.baseGlyph
                )
            source_to.font[glyph.name] = glyph

        # For compatibility checker, only:
        source_to.font.lib["public.skipExportGlyphs"].extend(
            sorted(set(source_from.font.lib.get("public.skipExportGlyphs", [])) - SKIP)
        )

        # Keep track of how /space needs its width adjusted too.
        for glyph_name, new_widths in spaces_to.items():
            (space_to,) = new_widths
            assert source_from.path is not None
            di_space_changes = space_changes.setdefault(Path(source_from.path).stem, {})
            di_space_changes[glyph_name] = space_from[glyph_name] - space_to


# Skip or decompose the glyphs that the source does too.
ds_to.lib["public.skipExportGlyphs"].extend(
    sorted(set(ds_from.lib.get("public.skipExportGlyphs", [])) - SKIP)
)

# Use the direct output of the custom feature writers. This debug fea is
# delineated by comment headers into the sources that each section came from.
# We must split as a string line-by-line, otherwise the Parser will report
# false-positive duplicate definitions across the boundaries.
fea_by_source_raw: dict[str, list[str]] = {}
current_source = None
for line in fea_from.strip().splitlines():
    header = re.match(r"\A### (.+) ###\Z", line)
    if header:
        current_source = header.group(1)
    else:
        assert current_source is not None
        fea_by_source_raw.setdefault(current_source, []).append(line)

# Parsing can now occur.
fea_by_source: dict[str, FeatureFile] = {
    source: Parser(StringIO("\n".join(lines))).parse()
    for source, lines in fea_by_source_raw.items()
}
assert len(fea_by_source) == 4


class SuffixingVisitor(Visitor):
    pass


@SuffixingVisitor.register((LookupBlock, MarkClass))
def visit(_visitor: SuffixingVisitor, obj: LookupBlock | MarkClass) -> None:
    if not obj.name.endswith("_arabic"):
        obj.name += "_arabic"


visitor = SuffixingVisitor()

# Process the features further to adjust the advance of spaces, extract some
# GDEF information, and write the feature files.
mapping = {
    "GoogleSansArabic-Regular": {"opsz": 18, "wght": 380},
    "GoogleSansArabic-Bold": {"opsz": 18, "wght": 734},
    "GoogleSansArabicText-Regular": {"opsz": 17, "wght": 380},
    "GoogleSansArabicText-Bold": {"opsz": 17, "wght": 734},
}
for source, fea in fea_by_source.items():
    # Extract GDEF and languagesystem information, then omit these from the fea.
    kept_elements: list[Element] = []
    categories: dict[str, str] | None = None
    ligature_carets: dict[str, list[int]] = {}
    arabic_languages: set[str] = set()
    for element in fea.statements:
        if isinstance(element, LanguageSystemStatement):
            # Only Arabic languagesystem statements must be added to avoid
            # duplication. In addition, note the specific languages, for
            # registering our new locl feature later.
            if element.script == "arab":
                arabic_languages.add(element.language)
            else:
                continue
        elif isinstance(element, TableBlock) and element.name == "GDEF":
            # These must be stored in a <lib> key instead of in the feature
            # files otherwise ufo2ft will not create the automatic GDEF for all
            # other writing systems.
            for element in element.statements:
                if isinstance(element, GlyphClassDefStatement):
                    assert categories is None
                    categories = {}
                    assert isinstance(element.baseGlyphs, GlyphClass)
                    for glyph in element.baseGlyphs.glyphs:
                        assert isinstance(glyph, str)
                        assert glyph not in categories
                        categories[glyph] = "base"
                    assert isinstance(element.markGlyphs, GlyphClass)
                    for glyph in element.markGlyphs.glyphs:
                        assert isinstance(glyph, str)
                        assert glyph not in categories
                        categories[glyph] = "mark"
                    assert isinstance(element.ligatureGlyphs, GlyphClass)
                    for glyph in element.ligatureGlyphs.glyphs:
                        assert isinstance(glyph, str)
                        assert glyph not in categories
                        categories[glyph] = "ligature"
                    assert isinstance(element.componentGlyphs, GlyphClass)
                    for glyph in element.componentGlyphs.glyphs:
                        assert isinstance(glyph, str)
                        assert glyph not in categories
                        categories[glyph] = "component"
                elif isinstance(element, LigatureCaretByPosStatement):
                    assert isinstance(element.glyphs, GlyphName)
                    assert element.glyphs.glyph not in ligature_carets
                    ligature_carets[element.glyphs.glyph] = element.carets
                else:
                    assert False, f"Unrecognised GDEF element: {type(element)}"
            continue
        kept_elements.append(element)
    assert categories is not None

    di_space_changes = space_changes[source]

    # Create locl feature to adjust spaces for Arabic.
    spaces_lookup = LookupBlock("arabicspace")
    spaces_lookup.statements = [
        SinglePosStatement(
            [(GlyphName(glyph_name), ValueRecord(xAdvance=space_change))],
            prefix=[],
            suffix=[],
            forceChain=False,
        )
        for glyph_name, space_change in di_space_changes.items()
    ]
    kept_elements.append(spaces_lookup)

    locl_fea = FeatureBlock("locl")
    locl_fea.statements = [
        ScriptStatement("arab"),
        *(
            statement
            for lang in sorted(arabic_languages)
            for statement in (
                LanguageStatement(lang),
                LookupReferenceStatement(spaces_lookup),
            )
        ),
    ]
    kept_elements.append(locl_fea)
    fea.statements = kept_elements

    visitor.visit(fea)

    # Write feature file.
    loc_from = mapping[source]
    path = Path(
        "source",
        "GoogleSans",
        f"arabic-opsz{loc_from['opsz']}-wght{loc_from['wght']}.fea",
    )
    path.write_text(fea.asFea())

    # Add feature file and GDEF information to all relevant UFOs.
    for source_to in ds_to.sources:
        assert isinstance(source_to.font, Font)
        if source_to.layerName is not None:
            continue

        loc_to = {
            name_to_tag[name]: value
            for name, value in source_to.getFullDesignLocation(ds_to).items()
        }
        matches = all(loc_from[tag] == loc_to[tag] for tag in loc_from)

        if not matches:
            continue

        ufo_cats = source_to.font.lib["public.openTypeCategories"]
        for glyph, category in categories.items():
            if glyph in SKIP:
                continue
            assert glyph not in ufo_cats
            ufo_cats[glyph] = category

        for glyph in source_to.font:
            assert glyph.name is not None
            if glyph.name in SKIP:
                continue
            if carets := ligature_carets.get(glyph.name):
                for idx, x in enumerate(sorted(carets, reverse=True)):
                    glyph.appendAnchor(Anchor(x=x, name=f"caret_{idx + 1}", y=0))

        source_to.font.features.text += f"include({path.name});\n"

# Save everything.
for ufo in ufos_to:
    ufo.save()

ds_to.write(ds_to.path)
