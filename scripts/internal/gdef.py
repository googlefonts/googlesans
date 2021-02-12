import textwrap
from typing import List

from glyphsLib.builder.constants import GLYPHLIB_PREFIX


# TODO: Move this information into
# https://unifiedfontobject.org/versions/ufo3/lib.plist/#publicopentypecategories
KNOWN_BASES = {
    "k_ssa-deva",
    "j_nya-deva",
    "k_ss-deva",
    "k_ss-deva.alt2",
    "k_ss-deva.alt3",
    "k_ss-deva.alt4",
    "k_ss-deva.alt5",
    "k_ss-deva.alt6",
    "k_ss-deva.alt7",
    "j_ny-deva",
    "j_ny-deva.alt2",
    "j_ny-deva.alt3",
    "j_ny-deva.alt4",
    "j_ny-deva.alt5",
    "j_ny-deva.alt6",
    "j_ny-deva.alt7",
    "j_ny-deva.alt8",
    "ng_ya-deva",
    "ch_ya-deva",
    "tt_tta-deva",
    "tt_ttha-deva",
    "tt_ya-deva",
    "tth_ttha-deva",
    "tth_ya-deva",
    "dd_dda-deva",
    "dd_ddha-deva",
    "dd_ya-deva",
    "ddh_ddha-deva",
    "ddh_ya-deva",
    "t_ta-deva",
    "t_ra-deva",
    "d_ga-deva",
    "d_gha-deva",
    "d_da-deva",
    "d_dha-deva",
    "d_dh_ya-deva",
    "d_ba-deva",
    "d_bha-deva",
    "d_ma-deva",
    "d_ya-deva",
    "d_ra-deva",
    "d_va-deva",
    "p_ta-deva",
    "sh_ra-deva",
    "ss_tta-deva",
    "ss_ttha-deva",
    "h_nna-deva",
    "h_na-deva",
    "h_ma-deva",
    "h_ya-deva",
    "h_ra-deva",
    "h_la-deva",
    "h_va-deva",
    "h_ra_uMatra-deva",
    "h_ra_uuMatra-deva",
}


# Lifted from glyphsLib v5.2.0 and made to return a list of str for splicing
# (also wrapped glyph name lists for easier diffing).
def build_gdef(ufo, skipExportGlyphs=None) -> List[str]:
    """Build a GDEF table statement (GlyphClassDef and LigatureCaretByPos).
    Building GlyphClassDef requires anchor propagation or user care to work as
    expected, as Glyphs.app also looks at anchors for classification:
    * Base: any glyph that has an attaching anchor (such as "top"; "_top" does
      not count) and is neither classified as Ligature nor Mark using the
      definitions below;
    * Ligature: if subCategory is "Ligature" and the glyph has at least one
      attaching anchor;
    * Mark: if category is "Mark" and subCategory is either "Nonspacing" or
      "Spacing Combining";
    * Compound: never assigned by Glyphs.app.
    See:
    * https://github.com/googlefonts/glyphsLib/issues/85
    * https://github.com/googlefonts/glyphsLib/pull/100#issuecomment-275430289
    """
    from glyphsLib import glyphdata

    bases, ligatures, marks, carets = set(), set(), set(), {}
    category_key = GLYPHLIB_PREFIX + "category"
    subCategory_key = GLYPHLIB_PREFIX + "subCategory"

    for glyph in ufo:
        # Do not generate any entries for non-export glyphs, as looking them up on
        # compilation will fail.
        if skipExportGlyphs is not None:
            if glyph.name in skipExportGlyphs:
                continue

        has_attaching_anchor = False
        for anchor in glyph.anchors:
            name = anchor.name
            if name and not name.startswith("_"):
                has_attaching_anchor = True
            if name and name.startswith("caret_") and "x" in anchor:
                carets.setdefault(glyph.name, []).append(round(anchor["x"]))

        # First check glyph.lib for category/subCategory overrides. Otherwise,
        # use global values from GlyphData.
        glyphinfo = glyphdata.get_glyph(glyph.name)
        category = glyph.lib.get(category_key) or glyphinfo.category
        subCategory = glyph.lib.get(subCategory_key) or glyphinfo.subCategory

        if glyph.name in KNOWN_BASES:
            bases.add(glyph.name)
        elif subCategory == "Ligature" and has_attaching_anchor:
            ligatures.add(glyph.name)
        elif category == "Mark" and (
            subCategory == "Nonspacing" or subCategory == "Spacing Combining"
        ):
            marks.add(glyph.name)
        elif has_attaching_anchor:
            bases.add(glyph.name)

    if not any((bases, ligatures, marks, carets)):
        return None

    def sortkey(glyph_name):
        try:
            return ufo.glyphOrder.index(glyph_name), glyph_name
        except ValueError:
            return len(ufo.glyphOrder), glyph_name

    def fmt(glyphs):
        return ("[%s]" % " ".join(sorted(glyphs, key=sortkey))) if glyphs else ""

    lines = [
        "table GDEF {",
        "  # automatic",
        "  GlyphClassDef",
        "    %s, # Base"
        % "\n".join(
            textwrap.wrap(
                fmt(bases),
                width=88,
                break_on_hyphens=False,
                break_long_words=False,
                initial_indent="    ",
                subsequent_indent=2 * "    ",
            )
        ),
        "    %s, # Liga"
        % "\n".join(
            textwrap.wrap(
                fmt(ligatures),
                width=88,
                break_on_hyphens=False,
                break_long_words=False,
                initial_indent="    ",
                subsequent_indent=2 * "    ",
            )
        ),
        "    %s, # Mark"
        % "\n".join(
            textwrap.wrap(
                fmt(marks),
                width=88,
                break_on_hyphens=False,
                break_long_words=False,
                initial_indent="    ",
                subsequent_indent=2 * "    ",
            )
        ),
        "    ;",
    ]
    for glyph, caretPos in sorted(carets.items()):
        lines.append(
            "  LigatureCaretByPos %s %s;"
            % (glyph, " ".join(str(p) for p in sorted(caretPos)))
        )
    lines.append("} GDEF;")

    return lines
