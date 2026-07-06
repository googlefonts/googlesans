"""Unit tests for merge_variable_fea.py (the feaLib-AST merge)."""

import io

import pytest
from fontTools.feaLib import ast
from fontTools.feaLib.parser import Parser

import merge_variable_fea as mvf

GLYPHS = {"a", "b", "c", "x", "y", "f_i", "acutecomb", "gravecomb", "uni0041", "uni0042"}


def _parse(text, glyphs=GLYPHS):
    return Parser(io.StringIO(text), glyphNames=glyphs).parse().statements


def merge(fragments, locations, glyphs=GLYPHS):
    """Parse each fragment string, merge, return the reference master's asFea."""
    masters = [_parse(f, glyphs) for f in fragments]
    locs = [mvf.parse_location(s) for s in locations]
    mvf.merge_level(masters, locs, "root")
    out = ast.FeatureFile()
    out.statements = masters[0]
    return out.asFea()


class TestParseLocation:
    def test_integers(self):
        assert mvf.parse_location("opsz=18,wght=400") == {"opsz": 18, "wght": 400}

    def test_float_kept_when_not_integral(self):
        assert mvf.parse_location("wght=400.5") == {"wght": 400.5}

    def test_integral_float_coerced_to_int(self):
        assert mvf.parse_location("wght=400.0") == {"wght": 400}

    def test_missing_equals_raises(self):
        with pytest.raises(ValueError):
            mvf.parse_location("opsz18")


class TestSignature:
    def test_differing_values_same_signature(self):
        a = _parse("feature kern { pos a b -40; } kern;")[0].statements[0]
        b = _parse("feature kern { pos a b -60; } kern;")[0].statements[0]
        assert mvf.signature(a) == mvf.signature(b)

    def test_glyph_class_order_ignored(self):
        a = _parse("feature kern { pos [a b c] x -1; } kern;")[0].statements[0]
        b = _parse("feature kern { pos [c b a] x -1; } kern;")[0].statements[0]
        assert mvf.signature(a) == mvf.signature(b)

    def test_different_glyphs_differ(self):
        a = _parse("feature kern { pos a b -1; } kern;")[0].statements[0]
        b = _parse("feature kern { pos a c -1; } kern;")[0].statements[0]
        assert mvf.signature(a) != mvf.signature(b)

    def test_glyph_names_differing_only_by_digit_differ(self):
        # Regression: signature blanks values by zeroing the ValueRecord, not by
        # blanking digits in text, so digits inside glyph names are preserved.
        a = _parse("feature kern { pos uni0041 b -1; } kern;")[0].statements[0]
        b = _parse("feature kern { pos uni0042 b -1; } kern;")[0].statements[0]
        assert mvf.signature(a) != mvf.signature(b)


class TestHolderSlots:
    def test_anchor_slots(self):
        assert mvf.holder_slots(ast.Anchor(1, 2)) == ("x", "y")

    def test_value_record_slots(self):
        assert mvf.holder_slots(ast.ValueRecord(xAdvance=5)) == (
            "xPlacement",
            "yPlacement",
            "xAdvance",
            "yAdvance",
        )

    def test_contourpoint_anchor_raises(self):
        with pytest.raises(ValueError, match="contourpoint"):
            mvf.holder_slots(ast.Anchor(1, 2, contourpoint=3))


class TestAlignedMerge:
    def test_equal_value_stays_plain(self):
        out = merge(["feature kern { pos a b -40; } kern;"] * 2, ["opsz=18", "opsz=17"])
        assert "pos a b -40;" in out
        assert "opsz=18:" not in out

    def test_differing_value_becomes_variable_scalar(self):
        out = merge(
            [
                "feature kern { pos a b -40; } kern;",
                "feature kern { pos a b -60; } kern;",
            ],
            ["opsz=18", "opsz=17"],
        )
        assert "pos a b (opsz=18:-40 opsz=17:-60);" in out

    def test_value_record_fields_merge_independently(self):
        out = merge(
            [
                "feature kern { pos a b <10 20 30 40>; } kern;",
                "feature kern { pos a b <10 25 30 45>; } kern;",
            ],
            ["opsz=18", "opsz=17"],
        )
        # xPlacement(10) and xAdvance(30) equal -> plain; y fields differ -> scalar
        assert "(opsz=18:20 opsz=17:25)" in out
        assert "(opsz=18:40 opsz=17:45)" in out

    def test_anchor_coords_merge(self):
        frag = (
            "feature mark {{ markClass acutecomb <anchor 0 500> @TOP;"
            " pos base a <anchor {x} 600> mark @TOP; }} mark;"
        )
        out = merge([frag.format(x=250), frag.format(x=240)], ["opsz=18", "opsz=17"])
        assert "(opsz=18:250 opsz=17:240)" in out

    def test_shared_null_anchor_passes_through(self):
        # A NULL ligature component every master agrees on carries no value to
        # variabilize; it is kept verbatim while the real anchor still merges.
        frag = (
            "feature mark {{ markClass acutecomb <anchor 0 500> @TOP;"
            " pos ligature f_i <anchor {x} 600> mark @TOP"
            " ligComponent <anchor NULL>; }} mark;"
        )
        out = merge([frag.format(x=100), frag.format(x=120)], ["opsz=18", "opsz=17"])
        assert "<anchor NULL>" in out
        assert "(opsz=18:100 opsz=17:120)" in out

    def test_cursive_anchors_merge(self):
        frag = (
            "feature curs {{ pos cursive [a b] <anchor {e} 0> <anchor 50 -10>; }} curs;"
        )
        out = merge([frag.format(e=100), frag.format(e=110)], ["opsz=18", "opsz=17"])
        assert "(opsz=18:100 opsz=17:110)" in out  # entry x varied
        assert "<anchor 50 -10>" in out  # exit unchanged

    def test_cursive_null_entry_shared_passes_through(self):
        # An open (NULL) entry anchor every master shares carries no value; the
        # real exit anchor still merges.
        frag = (
            "feature curs {{ pos cursive [a b] <anchor NULL> <anchor {x} -10>; }} curs;"
        )
        out = merge([frag.format(x=50), frag.format(x=60)], ["opsz=18", "opsz=17"])
        assert "<anchor NULL>" in out
        assert "(opsz=18:50 opsz=17:60)" in out

    def test_ligature_carets_merge(self):
        frag = "table GDEF {{ LigatureCaretByPos f_i {a} 500; }} GDEF;"
        out = merge([frag.format(a=400), frag.format(a=420)], ["opsz=18", "opsz=17"])
        assert "LigatureCaretByPos f_i (opsz=18:400 opsz=17:420) 500;" in out

    def test_ligature_caret_equal_stays_plain(self):
        out = merge(
            ["table GDEF { LigatureCaretByPos f_i 400 500; } GDEF;"] * 2,
            ["opsz=18", "opsz=17"],
        )
        assert "LigatureCaretByPos f_i 400 500;" in out
        assert "opsz=18:" not in out

    def test_multiline_statement_merges_correctly(self):
        # The motivating bug: a pos split across physical lines. The line-oriented
        # regex merge silently freezes the continuation value; the AST merge does
        # not, because the value comes from the ValueRecord, not the line.
        out = merge(
            [
                "feature kern {\n  pos a b\n    -40;\n} kern;",
                "feature kern {\n  pos a b\n    -60;\n} kern;",
            ],
            ["opsz=18", "opsz=17"],
        )
        assert "pos a b (opsz=18:-40 opsz=17:-60);" in out

    def test_comments_preserved(self):
        out = merge(
            ["feature kern {\n  # keep me\n  pos a b -40;\n} kern;"] * 2,
            ["opsz=18", "opsz=17"],
        )
        assert "# keep me" in out

    def test_comment_divergence_does_not_block_merge(self):
        out = merge(
            [
                "feature kern {\n  # one\n  pos a b -40;\n} kern;",
                "feature kern {\n  # two\n  pos a b -60;\n} kern;",
            ],
            ["opsz=18", "opsz=17"],
        )
        assert "pos a b (opsz=18:-40 opsz=17:-60);" in out


class TestLoudFailures:
    def test_statement_count_mismatch(self):
        with pytest.raises(ValueError, match="count mismatch"):
            merge(
                [
                    "feature kern { pos a b -1; pos a c -1; } kern;",
                    "feature kern { pos a b -1; } kern;",
                ],
                ["opsz=18", "opsz=17"],
            )

    def test_structure_mismatch(self):
        with pytest.raises(ValueError, match="structure mismatch"):
            merge(
                [
                    "feature kern { pos a b -1; } kern;",
                    "feature kern { pos a c -1; } kern;",
                ],
                ["opsz=18", "opsz=17"],
            )

    def test_glyph_digit_difference_fails_loud(self):
        # Masters differing only by a digit in a glyph name must not be silently
        # mis-merged (the old text-blanking signature would have aligned them).
        with pytest.raises(ValueError, match="structure mismatch"):
            merge(
                [
                    "feature kern { pos uni0041 b -40; } kern;",
                    "feature kern { pos uni0042 b -60; } kern;",
                ],
                ["opsz=18", "opsz=17"],
            )

    def test_null_anchor_divergent_fails(self):
        # NULL in one master but positioned in another is not expressible: the
        # statement's structure differs, so the alignment check rejects it.
        null = (
            "feature mark { markClass acutecomb <anchor 0 500> @TOP;"
            " pos ligature f_i <anchor 100 600> mark @TOP"
            " ligComponent <anchor NULL>; } mark;"
        )
        real = (
            "feature mark { markClass acutecomb <anchor 0 500> @TOP;"
            " pos ligature f_i <anchor 100 600> mark @TOP"
            " ligComponent <anchor 5 5> mark @TOP; } mark;"
        )
        with pytest.raises(ValueError, match="structure mismatch"):
            merge([null, real], ["opsz=18", "opsz=17"])

    def test_ligature_caret_by_index_not_variabilized(self):
        # Caret indices reference contour points; a differing index is a real
        # structural difference, not a coordinate to interpolate -> fail loud.
        with pytest.raises(ValueError, match="structure mismatch"):
            merge(
                [
                    "table GDEF { LigatureCaretByIndex f_i 7; } GDEF;",
                    "table GDEF { LigatureCaretByIndex f_i 9; } GDEF;",
                ],
                ["opsz=18", "opsz=17"],
            )

    def test_ligature_caret_count_guard(self):
        # Defensive: unequal caret counts are rejected by the alignment gate first
        # (blanked carets serialize differently), so exercise the merge guard.
        with pytest.raises(ValueError, match="caret count mismatch"):
            mvf.merge_caret_lists(
                [[400, 500], [400]], [{"opsz": 18}, {"opsz": 17}], "root"
            )

    def test_divergent_class_substitution_fails(self):
        # One-to-one class subs are order-significant (a->x, b->y); reordered source
        # classes encode a different mapping and must not be silently flattened by
        # the glyph-class sort, which is skipped for substitutions.
        with pytest.raises(ValueError, match="structure mismatch"):
            merge(
                [
                    "feature ss01 { sub [a b] by [x y]; } ss01;",
                    "feature ss01 { sub [b a] by [x y]; } ss01;",
                ],
                ["opsz=18", "opsz=17"],
            )

    def test_value_present_in_some_only(self):
        # Defensive guard: a numeric slot set in one master but absent in another
        # (unreachable through the alignment gate, since differing value-record
        # shapes fail the structure check first, so exercise it directly).
        h0 = [ast.ValueRecord(xAdvance=10)]
        h1 = [ast.ValueRecord(xAdvance=10, yAdvance=5)]
        with pytest.raises(ValueError, match="present in some"):
            mvf.merge_holder_lists([h0, h1], [{"opsz": 18}, {"opsz": 17}], "root")


class TestMarkClassCanonicalization:
    def test_split_on_divergent_anchor(self):
        # A groups [a b]@100; B splits a@100 b@200 -> b must become variable.
        out = merge(
            [
                "feature t { markClass [a b] <anchor 100 0> @C; } t;",
                "feature t { markClass [a] <anchor 100 0> @C;"
                " markClass [b] <anchor 200 0> @C; } t;",
            ],
            ["opsz=18", "opsz=17"],
        )
        assert "markClass [a] <anchor 100 0> @C;" in out
        assert "markClass [b] <anchor (opsz=18:100 opsz=17:200) 0> @C;" in out

    def test_regroup_keeps_group_when_uniform(self):
        # A grouped; B as two stmts but uniform anchor -> reconcile to one group.
        out = merge(
            [
                "feature t { markClass [a b] <anchor 100 0> @C; } t;",
                "feature t { markClass [a] <anchor 150 0> @C;"
                " markClass [b] <anchor 150 0> @C; } t;",
            ],
            ["opsz=18", "opsz=17"],
        )
        assert "markClass [a b] <anchor (opsz=18:100 opsz=17:150) 0> @C;" in out

    def test_contourpoint_anchor_fails_not_dropped(self):
        # Reconciled anchors are rebuilt from x/y only; a contourpoint must be
        # rejected, not silently dropped in the rebuild.
        with pytest.raises(ValueError, match="contourpoint"):
            merge(
                [
                    "feature t { markClass [a b] <anchor 1 0 contourpoint 2> @C; } t;",
                    "feature t { markClass [a] <anchor 1 0 contourpoint 2> @C;"
                    " markClass [b] <anchor 2 0 contourpoint 2> @C; } t;",
                ],
                ["opsz=18", "opsz=17"],
            )

    def test_device_table_anchor_fails_not_dropped(self):
        dev1 = "<anchor 100 0 <device 11 1> <device NULL>>"
        dev2 = "<anchor 200 0 <device 11 1> <device NULL>>"
        with pytest.raises(ValueError, match="device"):
            merge(
                [
                    f"feature t {{ markClass [a b] {dev1} @C; }} t;",
                    f"feature t {{ markClass [a] {dev1} @C;"
                    f" markClass [b] {dev2} @C; }} t;",
                ],
                ["opsz=18", "opsz=17"],
            )

    def test_divergent_keys_fail_loud(self):
        with pytest.raises(ValueError, match="diverges structurally"):
            merge(
                [
                    "feature t { markClass [a b] <anchor 100 0> @C; } t;",
                    "feature t { markClass [a] <anchor 100 0> @C; } t;",
                ],
                ["opsz=18", "opsz=17"],
            )

    def test_noncontiguous_divergent_block_fails(self):
        # markClass run interrupted by a pos statement, AND grouping diverges.
        with pytest.raises(ValueError, match="not contiguous"):
            merge(
                [
                    "feature t { markClass [a b] <anchor 1 0> @C; pos x y -1; } t;",
                    "feature t { markClass [a] <anchor 1 0> @C; pos x y -1;"
                    " markClass [b] <anchor 2 0> @C; } t;",
                ],
                ["opsz=18", "opsz=17"],
            )

    def test_block_present_in_some_only(self):
        with pytest.raises(ValueError, match="present in some"):
            merge(
                [
                    "feature t { markClass [a] <anchor 1 0> @C; pos x y -1; } t;",
                    "feature t { pos x y -1; pos x a -1; } t;",
                ],
                ["opsz=18", "opsz=17"],
            )


class TestIntegration:
    def test_three_masters(self):
        out = merge(
            [
                "feature kern { pos a b -40; } kern;",
                "feature kern { pos a b -50; } kern;",
                "feature kern { pos a b -60; } kern;",
            ],
            ["opsz=18", "opsz=17", "opsz=16"],
        )
        assert "(opsz=18:-40 opsz=17:-50 opsz=16:-60)" in out
