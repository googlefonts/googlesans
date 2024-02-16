# Copyright 2024 Google Sans Authors
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

"""
This script checks for source differences, glyph by glyph, between GS sources
from two different branches (they need to be checked out in two folders as per
the constants `RESPACED_DIR` and `TARGET_DIR` below).

The script ignore spacing differences (that is: horizontal translation and
advance width changes) and reports other differences in a spreadsheet format.

The goal is to ensure that Eduardo has only changed spacing, and whenever he's
changed something else, we have an explanation for the change.
"""

from __future__ import annotations
import csv

from ufoLib2 import Font
from ufoLib2.objects import Glyph
from ufoLib2.typing import GlyphSet
from pathlib import Path
from fontTools.pens.recordingPen import DecomposingRecordingPen, RecordingPen
from fontTools.pens.roundingPen import RoundingPen

ROOT_DIR = Path(__file__).parent.parent.parent
RESPACED_DIR = ROOT_DIR / "../googlesans-eduardo/source/GoogleSans"
TARGET_DIR = ROOT_DIR / "../googlesans-mark-weights/source/GoogleSans"

MAIN_UFOS = [
    "GoogleSans-opsz17-wght380-GRAD0.ufo",
    "GoogleSans-opsz17-wght734-GRAD0.ufo",
    "GoogleSans-opsz18-wght380-GRAD0.ufo",
    "GoogleSans-opsz18-wght734-GRAD0.ufo",
    "GoogleSansItalic-opsz17-wght380-GRAD0.ufo",
    "GoogleSansItalic-opsz17-wght734-GRAD0.ufo",
    "GoogleSansItalic-opsz18-wght380-GRAD0.ufo",
    "GoogleSansItalic-opsz18-wght734-GRAD0.ufo",
    "GoogleSans-opsz17-wght380-GRAD-50.ufo",
    "GoogleSans-opsz17-wght380-GRAD200.ufo",
    "GoogleSans-opsz18-wght380-GRAD-50.ufo",
    "GoogleSans-opsz18-wght380-GRAD200.ufo",
    "GoogleSansItalic-opsz17-wght380-GRAD-50.ufo",
    "GoogleSansItalic-opsz17-wght380-GRAD200.ufo",
    "GoogleSansItalic-opsz18-wght380-GRAD-50.ufo",
    "GoogleSansItalic-opsz18-wght380-GRAD200.ufo",
]

EXPECTED_DIFFS = {
    "dje-cy": "The bar moved by one unit to match the GRAD",
    "tshe-cy.sc": "The bar moved by one unit to match the GRAD",
    "elhook-cy": "Moved one leg to make it work in GRAD 200",
    "Elhook-cy": "Moved one leg to make it work in GRAD 200",
    "elhook-cy.sc": "Moved one leg to make it work in GRAD 200",
    "Enghe-cy": "Moved the terminal to make it fit in the GRAD",
    "enghe-cy": "Moved the terminal to make it fit in the GRAD",
    "enghe-cy.sc": "Moved the terminal to make it fit in the GRAD",
    "enlefthook-cy": "Moved one leg to make it work in GRAD",
    "ge-cy": "Moved the terminal to make it fit in GRAD",
    "Ge-cy": "Moved the terminal to make it fit in GRAD",
    "ge-cy.sc": "Moved the terminal to make it fit in GRAD",
    "hahook-cy": "Moved left side to make it work in GRAD",
    "lje-cy": "Moved one leg to make it work in GRAD",
    "te-cy": "Fix symmetry of the arms",
    "upturn-cy": "Adjusted the weight by a couple units to match descenders",
    "upturnlc-cy": "Adjusted the weight by a couple units to match descenders",
    "upturnsc-cy": "Adjusted the weight by a couple units to match descenders",
}

for glyph in """\
        /Chekhakassian-cy
        /Chedescenderabkhasian-cy
        /Eltail-cy
        /Emtail-cy
        /Entail-cy
        /Gedescender-cy
        /Gestrokehook-cy
        /Tedescender-cy
        /chedescender-cy.sc
        /De-cy
        /de-cy
        /de-cy.sc
        /descender-cy
        /descender3-cy
        /descenderlc1-cy
        /descenderlc3-cy
        /descender1sc-cy
        /descender3-cy.sc
        /el-cy
        /eldescender-cy.sc
        /eltail-cy.sc
        /emtail-cy.sc
        /endescender-cy.sc
        /entail-cy.sc
        /gestrokehook-cy.sc
        /ghestroke-cy
        /iishorttail-cy
        /iishorttail-cy.sc
        /pedescender-cy.sc
        /sha-cy
        /shcha-cy.sc
        /Shcha-cy
        /shcha-cy.loclBGR
        /shhadescender-cy
        /shhadescender-cy.sc
        /tail-cy
        /taillc-cy
        /tailsc-cy
        /Tetse-cy
        /tetse-cy
        /tetse-cy.sc
        /Tse-cy
        /tse-cy
        /tse-cy.loclBGR
        /Chedescender-cy
        /Eldescender-cy
        /Endescender-cy
        /Hadescender-cy
        /Kadescender-cy
        /Pedescender-cy
        /Ustraightstroke-cy
        /Zhedescender-cy
        """.strip().split():
    EXPECTED_DIFFS[glyph.lstrip("/")] = "Fixed descender shape"

for glyph in """\
        /Ldot
        /ldot.sc
        /Nine-roman
        /Twelve-roman
        /Eleven-roman
        /pertenthousand
        /ij
        /Iu-cy
        /iu-cy
        /iu-cy.loclBGR
        /iu-cy.sc
        /f_b
        /f_f
        /f_f_b
        /f_f_h
        /f_f_i
        /f_f_j
        /f_f_k
        /f_f_l
        /f_f_t
        /f_h
        /f_i
        /f_j
        /f_k
        /f_l
        /f_t
        /r_f
        /r_f_f
        /r_t
        /t_f
        /t_t
        """.strip().split():
    EXPECTED_DIFFS[glyph.lstrip("/")] = "Fixed spacing inside the ligature"

for glyph in """\
        /idieresis
        /Ustraightstroke-cy
        /yi-cy
        /Abreve
        /abreve.sc
        /abreve.sc
        /Ebreve
        /ebreve.sc
        /ebreve.sc
        /Gbreve
        /gbreve.sc
        /gbreve.sc
        /Ibreve
        /ibreve.sc
        /ibreve.sc
        /Obreve
        /obreve.sc
        /obreve.sc
        /Ubreve
        /ubreve.sc
        /ubreve.sc
        /zhebreve-cy
        /Zhebreve-cy
        /Zhebreve-cy
        """.strip().split():
    EXPECTED_DIFFS[glyph.lstrip("/")] = "Fixed spacing inside the ligature"


def normalise(before: Glyph, layer: GlyphSet, *, decompose: bool) -> Glyph:
    reference_x = min(
        (
            bound
            for bound in (
                before.getLeftMargin(layer),
                min(
                    (
                        bounds[0]
                        for bounds in (
                            component.getControlBounds(layer)
                            for component in before.components
                        )
                        if bounds is not None
                    ),
                    default=None,
                ),
            )
            if bound is not None
        ),
        default=0,
    )

    after = before.copy()
    after.contours = []
    after.components = []

    decomposed = DecomposingRecordingPen(layer) if decompose else RecordingPen()
    before.draw(decomposed)

    after_pen = after.getPen()
    rounding = RoundingPen(after_pen, roundFunc=lambda n: round(n, 2))
    decomposed.replay(rounding)

    after.move((-reference_x, 0))

    return after


def get_other_diffs(
    source: tuple[Glyph, GlyphSet], target: tuple[Glyph, GlyphSet]
) -> dict[str, bool]:
    source_glyph, source_set = source
    target_glyph, target_set = target

    source_glyph = normalise(source_glyph, source_set, decompose=False)
    target_glyph = normalise(target_glyph, target_set, decompose=False)
    source_glyph_decomp = normalise(source_glyph, source_set, decompose=True)
    target_glyph_decomp = normalise(target_glyph, target_set, decompose=True)

    # Allow width to vary, but nothing else
    return {
        "height": source_glyph.height == target_glyph.height,
        "unicodes": source_glyph.unicodes == target_glyph.unicodes,
        "notes": source_glyph.note == target_glyph.note,
        "images": source_glyph.image == target_glyph.image,
        "guidelines": source_glyph.guidelines == target_glyph.guidelines,
        "anchors_names": [a.name for a in source_glyph.anchors]
        == [a.name for a in target_glyph.anchors],
        "anchors": (len(source_glyph.anchors) == len(target_glyph.anchors))
        and all(
            (
                source_anc.x == target_anc.x
                and source_anc.y == target_anc.y
                and source_anc.name == target_anc.name
                and source_anc.color == target_anc.color
                and source_anc.identifier == target_anc.identifier
            )
            for source_anc, target_anc in zip(
                source_glyph.anchors, target_glyph.anchors, strict=True
            )
        ),
        "contours_decomposed": source_glyph_decomp.contours
        == target_glyph_decomp.contours,
        "contours": source_glyph.contours == target_glyph.contours,
        "components": source_glyph.components == target_glyph.components,
        "lib": source_glyph.lib == target_glyph.lib,
    }


def main():
    diffs = []
    for source_ufo_path in (RESPACED_DIR / u for u in MAIN_UFOS):
        print("#", source_ufo_path.stem)
        print()

        target_ufo_path = TARGET_DIR / source_ufo_path.name
        source_ufo = Font.open(source_ufo_path)
        target_ufo = Font.open(target_ufo_path)

        glyphs_in_source = set(source_ufo.keys())
        glyphs_in_target = set(target_ufo.keys())
        print(
            "In source but not in target:", sorted(glyphs_in_source - glyphs_in_target)
        )
        print(
            "In target but not in source:", sorted(glyphs_in_target - glyphs_in_source)
        )
        glyph_names = set(source_ufo.keys()) & set(target_ufo.keys())

        for glyph_name in sorted(glyph_names):
            source_glyph = source_ufo[glyph_name]
            target_glyph = target_ufo[glyph_name]

            differences = get_other_diffs(
                (source_glyph, source_ufo), (target_glyph, target_ufo)
            )

            if not all(differences.values()):
                print(
                    glyph_name,
                    sorted(key for key, is_same in differences.items() if not is_same),
                )
                diffs.append(
                    {
                        "ufo": source_ufo_path.name,
                        "glyph_name": f"/{glyph_name}",
                        **differences,
                        "comment": EXPECTED_DIFFS.get(glyph_name),
                    }
                )

    with open("comparison.csv", "w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(
            fp,
            fieldnames=[
                "ufo",
                "glyph_name",
                "height",
                "unicodes",
                "notes",
                "images",
                "guidelines",
                "anchors_names",
                "anchors",
                "contours",
                "contours_decomposed",
                "components",
                "lib",
                "comment",
            ],
        )
        writer.writeheader()
        for diff in diffs:
            writer.writerow(diff)


if __name__ == "__main__":
    main()
