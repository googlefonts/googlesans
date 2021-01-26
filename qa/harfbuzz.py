from typing import Any, Dict, List

import uharfbuzz as hb


def shape_text(
    font_path: str, text_path: str, features: Dict[str, bool]
) -> List[Dict[str, Any]]:
    with open(font_path, "rb") as fontfile:
        fontdata = fontfile.read()

    with open(text_path, "r") as textfile:
        text = textfile.read()

    face = hb.Face(fontdata)
    font = hb.Font(face)
    upem = face.upem

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
    import os
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument("font_path", type=Path)
    parser.add_argument("text_path", type=Path)
    parser.add_argument(
        "--features", help="Comma-separated feature list like `ccmp=true,smcp=false`"
    )
    parsed_args = parser.parse_args()

    font_path = parsed_args.font_path
    text_path = parsed_args.text_path
    features = {}
    if parsed_args.features is not None:
        for s in parsed_args.features.split(","):
            f, t = s.split("=")
            t = True if t == "true" else False
            features[f] = t

    output = shape_text(os.fspath(font_path), os.fspath(text_path), features)

    with open(text_path.with_suffix(".json"), "w+") as f:
        json.dump(output, fp=f, indent=2)
