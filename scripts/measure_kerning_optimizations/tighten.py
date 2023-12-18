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

import collections
from graphlib import TopologicalSorter

from fontTools.designspaceLib import DesignSpaceDocument
from ufoLib2.objects import Font, Glyph

from . import drop_kerning


def drop_and_tighten(designspace: DesignSpaceDocument) -> DesignSpaceDocument:
    designspace = drop_kerning.drop_threshold(designspace, 10)
    for source in designspace.sources:
        tighten(source.font, 1)
    return designspace


def tighten(font: Font, units: float) -> None:
    # Build a cache of what glyphs are used as components where, to keep them
    # in place when moving the base.
    glyph_graph = {}
    composite_graph: collections.defaultdict[str, set[str]]
    composite_graph = collections.defaultdict(set)
    for g in font:
        if g.name is None:
            continue
        glyph_graph[g.name] = set()
        for c in g.components:
            glyph_graph[g.name].add(c.baseGlyph)
            composite_graph[c.baseGlyph].add(g.name)

    # Make sure outline glyphs are first in the list, then those that use these
    # outlines as components, then those that use these composite glyphs as
    # components etc. This ensures changing bearings does not change glyphs
    # we already processed.
    ts = TopologicalSorter(glyph_graph)
    for glyph_name in tuple(ts.static_order()):
        glyph = font[glyph_name]
        if not should_tighten_glyph(font, glyph):
            continue
        left_before = glyph.getLeftMargin(font)
        set_left_margin_rounded(glyph, int(left_before - units), font)
        set_right_margin_rounded(glyph, int(glyph.getRightMargin(font) - units), font)

        # If the glyph is used as a component in any other glyph, move that component
        # in the opposite direction (measured to the left, to the origin) to ensure
        # that existing components stay in place.
        if glyph_name in composite_graph:
            left_after = glyph.getLeftMargin(font)
            assert left_after is not None
            left_diff = left_before - left_after
            if isinstance(left_diff, float) and left_diff.is_integer():
                left_diff = round(left_diff)
            if not left_diff:
                continue
            for composite_name in composite_graph[glyph_name]:
                composite = font[composite_name]
                for c in composite.components:
                    if c.baseGlyph != glyph_name:
                        continue
                    c.transformation = c.transformation.translate(left_diff, 0)


def set_left_margin_rounded(glyph: Glyph, value: float, layer=None) -> None:
    """Sets the the rounded space in font units from the point of origin to the
    left side of the glyph.
    Args:
        value: The desired left margin in font units.
        layer: The layer of the glyph to look up components, if any. Not needed for
            pure-contour glyphs.
    """
    bounds = glyph.getBounds(layer)
    if bounds is None:
        return None
    diff = round(value - bounds.xMin)
    if diff:
        glyph.width += diff
        glyph.move((diff, 0))


def set_right_margin_rounded(glyph: Glyph, value: float, layer=None) -> None:
    """Sets the the rounded space in font units from the glyph's advance width to
    the right side of the glyph.
    Args:
        value: The desired right margin in font units.
        layer: The layer of the glyph to look up components, if any. Not needed for
            pure-contour glyphs.
    """
    bounds = glyph.getBounds(layer)
    if bounds is None:
        return None
    glyph.width = round(bounds.xMax + value)


EXCEPTIONS = frozenset(
    """\
G.super
one.sansSerifCircled
two.sansSerifCircled
three.sansSerifCircled
four.sansSerifCircled
five.sansSerifCircled
six.sansSerifCircled
seven.sansSerifCircled
eight.sansSerifCircled
nine.sansSerifCircled
one.sansSerifBlackCircled
two.sansSerifBlackCircled
three.sansSerifBlackCircled
four.sansSerifBlackCircled
five.sansSerifBlackCircled
six.sansSerifBlackCircled
seven.sansSerifBlackCircled
eight.sansSerifBlackCircled
nine.sansSerifBlackCircled
zero.tf
one.tf
two.tf
three.tf
four.tf
five.tf
six.tf
seven.tf
eight.tf
nine.tf
slash
backslash
period.tf
comma.tf
colon.tf
semicolon.tf
numbersign.tf
endash
emdash
horizontalbar
underscore
endash.cap
emdash.cap
emquad
emspace
enquad
enspace
figurespace
hairspace
punctuationspace
sixperemspace
nbspace
thinspace
threeperemspace
zerowidthspace
space.tf
CR
.notdef
cent.tf
currency.tf
dollar.tf
dong.tf
euro.tf
florin.tf
franc.tf
hryvnia.tf
lira.tf
liraTurkish.tf
peso.tf
ruble.tf
rupeeIndian.tf
sterling.tf
tenge.tf
tugrik.tf
won.tf
yen.tf
divisionslash
plus.tf
minus.tf
multiply.tf
divide.tf
equal.tf
notequal.tf
greater.tf
less.tf
greaterequal.tf
lessequal.tf
plusminus.tf
approxequal.tf
logicalnot.tf
percent.tf
replacementCharacter
copyright.alt
registered.alt
published.alt
section.tf
peace
whiteFrowningFace
whiteSmilingFace
apple
dieresiscomb
dotaccentcomb
gravecomb
acutecomb
hungarumlautcomb
caroncomb.alt
circumflexcomb
caroncomb
brevecomb
ringcomb
tildecomb
macroncomb
hookabovecomb
commaturnedabovecomb
horncomb
dotbelowcomb
dieresisbelowcomb
commaaccentcomb
cedillacomb
ogonekcomb
brevebelowcomb
macronbelowcomb
dieresis
dotaccent
grave
acute
hungarumlaut
circumflex
caron
breve
ring
tilde
macron
cedilla
ogonek
cedillacomb.alt
caron.alt
cedilla.alt
dieresiscomb.cap
dotaccentcomb.cap
gravecomb.cap
acutecomb.cap
hungarumlautcomb.cap
caroncomb.alt.cap
circumflexcomb.cap
caroncomb.cap
brevecomb.cap
ringcomb.cap
tildecomb.cap
macroncomb.cap
hookabovecomb.cap
horncomb.cap
dieresiscomb.sc
dotaccentcomb.sc
gravecomb.sc
acutecomb.sc
hungarumlautcomb.sc
circumflexcomb.sc
caroncomb.sc
brevecomb.sc
ringcomb.sc
tildecomb.sc
macroncomb.sc
hookabovecomb.sc
tonos
dieresistonos
brevecomb_acutecomb.sc
brevecomb_gravecomb.sc
brevecomb_hookabovecomb.sc
brevecomb_tildecomb.sc
circumflexcomb_acutecomb.sc
circumflexcomb_gravecomb.sc
circumflexcomb_hookabovecomb.sc
circumflexcomb_tildecomb.sc
uni0002
uni0009
Glogo
ologo
glogo
llogo
elogo
Gsuper
Googlelogo
uniE007
NULL
Google.logo
__descender-cy.case
__descender-cy
sheqel.tf
shindot-hb
etnahtaleft-hb
segolta-hb
shalshelet-hb
zaqefqatan-hb
zaqefgadol-hb
tipehaleft-hb
reviamugrash-hb
zarqa-hb
pashta-hb
yetiv-hb
tevirleft-hb
gereshaccent-hb
gereshmuqdam-hb
gershayimaccent-hb
qarneypara-hb
telishagedola-hb
pazer-hb
atnahhafukh-hb
munahleft-hb
mahapakhleft-hb
merkhaleft-hb
merkhakefulaleft-hb
dargaleft-hb
qadma-hb
telishaqetana-hb
yerahbenyomoleft-hb
ole-hb
iluy-hb
dehi-hb
zinor-hb
masoracircle-hb
sheva-hb
hatafsegol-hb
hatafsegol_siluqleft-hb
hatafpatah-hb
hatafpatah_siluqleft-hb
hatafqamats-hb
hatafqamats_siluqleft-hb
hiriq-hb
tsere-hb
segol-hb
patah-hb
qamats-hb
holam-hb
holamhaser-hb
qubuts-hb
dagesh-hb
dagesh-hb.alt
siluqleft-hb
rafe-hb
sindot-hb
upperdot-hb
lowerdot-hb
qamatsqatan-hb
judeospanishvarika-hb
segolta-hb.final
telishaqetana-hb.final
masoracircle-hb.final
apostrophemod
dram-arm
dram-arm.cap
dram-arm.tf
eternity-arm-lf
eternity-arm-rf
emphasis-arm.comb
exclam-arm.comb
question-arm.comb
emphasis-arm.cap.comb
exclam-arm.cap.comb
question-arm.cap.comb
zerowidthjoiner
zerowidthnonjoiner
candraBindu-deva
anusvara-deva
nukta-deva
halant-deva
oeMatra-deva
uMatra-deva
uuMatra-deva
rVocalicMatra-deva
rrVocalicMatra-deva
lVocalicMatra-deva
llVocalicMatra-deva
eCandraMatra-deva
eShortMatra-deva
eMatra-deva
aiMatra-deva
eLongCandra-deva
ueMatra-deva
uueMatra-deva
reph-deva
rakar-deva
rakar-deva.diagonal
rakar-deva.short
uMatra-deva.alt
uMatra-deva.narrow
uuMatra-deva.alt
eMatra-deva.narrow
eMatra_anusvara-deva
eMatra_candraBindu-deva
eMatra_reph-deva
eMatra_reph_anusvara-deva
aiMatra_anusvara-deva
aiMatra_candraBindu-deva
aiMatra_reph-deva
aiMatra_reph_anusvara-deva
eCandraMatra_anusvara-deva
eCandraMatra_reph-deva
eShortMatra_anusvara-deva
eShortMatra_candraBindu-deva
eShortMatra_reph-deva
eShortMatra_reph_anusvara-deva
reph_anusvara-deva
commaaccentcomb.BRACKET.18
commaturnedabovecomb.BRACKET.18
percent
pertenthousand
perthousand
percent.cap
pertenthousand.cap
perthousand.cap
upArrow
northEastArrow
rightArrow
southEastArrow
downArrow
southWestArrow
leftArrow
northWestArrow
rightOverLeftArrow
upArrow.ss05
northEastArrow.ss05
rightArrow.ss05
southEastArrow.ss05
downArrow.ss05
southWestArrow.ss05
leftArrow.ss05
northWestArrow.ss05
blackCircle
whiteCircle
lozenge
blackSquare
whiteSquare
upBlackTriangle
upWhiteTriangle
checkmark
multiplicationX
heavySingleTurnedCommaQuotationMarkOrnament
heavySingleCommaQuotationMarkOrnament
heavyDoubleTurnedCommaQuotationMarkOrnament
heavyDoubleCommaQuotationMarkOrnament
copyright
registered
published
G.logo
e.logo
g.logo
l.logo
o.logo
brevecomb_acutecomb
brevecomb_gravecomb
brevecomb_hookabovecomb
brevecomb_tildecomb
circumflexcomb_acutecomb
circumflexcomb_gravecomb
circumflexcomb_hookabovecomb
circumflexcomb_tildecomb
brevecomb_acutecomb.cap
brevecomb_gravecomb.cap
brevecomb_hookabovecomb.cap
brevecomb_tildecomb.cap
circumflexcomb_acutecomb.cap
circumflexcomb_gravecomb.cap
circumflexcomb_hookabovecomb.cap
circumflexcomb_tildecomb.cap
brevecombcy.sc
brevecombcy.cap
brevecombcy
U-ogonekcomb
Uogonekcomb
asteriskcomb
emphasis-arm.short.comb
exclam-arm.short.comb
question-arm.short.comb
emphasis-arm.comb.sc
exclam-arm.comb.sc
question-arm.comb.sc
emphasis-arm.short.comb.sc
exclam-arm.short.comb.sc
question-arm.short.comb.sc
""".splitlines()
)


def should_tighten_glyph(font: Font, glyph: Glyph) -> bool:
    if not glyph.contours and not glyph.components:
        return False
    if glyph.width == 0:
        return False
    if glyph.name in EXCEPTIONS:
        return False
    return True
