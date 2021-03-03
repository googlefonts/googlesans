import copy
from pathlib import Path
from typing import List, Set

import ufo2ft
import ufoLib2
from fontTools.designspaceLib import (
    DesignSpaceDocument,
    InstanceDescriptor,
    RuleDescriptor,
    SourceDescriptor,
)
from glyphsLib.builder.builders import _expand_kerning_to_brackets

from . import gdef


def scrub_designspace(designspace: DesignSpaceDocument, project_root: Path) -> None:
    designspace.loadSourceFonts(ufoLib2.Font.open)
    skip_export_glyphs = set(designspace.lib.get("public.skipExportGlyphs", []))
    rules = designspace.rules

    for source in designspace.sources:
        scrub_source(source, skip_export_glyphs, rules)

    for instance in designspace.instances:
        scrub_instance(instance, project_root)


    if skip_export_glyphs:
        designspace.lib["public.skipExportGlyphs"] = sorted(skip_export_glyphs)
    designspace.lib = {
        k: v
        for k, v in designspace.lib.items()
        if k.startswith("public.")
        or k.startswith("com.github.googlei18n.ufo2ft.")
        or k == "GSDimensionPlugin.Dimensions"
    }


def scrub_instance(instance: InstanceDescriptor, project_root: Path) -> None:
    lib = instance.lib
    if not lib:
        return

    # Custom parameters influence the build.
    keys_to_keep = {"com.schriftgestaltung.customParameters"}

    # Exporting is the default, only remember if not exporting.
    if lib.get("com.schriftgestaltung.export") is False:
        keys_to_keep.add("com.schriftgestaltung.export")

    instance.lib = {
        k: v for k, v in lib.items() if k.startswith("public.") or k in keys_to_keep
    }

    # Trick DesignSpaceDocument.updatePaths() into doing the right thing.
    filename = Path(instance.filename)
    instance.filename = None
    instance.path = str(
        project_root / "build" / "GoogleSans" / "instance_ufo" / filename.name
    )


def scrub_source(
    source: SourceDescriptor, skip_export_glyphs: Set[str], rules: List[RuleDescriptor]
) -> None:
    scrub_ufo(source.font, skip_export_glyphs, rules)


def scrub_ufo(
    ufo: ufoLib2.Font, skip_export_glyphs: Set[str], rules: List[RuleDescriptor]
) -> None:
    # Clean global lib.
    keys_to_keep = {
        # UFOs don't need lastChanged because glyphs are separate files, keep it disabled.
        "com.schriftgestaltung.customParameter.GSFont.disablesLastChange",
        # May be useful for Glyphs.
        "com.schriftgestaltung.customParameter.GSFont.Enforce Compatibility Check",
        # Cuts down on ufo2glyphs Git diffs slightly.
        "com.schriftgestaltung.fontMasterID",
    }
    keys_to_remove = {
        # Using production names is fontmake's default.
        "com.github.googlei18n.ufo2ft.useProductionNames"
    }
    ufo.lib = {
        k: v
        for k, v in ufo.lib.items()
        if (
            k.startswith("public.")
            or k.startswith("com.github.googlei18n.ufo2ft.")
            or k in keys_to_keep
        )
        and k not in keys_to_remove
    }

    ufo.lib["public.skipExportGlyphs"] = sorted(skip_export_glyphs)

    # Reset the ufo2ft filters.
    ufo.lib["com.github.googlei18n.ufo2ft.filters"] = [
        {
            "name": "propagateAnchors",
            "pre": True,
            # Compiling Glyphs files to VFs does not propagate anchors in the following
            # glyphs:
            "exclude": [
                "finalpedagesh-hb.BRACKET.18",
                "Gbreve.BRACKET.18",
                "Gcircumflex.BRACKET.18",
                "Gcommaaccent.alt.BRACKET.18",
                "gcommaaccent.BRACKET.18",
                "Gcommaaccent.BRACKET.18",
                "Gdotaccent.BRACKET.18",
                "kcommaaccent.alt.BRACKET.18",
                "Kcommaaccent.alt.BRACKET.18",
                "kcommaaccent.BRACKET.18",
                "Kcommaaccent.BRACKET.18",
                "lcommaaccent.BRACKET.18",
                "Lcommaaccent.BRACKET.18",
                "ncommaaccent.BRACKET.18",
                "Ncommaaccent.BRACKET.18",
                "pedagesh-hb.BRACKET.18",
                "perafe-hb.BRACKET.18",
                "rcommaaccent.alt.BRACKET.18",
                "Rcommaaccent.alt.BRACKET.18",
                "rcommaaccent.BRACKET.18",
                "Rcommaaccent.BRACKET.18",
                "samekhdagesh-hb.BRACKET.18",
                "scommaaccent.BRACKET.18",
                "Scommaaccent.BRACKET.18",
                "tcommaaccent.BRACKET.18",
                "Tcommaaccent.BRACKET.18",
                "yacute.BRACKET.18",
                "ycircumflex.BRACKET.18",
                "ydieresis.BRACKET.18",
                "ydotbelow.BRACKET.18",
                "ygrave.BRACKET.18",
                "yhookabove.BRACKET.18",
                "ytilde.BRACKET.18",
            ],
        },
        # Uncomment after attaining parity between Glyphs file and DS compilation.
        # {"name": "flattenComponents", "pre": True},
    ]

    # Delete non-build-relevant layers.
    layers_to_delete = []
    for layer in ufo.layers:
        if layer is ufo.layers.defaultLayer:
            continue
        if layer.name.startswith(("[", "{")) and ".background" not in layer.name:
            continue
        layers_to_delete.append(layer.name)
    for layer_name in layers_to_delete:
        del ufo.layers[layer_name]

    for layer in ufo.layers:
        layer.lib = {
            k: v
            for k, v in layer.lib.items()
            if k.startswith("public.")
            or not k.startswith("com.schriftgestaltung.layerOrderInGlyph.")
        }

    # Clean glif libs.
    for layer in ufo.layers:
        for glyph in layer:
            if not glyph.lib:
                continue

            glyph.lib = {
                k: v
                for k, v in glyph.lib.items()
                if (k.startswith("public.") and k != "public.markColor")
                or (
                    k.startswith("com.schriftgestaltung.Glyphs.")
                    and k != "com.schriftgestaltung.Glyphs.lastChange"
                )
            }

    # Clean out empty/non-existing groups and kerning pairs.
    new_groups = {}
    for key, value in ufo.groups.items():
        new_value = [v for v in value if v in ufo]
        if new_value:
            new_groups[key] = new_value
    ufo.groups.clear()
    ufo.groups.update(new_groups)

    new_kerning = {}
    for key, value in ufo.kerning.items():
        first, second = key
        if (first in ufo.groups or first in ufo) and (
            second in ufo.groups or second in ufo
        ):
            new_kerning[key] = value
    ufo.kerning.clear()
    ufo.kerning.update(new_kerning)

    # Bracket glyphs are a Glyphs.app construct that inherit the kerning from
    # their parents.
    for rule in rules:
        for name, name_bracket in rule.subs:
            _expand_kerning_to_brackets(name, name_bracket, ufo)

    # Update GDEF table. Anchors have to be propagated before we can construct
    # the GDEF table. Use the UFO copy so we can safely save the original with
    # just updated features.
    ufo_copy = copy.deepcopy(ufo)
    skip_export_glyphs_copy = copy.copy(skip_export_glyphs)
    pre_filter, _ = ufo2ft.filters.loadFilters(ufo_copy)
    for pf in pre_filter:
        # Treat excluded glyphs as if they are skipped glpyhs to ensure they don't
        # show up in the feature file and cause a compilation error.
        if pf.name == "PropagateAnchorsFilter":
            skip_export_glyphs_copy.update(
                g.name for g in ufo_copy if not pf.include(g)
            )
        pf(font=ufo_copy)

    # Generate GDEF definition string.
    gdef_table_lines = gdef.build_gdef(ufo_copy, skip_export_glyphs_copy)
    features = ufo.features.text.split("\n")
    try:
        gdef_start = features.index("table GDEF {")
        gdef_end = features.index("} GDEF;") + 1
        features[gdef_start:gdef_end] = gdef_table_lines
    except ValueError:
        features.extend(gdef_table_lines)
        features.append("")  # newline.
    ufo.features.text = "\n".join(features)
