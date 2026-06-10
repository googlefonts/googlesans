#!/usr/bin/env python3
r"""Merge per-master FEA files into a single variable FEA via the feaLib AST.

Given N feature files, one per designspace master, emit one feature file in which
numeric values that differ across masters become feaLib variable scalars
'(axis=val:num ...)', while values equal at every master stay plain numbers.

Rather than line/regex manipulation, each per-master fragment is parsed into a
feaLib AST; the parallel statement trees are walked together, and any numeric
leaf -- a ValueRecord field (x/y placement, x/y advance), an Anchor coordinate,
or a ligature caret position -- that differs across masters is replaced by a
VariableScalar populated per master location. The reference (first) master's tree
is then serialized with asFea().

Parse context
-------------
feaLib has to fully parse each input before it can be merged: that needs the glyph
set, and -- when an input is an include fragment rather than a self-contained file
-- the sibling files that define its context. GoogleSans' per-master Telugu/Arabic
inputs are such fragments: never compiled standalone, only pulled into an assembled
features.fea after the files that define their context. They reference glyphs by
name (hyphenated names like 'kha-telugu.below' look like FEA glyph ranges to the
parser unless it knows the glyph set) and may reference glyph classes defined in
sibling files (Telugu's @TEL_* live in telugu.fea). So:

  --ufo PATH        default-master UFO; its glyph names are handed to the parser
                    so hyphenated names aren't misread as ranges (required).
  --context FILE..  .fea files prepended as include(...) before each fragment so
                    feaLib can resolve external @classes (e.g. telugu.fea). The
                    context's own statements are discarded; only each fragment's
                    statements are merged. Self-contained inputs need none; among
                    the GoogleSans inputs Arabic needs none, Telugu needs
                    telugu.fea. Includes are resolved against --include-dir,
                    which defaults to the directory of the first input file.

Reconciled divergences
-----------------------
Inputs must hold the same statements in the same order, with two divergences
reconciled automatically (mirroring the structure feaLib already models):
  - glyph classes are unordered, so masters whose '[...]' contents are reordered
    still match; the reference master's order is kept in the output;
  - the markClass block may group glyphs differently across masters (two glyphs
    that share an anchor in one master can be collapsed into one statement). It is
    decomposed per (class, glyph) and re-emitted in the reference layout, keeping a
    group intact unless its glyphs carry different anchors in some master, in which
    case it is split. Requires the markClass statements to be contiguous *when*
    they diverge; an already-aligned block (the common case) is merged in place and
    may be non-contiguous. This reconciliation is defensive: the current GoogleSans
    masters are already aligned (identical grouping), so it engages only if future
    generated fragments group glyphs differently.

Comments (including Glyphs' '# Automatic Code' markers) are preserved; the parser
keeps them and asFea() re-emits them. Input order does not affect merged values
(scalars are keyed by location); the first file only sets the reference layout, so
pass the default master first.

Anything variable FEA cannot express -- a differing set of statements, markClass
entries that don't match across masters, device tables, or contourpoint anchors --
fails loudly rather than silently emitting a wrong font. A NULL anchor (a ligature
component with no attachment) carries no value to variabilize: when every master
agrees on it, it passes through unchanged; a slot that is NULL in some masters but
positioned in others is a structure mismatch and fails loud.

Usage (the GoogleSans Telugu/Arabic variable features, run from the repo root;
--include-dir defaults to the fragment directory, so --context resolves there):

    python scripts/merge_variable_fea.py \
        source/GoogleSans/telugu-opsz18-wght380.fea \
        source/GoogleSans/telugu-opsz18-wght734.fea \
        source/GoogleSans/telugu-opsz17-wght380.fea \
        source/GoogleSans/telugu-opsz17-wght734.fea \
        -l "opsz=18,wght=400" "opsz=18,wght=700" "opsz=17,wght=400" "opsz=17,wght=700" \
        --ufo source/GoogleSans/GoogleSans-opsz18-wght380-GRAD0.ufo \
        --context telugu.fea \
        -o source/GoogleSans/telugu-variable.fea

    python scripts/merge_variable_fea.py \
        source/GoogleSans/arabic-opsz18-wght380.fea \
        source/GoogleSans/arabic-opsz18-wght734.fea \
        source/GoogleSans/arabic-opsz17-wght380.fea \
        source/GoogleSans/arabic-opsz17-wght734.fea \
        -l "opsz=18,wght=400" "opsz=18,wght=700" "opsz=17,wght=400" "opsz=17,wght=700" \
        --ufo source/GoogleSans/GoogleSans-opsz18-wght380-GRAD0.ufo \
        -o source/GoogleSans/arabic-variable.fea

Telugu-Italic mirrors the Telugu command with the italic per-master fragments and
--ufo source/GoogleSans/GoogleSansItalic-opsz18-wght380-GRAD0.ufo.
"""

import argparse
import io
import os
import re

from fontTools.feaLib import ast
from fontTools.feaLib.parser import Parser
from fontTools.feaLib.variableScalar import VariableScalar
from fontTools.ufoLib import UFOReader

ANCHOR_SLOTS = ("x", "y")
VALUEREC_SLOTS = ("xPlacement", "yPlacement", "xAdvance", "yAdvance")
DEVICE_SLOTS = ("xPlaDevice", "yPlaDevice", "xAdvDevice", "yAdvDevice")

_GLYPH_CLASS_RE = re.compile(r"\[([^\]]+)\]")


def parse_location(spec: str) -> dict:
    """'opsz=18,wght=400' -> {'opsz': 18, 'wght': 400} (int where integral)."""
    loc = {}
    for part in spec.split(","):
        tag, sep, val = part.partition("=")
        if not sep:
            raise ValueError(f"bad location component {part!r} in {spec!r}")
        f = float(val)
        loc[tag.strip()] = int(f) if f.is_integer() else f
    return loc


def glyph_names_from_ufo(ufo_path: str) -> set:
    return set(UFOReader(ufo_path).getGlyphSet().keys())


def parse_master(
    frag_path: str, glyph_names: set, context: list, include_dir: str
) -> list:
    """Parse one fragment with prepended context includes; return only the
    fragment's own top-level statements (context statements sliced off)."""
    preamble = "".join(f"include({c});\n" for c in context)
    n_ctx = 0
    if context:
        ctx_tree = Parser(
            io.StringIO(preamble), glyphNames=glyph_names, includeDir=include_dir
        ).parse()
        n_ctx = len(ctx_tree.statements)
    with open(frag_path) as f:
        text = f.read()
    full = Parser(
        io.StringIO(preamble + text), glyphNames=glyph_names, includeDir=include_dir
    ).parse()
    return full.statements[n_ctx:]


def meaningful(stmts: list) -> list:
    """Statements that carry structure/values (standalone comments dropped from
    pairing; they remain in the reference tree and so in the output)."""
    return [s for s in stmts if not isinstance(s, ast.Comment)]


def is_block(node) -> bool:
    return hasattr(node, "statements") and isinstance(node.statements, list)


def block_header(node) -> tuple:
    """Block identity independent of its body (and its body's comments)."""
    return (
        type(node).__name__,
        getattr(node, "name", None),
        getattr(node, "use_extension", None),
    )


def signature(stmt) -> str:
    """Equality skeleton for a leaf statement: the statement serialized with its
    numeric values neutralized, leaving structure and glyph operands. Only the
    values are blanked -- the ValueRecord/Anchor fields are zeroed around the
    asFea() call, then restored -- so glyph names keep their digits (a statement
    differing only in a glyph differs here). Glyph-class member order is normalized
    (the bracketed run is sorted in the serialized text) so masters that reorder a
    class still match -- except in substitutions, where a class's order can be
    significant (one-to-one class subs), so those are left as-is and a reorder
    fails loud rather than being silently flattened."""
    saved = []
    for h in value_holders(stmt):
        if isinstance(h, ast.Anchor):
            slots = ANCHOR_SLOTS
        elif isinstance(h, ast.ValueRecord):
            slots = VALUEREC_SLOTS
        else:
            slots = ()
        for slot in slots:
            v = getattr(h, slot)
            if v is not None:
                saved.append((h, slot, v))
                setattr(h, slot, 0)
    carets = caret_holder(stmt)
    saved_carets = list(carets) if carets is not None else None
    if carets is not None:
        carets[:] = [0] * len(carets)
    try:
        s = stmt.asFea()
    finally:
        for h, slot, v in saved:
            setattr(h, slot, v)
        if carets is not None and saved_carets is not None:
            carets[:] = saved_carets
    if "Subst" in type(stmt).__name__:
        return s  # class order can be significant in a one-to-one sub; don't touch
    return _GLYPH_CLASS_RE.sub(
        lambda m: "[" + " ".join(sorted(m.group(1).split())) + "]", s
    )


def shape(node) -> tuple:
    """Per-statement alignment key: block header, or leaf signature."""
    if is_block(node):
        return block_header(node)
    return ("leaf", signature(node))


def aligned(mlists: list) -> bool:
    """True if every master has the same statement shapes in the same order."""
    shapes = [tuple(shape(s) for s in ml) for ml in mlists]
    return all(s == shapes[0] for s in shapes)


def value_holders(stmt) -> list:
    """Ordered Anchor/ValueRecord objects carrying mergeable numerics in `stmt`
    itself (not its child statements). [] for purely structural statements;
    ligature-caret positions are bare numbers, not holder objects, and are merged
    separately via caret_holder()."""
    tn = type(stmt).__name__
    if tn == "MarkClassDefinition":
        return [stmt.anchor]
    if tn in ("MarkBasePosStatement", "MarkMarkPosStatement"):
        return [anc for anc, _ in stmt.marks]
    if tn == "MarkLigPosStatement":
        return [anc for comp in stmt.marks for anc, _ in (comp or [])]
    if tn == "CursivePosStatement":
        # entry/exit anchors; either may be NULL (None) for an open connection.
        return [a for a in (stmt.entryAnchor, stmt.exitAnchor) if a is not None]
    if tn == "SinglePosStatement":
        return [vr for _, vr in stmt.pos]
    if tn == "PairPosStatement":
        return [vr for vr in (stmt.valuerecord1, stmt.valuerecord2) if vr is not None]
    if tn == "ValueRecordDefinition":
        return [stmt.value]
    return []


def holder_slots(h) -> tuple:
    """Numeric slot names on a value holder; raises on shapes the merge can't
    express (device tables, contourpoint anchors). NULL anchors never reach here:
    feaLib parses '<anchor NULL>' to a value-less component, so value_holders
    yields no holder for it. An anchor that is NULL in every master is dropped and
    passes through unchanged; one that is NULL in some masters but positioned in
    others changes the statement's asFea and fails the alignment check upstream."""
    if isinstance(h, ast.Anchor):
        if h.contourpoint is not None:
            raise ValueError("contourpoint anchor not supported")
        if h.xDeviceTable is not None or h.yDeviceTable is not None:
            raise ValueError("anchor device table not supported")
        return ANCHOR_SLOTS
    if isinstance(h, ast.ValueRecord):
        if any(getattr(h, d, None) is not None for d in DEVICE_SLOTS):
            raise ValueError("value record device table not supported")
        return VALUEREC_SLOTS
    raise TypeError(f"unexpected value holder {type(h).__name__}")


def caret_holder(stmt):
    """The mutable list of ligature-caret X-coordinates for a LigatureCaretByPos
    statement (coordinates, mergeable like any other), else None.

    LigatureCaretByIndex is deliberately excluded: its carets are contour-point
    indices, which name a point rather than a coordinate and so do not interpolate
    -- a differing index is a real structural difference, not a value to merge, and
    is caught by the alignment check (signature does not blank it)."""
    if type(stmt).__name__ == "LigatureCaretByPosStatement":
        return stmt.carets
    return None


def _variabilize(vals: list, locations: list, where: str):
    """One numeric value per master for a single slot. Returns a VariableScalar to
    write when the masters disagree, or None to leave the slot untouched (every
    master equal, or the slot is unset in every master). Raises if the slot is set
    in some masters but not others, or if an input is already a variable scalar."""
    present = [v is not None for v in vals]
    if any(present) and not all(present):
        raise ValueError(f"{where}: present in some masters but not others")
    if vals[0] is None:
        return None
    if any(isinstance(v, VariableScalar) for v in vals):
        raise ValueError(f"{where}: input already contains a variable scalar")
    if len(set(vals)) > 1:
        vs = VariableScalar()
        for loc, val in zip(locations, vals):
            vs.add_value(loc, val)
        return vs
    return None


def merge_holder_lists(holders_per_master: list, locations: list, where: str):
    """Merge parallel holders, mutating the reference master's holders: a numeric
    slot that differs across masters becomes a VariableScalar."""
    ref = holders_per_master[0]
    for i, h0 in enumerate(ref):
        for slot in holder_slots(h0):
            vals = [getattr(hpm[i], slot) for hpm in holders_per_master]
            vs = _variabilize(vals, locations, f"{where}: {slot}")
            if vs is not None:
                setattr(h0, slot, vs)


def merge_caret_lists(carets_per_master: list, locations: list, where: str):
    """Merge parallel ligature-caret lists, mutating the reference master's list: a
    caret position that differs across masters becomes a VariableScalar."""
    ref = carets_per_master[0]
    if len({len(c) for c in carets_per_master}) != 1:
        raise ValueError(f"{where}: ligature caret count mismatch")
    for i in range(len(ref)):
        vals = [c[i] for c in carets_per_master]
        vs = _variabilize(vals, locations, f"{where}: caret {i + 1}")
        if vs is not None:
            ref[i] = vs


def _markclass_run(stmts: list):
    """(lo, hi) inclusive span covering every MarkClassDefinition among `stmts`,
    or None if there are none. Comments may sit inside the run; any other kind of
    statement between two markClass defs means the block is non-contiguous."""
    idxs = [i for i, s in enumerate(stmts) if isinstance(s, ast.MarkClassDefinition)]
    if not idxs:
        return None
    lo, hi = idxs[0], idxs[-1]
    for i in range(lo, hi + 1):
        if not isinstance(stmts[i], (ast.MarkClassDefinition, ast.Comment)):
            raise ValueError(
                "markClass statements are not contiguous; cannot "
                "reconcile grouping divergence"
            )
    return lo, hi


def _glyph_set(container) -> tuple:
    """Glyph names of a feaLib glyph container (GlyphName/GlyphClass/...)."""
    return tuple(container.glyphSet())


def _decompose_run(run: list):
    """run -> ({(class, glyph): Anchor}, [(class, [glyphs])], {class: MarkClass})."""
    entries, groups, classes = {}, [], {}
    for s in run:
        if not isinstance(s, ast.MarkClassDefinition):
            continue
        # the reconciled anchors are rebuilt from x/y only; an anchor carrying
        # more (contourpoint, device tables) must fail loud, not drop it silently
        holder_slots(s.anchor)
        cls = s.markClass.name
        classes[cls] = s.markClass
        glyphs = list(_glyph_set(s.glyphs))
        for g in glyphs:
            if (cls, g) in entries:
                raise ValueError(f"glyph {g} defined twice in @{cls}")
            entries[(cls, g)] = s.anchor
        groups.append((cls, glyphs))
    return entries, groups, classes


def canonicalize_markclass_level(real_lists: list, where: str):
    """Reconcile markClass grouping divergence at one statement level: rewrite
    every master's markClass run in place to the reference master's grouping,
    splitting a group only where its glyphs' anchors diverge within some master.
    Anchors stay per-master; the positional merge that follows variabilizes them.
    """
    bounds = [_markclass_run(rl) for rl in real_lists]
    if all(b is None for b in bounds):
        return
    if any(b is None for b in bounds):
        raise ValueError(
            f"{where}: markClass block present in some masters but not others"
        )
    spans = [b for b in bounds if b is not None]  # all non-None past the guards

    decomp = [_decompose_run(rl[lo:hi + 1]) for rl, (lo, hi) in zip(real_lists, spans)]
    keysets = [set(d[0]) for d in decomp]
    if any(k != keysets[0] for k in keysets):
        union = set().union(*keysets)
        diverging = sorted(f"@{c} {g}" for c, g in union - set.intersection(*keysets))
        raise ValueError(
            f"{where}: markClass diverges structurally (not mergeable); differing "
            f"entries include: {', '.join(diverging[:8])}"
        )

    entries = [d[0] for d in decomp]
    ref_groups, classes = decomp[0][1], decomp[0][2]
    n = len(real_lists)
    rebuilt = [[] for _ in range(n)]
    for cls, glyphs in ref_groups:
        uniform = all(
            len({(entries[mi][(cls, g)].x, entries[mi][(cls, g)].y) for g in glyphs}) == 1
            for mi in range(n)
        )
        emit = [glyphs] if uniform else [[g] for g in glyphs]
        for grp in emit:
            for mi in range(n):
                a = entries[mi][(cls, grp[0])]
                rebuilt[mi].append(
                    ast.MarkClassDefinition(
                        classes[cls], ast.Anchor(a.x, a.y), ast.GlyphClass(list(grp))
                    )
                )
    for mi, (rl, (lo, hi)) in enumerate(zip(real_lists, spans)):
        rl[lo:hi + 1] = rebuilt[mi]


def merge_level(real_lists: list, locations: list, where: str):
    """Merge parallel statement lists for one level, recursing into blocks.
    Mutates the reference master's nodes (and, on divergence, every master's
    markClass run) in place."""
    mlists = [meaningful(rl) for rl in real_lists]
    if not aligned(mlists):
        if any(any(isinstance(s, ast.MarkClassDefinition) for s in ml) for ml in mlists):
            canonicalize_markclass_level(real_lists, where)
            mlists = [meaningful(rl) for rl in real_lists]
        if not aligned(mlists):
            counts = [len(ml) for ml in mlists]
            if len(set(counts)) != 1:
                raise ValueError(f"{where}: statement count mismatch: {counts}")
            for i, nodes in enumerate(zip(*mlists)):
                if len({shape(n) for n in nodes}) != 1:
                    raise ValueError(
                        f"{where}: statement {i + 1} structure mismatch:\n  "
                        + "\n  ".join(sorted({signature(n).strip()[:120] for n in nodes}))
                    )

    ref = mlists[0]
    for i, node0 in enumerate(ref):
        nodes = [ml[i] for ml in mlists]
        if is_block(node0):
            merge_level(
                [n.statements for n in nodes],
                locations,
                f"{where} > {block_header(node0)[1] or block_header(node0)[0]}",
            )
        else:
            where_i = f"{where} statement {i + 1}"
            holders = [value_holders(n) for n in nodes]
            if len({len(h) for h in holders}) != 1:
                raise ValueError(
                    f"{where}: value-holder count mismatch at statement {i + 1}"
                )
            if holders[0]:
                merge_holder_lists(holders, locations, where_i)
            carets = [caret_holder(n) for n in nodes]
            if carets[0] is not None:
                merge_caret_lists(carets, locations, where_i)


def merge_files(
    input_files: list,
    output_file: str,
    locations: list,
    ufo: str,
    context: list,
    include_dir=None,
):
    if len(input_files) != len(locations):
        raise ValueError("number of files must match number of locations")
    # include() in the prepended --context is resolved relative to this; default
    # to the fragment's own directory so the common case needs no --include-dir.
    if include_dir is None:
        include_dir = os.path.dirname(input_files[0]) or "."
    glyph_names = glyph_names_from_ufo(ufo)
    locs = [parse_location(s) for s in locations]
    masters = [parse_master(f, glyph_names, context, include_dir) for f in input_files]
    merge_level(masters, locs, "root")

    out = ast.FeatureFile()
    out.statements = masters[0]
    text = out.asFea()
    if not text.endswith("\n"):
        text += "\n"
    with open(output_file, "w") as f:
        f.write(text)

    first_axis = locations[0].split(",")[0].split("=")[0]
    n_scalars = text.count("(" + first_axis + "=")
    print(
        f"Merged {len(input_files)} masters -> {output_file}; "
        f"{n_scalars} variable scalars"
    )


def main():
    p = argparse.ArgumentParser(
        description="Merge per-master FEA into variable FEA (feaLib AST)"
    )
    p.add_argument("files", nargs="+", help="per-master input FEA fragments")
    p.add_argument("-o", "--output", required=True, help="output FEA file")
    p.add_argument(
        "-l",
        "--locations",
        nargs="+",
        required=True,
        help='userspace location per file, e.g. "opsz=18,wght=400"; '
        "same count and order as the input files",
    )
    p.add_argument(
        "--ufo",
        required=True,
        help="default-master UFO (its glyph names disambiguate "
        "hyphenated names from glyph ranges)",
    )
    p.add_argument(
        "--context",
        nargs="*",
        default=[],
        metavar="FEA",
        help="context .fea files to include before each fragment "
        "(define external @classes); their statements are dropped",
    )
    p.add_argument(
        "--include-dir",
        default=None,
        help="directory feaLib resolves include() against "
        "(default: the first input file's directory)",
    )
    args = p.parse_args()
    if len(args.files) != len(args.locations):
        p.error("number of files must match number of locations")
    merge_files(
        args.files, args.output, args.locations, args.ufo, args.context, args.include_dir
    )


if __name__ == "__main__":
    main()
