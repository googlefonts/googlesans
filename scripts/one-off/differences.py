from pathlib import Path

from fontTools.designspaceLib import DesignSpaceDocument
from ufoLib2 import Font
from ufoLib2.objects import Glyph, Layer
from fontTools.pens.recordingPen import DecomposingRecordingPointPen

SKIP = [
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
    "percentbar",
    "question",
    "radical",
    "slash",
    "dottedCircle",
]

# Define sources and targets.
ds_from = DesignSpaceDocument.fromfile(
    Path("..", "googlesans-arabic", "masters", "GoogleSansArabic.designspace")
)
ds_to = DesignSpaceDocument.fromfile(
    Path("source", "GoogleSans", "GoogleSans.designspace")
)

ds_from.loadSourceFonts(Font.open)
ds_to.loadSourceFonts(Font.open)

name_to_tag = {
    **{axis.name: axis.tag for axis in ds_from.axes},
    **{axis.name: axis.tag for axis in ds_to.axes},
}

defaults_to = {axis.tag: axis.default for axis in ds_to.axes}

statuses = {}


def normalise_spacing(glyph: Glyph, layer: Layer) -> Glyph:
    glyph = glyph.copy()

    left = glyph.getLeftMargin(layer)
    bottom = glyph.getBottomMargin(layer)

    if left is None or bottom is None:
        return glyph

    glyph.move((-left, -bottom))
    return glyph


def draws_the_same(
    *, before: Glyph, layer_before: Layer, after: Glyph, layer_after: Layer
) -> bool:
    pen_before = DecomposingRecordingPointPen(layer_before)
    before.drawPoints(pen_before)

    pen_after = DecomposingRecordingPointPen(layer_after)
    after.drawPoints(pen_after)

    return pen_before.value == pen_after.value


for source_from in ds_from.sources:
    assert isinstance(source_from.font, Font)
    assert source_from.layerName is None, "unexpected sparse layer"

    loc_from = {
        name_to_tag[name]: value
        for name, value in source_from.getFullDesignLocation(ds_from).items()
    }

    for source_to in ds_to.sources:
        assert isinstance(source_to.font, Font)
        if source_to.layerName is not None:
            continue

        loc_to = {
            name_to_tag[name]: value
            for name, value in source_to.getFullDesignLocation(ds_to).items()
        }
        matches = all(
            loc_from.get(tag, defaults_to[tag]) == loc_to[tag] for tag in loc_to
        )

        if not matches:
            continue

        layer_from = source_from.font.layers.defaultLayer
        layer_to = source_to.font.layers.defaultLayer

        for glyph_name in SKIP:
            glyph_from = layer_from[glyph_name]
            glyph_to = layer_to[glyph_name]

            if draws_the_same(
                before=normalise_spacing(glyph_from, layer_from),
                layer_before=layer_from,
                after=normalise_spacing(glyph_to, layer_to),
                layer_after=layer_to,
            ):
                if draws_the_same(
                    before=glyph_from,
                    layer_before=layer_from,
                    after=glyph_to,
                    layer_after=layer_to,
                ):
                    if glyph_from.width != glyph_to.width:
                        status = "different width"
                    else:
                        status = "same"
                else:
                    status = "different spacing"
            else:
                status = "different outlines"
            statuses.setdefault(glyph_name, {}).setdefault(status, []).append(
                sorted(list(source_to.location.items()))
            )
            # statuses.setdefault(glyph_name, set()).add(status)

for glyph in SKIP:
    print(f'"{glyph}":', statuses[glyph], sep=" ")
