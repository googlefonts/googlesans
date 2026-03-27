"""
Proof-of-concept import of Arabic.

After QA, the final goal is to have a record of the equivalent steps that would
be taken in a font editor in a literate programming style. In particular, there
are too many steps that would need manually undone to use an off-the-shelf merge
tool.

TODO: Continue to adapt in response to QA.
"""

import re
from pathlib import Path

from fontTools.designspaceLib import DesignSpaceDocument
from ufoLib2 import Font

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
    Path("..", "googlesans-arabic", "masters", "GoogleSansArabic.designspace")
)
ds_to = DesignSpaceDocument.fromfile(
    Path("source", "GoogleSans", "GoogleSans.designspace")
)
fea_from = Path(
    "..", "googlesans-arabic", "build", "arabic", "GoogleSansArabic.fea"
).read_text()

name_to_tag = {
    **{axis.name: axis.tag for axis in ds_from.axes},
    **{axis.name: axis.tag for axis in ds_to.axes},
}

ds_from.loadSourceFonts(Font.open)
ufos_to = ds_to.loadSourceFonts(Font.open)

space_changes = {}

# Copy every glyph to every target location that is a superset of the source axes.
for source_from in ds_from.sources:
    assert isinstance(source_from.font, Font)
    assert source_from.layerName is None, "unexpected sparse layer"

    loc_from = {
        name_to_tag[name]: value
        for name, value in source_from.getFullDesignLocation(ds_from).items()
    }

    space_from = source_from.font["space"].width
    spaces_to = set()

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

        spaces_to.add(source_to.font["space"].width)

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
    (space_to,) = spaces_to
    space_changes[Path(source_from.path).stem] = space_from - space_to


# Skip or decompose the glyphs that the source does too.
ds_to.lib["public.skipExportGlyphs"].extend(
    sorted(set(ds_from.lib.get("public.skipExportGlyphs", [])) - SKIP)
)
# TODO: GDEF categories?

# Use the direct output of the custom feature writers.
by_source = {}
current_source = None
arabic_languages = set()
for line in fea_from.strip().splitlines():
    header = re.match(r"\A### (.+) ###\Z", line)
    languagesystem = re.match(r"\Alanguagesystem (.+) (.+)\Z", line)
    if header:
        current_source = header.group(1)
    else:
        if languagesystem:
            # Only keep Arabic language systems.
            if languagesystem.group(1) != "arab":
                continue
            else:
                arabic_languages.add(languagesystem.group(2))
        by_source.setdefault(current_source, []).append(line)

assert len(by_source) == 4


# Create a feature to adjust the advance of /space, and write the feature files.
mapping = {
    "GoogleSansArabic-Regular": {"opsz": 18, "wght": 380},
    "GoogleSansArabic-Bold": {"opsz": 18, "wght": 734},
    "GoogleSansArabicText-Regular": {"opsz": 17, "wght": 380},
    "GoogleSansArabicText-Bold": {"opsz": 17, "wght": 734},
}
for source, lines in by_source.items():
    space_change = space_changes[source]
    lines.extend(
        f"""
        lookup arabicspace {{
            pos space {space_change};
        }} arabicspace;

        feature dist {{
            script arab;
            {
            "\n".join(
                line
                for lang in sorted(arabic_languages)
                for line in [f"language {lang};", "lookup arabicspace;"]
            )
        }
        }} dist;
""".strip().splitlines()
    )

    loc_from = mapping[source]
    path = Path(
        "source",
        "GoogleSans",
        f"arabic-opsz{loc_from['opsz']}-wght{loc_from['wght']}.fea",
    )
    path.write_text("\n".join(lines))

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

        source_to.font.features.text += f"include({path.name})\n"

# Save everything.
for ufo in ufos_to:
    ufo.save()

ds_to.write(ds_to.path)
