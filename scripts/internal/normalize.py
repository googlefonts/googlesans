import copy
from pathlib import Path
from typing import Dict, List, Set

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

# Various alternatives are not exported because the `aalt` feature was to be
# removed, but should be kept around in case someone wants them at some point.
SKIP_EXPORT_GLYPHS = {
    "Ccedilla.alt",
    "G.alt",
    "Gbreve.alt",
    "Gcircumflex.alt",
    "Gcommaaccent.alt",
    "Gdotaccent.alt",
    "I.alt",
    "Iacute.alt",
    "Ibreve.alt",
    "Icircumflex.alt",
    "Idieresis.alt",
    "Idotaccent.alt",
    "Igrave.alt",
    "Imacron.alt",
    "Iogonek.alt",
    "Itilde.alt",
    "J.alt",
    "Jcircumflex.alt",
    "K.alt",
    "Kcommaaccent.alt",
    "M.alt",
    "Q.alt",
    "R.alt",
    "Racute.alt",
    "Rcaron.alt",
    "Rcommaaccent.alt",
    "Scedilla.alt",
    "W.alt",
    "Wacute.alt",
    "Wcircumflex.alt",
    "Wdieresis.alt",
    "Wgrave.alt",
    "a.alt",
    "aacute.alt",
    "abreve.alt",
    "abreveacute.alt",
    "abrevedotbelow.alt",
    "abrevegrave.alt",
    "abrevehookabove.alt",
    "abrevetilde.alt",
    "acircumflex.alt",
    "acircumflexacute.alt",
    "acircumflexdotbelow.alt",
    "acircumflexgrave.alt",
    "acircumflexhookabove.alt",
    "acircumflextilde.alt",
    "adieresis.alt",
    "adotbelow.alt",
    "ae.alt",
    "aeacute.alt",
    "agrave.alt",
    "ahookabove.alt",
    "amacron.alt",
    "ampersand.alt",
    "aogonek.alt",
    "aring.alt",
    "aringacute.alt",
    "atilde.alt",
    "caron.alt",
    "caroncomb.alt",
    "caroncomb.alt.cap",
    "ccedilla.alt",
    "cedilla.alt",
    "cedillacomb.alt",
    "comma.alt",
    "copyright.alt",
    "f_f_j.alt",
    "f_f_k.alt",
    "f_f_t.alt",
    "f_j.alt",
    "f_k.alt",
    "f_t.alt",
    "j.alt",
    "jcircumflex.alt",
    "jdotless.alt",
    "k.alt",
    "kcommaaccent.alt",
    "nine.alt",
    "nine.alt.cap",
    "one.alt",
    "one.alt.cap",
    "published.alt",
    "q.alt",
    "quotedblbase.alt",
    "quotedblleft.alt",
    "quotedblright.alt",
    "quoteleft.alt",
    "quoteright.alt",
    "quotesinglbase.alt",
    "r.alt",
    "r_t.alt",
    "racute.alt",
    "rcaron.alt",
    "rcommaaccent.alt",
    "registered.alt",
    "scedilla.alt",
    "semicolon.alt",
    "servicemark.alt",
    "servicemark.alt2",
    "servicemark.alt3",
    "seven.alt",
    "seven.alt.cap",
    "six.alt",
    "six.alt.cap",
    "t.alt",
    "t_f.alt",
    "t_t.alt",
    "tbar.alt",
    "tcaron.alt",
    "tcedilla.alt",
    "tcedilla.alt.2",
    "tcommaaccent.alt",
    "trademark.alt",
    "trademark.alt2",
    "trademark.alt3",
    "y.alt",
    "yacute.alt",
    "ycircumflex.alt",
    "ydieresis.alt",
    "ydotbelow.alt",
    "ygrave.alt",
    "yhookabove.alt",
    "ytilde.alt",
    "zero.alt",
    "zero.alt.cap",
}


def scrub_designspace(designspace: DesignSpaceDocument, project_root: Path) -> None:
    designspace.loadSourceFonts(ufoLib2.Font.open)
    default_source = designspace.default.font
    glyph_order = [
        n for n in designspace.default.font.glyphOrder if n in default_source.keys()
    ]
    glyph_order_set = set(glyph_order)
    for glyph_name in default_source.keys():
        if glyph_name not in glyph_order_set:
            glyph_order.append(glyph_name)
            glyph_order_set.add(glyph_name)
    postscript_names = {
        k: v
        for k, v in default_source.lib["public.postscriptNames"].items()
        if k in glyph_order_set
    }
    skip_export_glyphs = set(designspace.lib.get("public.skipExportGlyphs", [])).union(
        SKIP_EXPORT_GLYPHS
    )
    rules = designspace.rules

    for source in designspace.sources:
        scrub_source(source, glyph_order, postscript_names, skip_export_glyphs, rules)

    for instance in designspace.instances:
        scrub_instance(instance, project_root)

    designspace.lib = {
        k: v
        for k, v in designspace.lib.items()
        if k.startswith("public.")
        or k.startswith("com.github.googlei18n.ufo2ft.")
        or k == "GSDimensionPlugin.Dimensions"
    }

    if skip_export_glyphs:
        designspace.lib["public.skipExportGlyphs"] = sorted(skip_export_glyphs)


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
    source: SourceDescriptor,
    glyph_order: List[str],
    postscript_names: Dict[str, str],
    skip_export_glyphs: Set[str],
    rules: List[RuleDescriptor],
) -> None:
    scrub_ufo(source.font, glyph_order, postscript_names, skip_export_glyphs, rules)


def scrub_ufo(
    ufo: ufoLib2.Font,
    glyph_order: List[str],
    postscript_names: Dict[str, str],
    skip_export_glyphs: Set[str],
    rules: List[RuleDescriptor],
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

    ufo.lib["public.glyphOrder"] = glyph_order
    ufo.lib["public.postscriptNames"] = postscript_names
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
