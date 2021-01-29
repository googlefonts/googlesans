from __future__ import annotations

from typing import Any, Dict, List, Optional

import uharfbuzz as hb


def shape_text(
    font_path: str,
    text: str,
    features: Dict[str, bool],
    variations: Optional[Dict[str, float]] = None,
) -> List[Dict[str, Any]]:
    with open(font_path, "rb") as fontfile:
        fontdata = fontfile.read()

    face = hb.Face(fontdata)
    font = hb.Font(face)
    upem = face.upem
    if variations is not None:
        font.set_variations(variations)

    font.scale = (upem, upem)
    hb.ot_font_set_funcs(font)

    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, features)

    infos = buf.glyph_infos
    positions = buf.glyph_positions

    return [
        {
            "glyph": font.get_glyph_name(info.codepoint),
            "cluster": info.cluster,
            "x_offset": pos.x_offset,
            "y_offset": pos.y_offset,
            "x_advance": pos.x_advance,
            "y_advance": pos.y_advance,
        }
        for info, pos in zip(infos, positions)
    ]


if __name__ == "__main__":
    import argparse
    import json
    from pathlib import Path

    from fontTools.ttLib import TTFont

    parser = argparse.ArgumentParser()
    parser.add_argument("shaping_file", type=Path)
    parser.add_argument("fonts", nargs="+", type=TTFont)
    parsed_args = parser.parse_args()

    shaping_file: Path = parsed_args.shaping_file
    shaping_input = json.loads(shaping_file.read_text())
    shaping_texts = shaping_input["text"]
    shaping_features = shaping_input["features"]

    font: TTFont
    for font in parsed_args.fonts:
        filename = Path(font.reader.file.name)
        if "fvar" in font:
            fvar = font["fvar"]
            result = {}
            for instance in fvar.instances:
                coordinate_str = ",".join(
                    f"{k}={v}" for k, v in instance.coordinates.items()
                )
                result[coordinate_str] = [
                    shape_text(filename, text, shaping_features, instance.coordinates)
                    for text in shaping_texts
                ]
        else:
            result = [
                shape_text(filename, text, shaping_features) for text in shaping_texts
            ]

        shaping_input[filename.name] = result

    shaping_file.write_text(json.dumps(shaping_input, indent=2, ensure_ascii=False))
