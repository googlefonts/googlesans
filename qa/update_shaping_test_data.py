from __future__ import annotations

import enum
from pathlib import Path
from typing import Dict, List, Optional, Union

import uharfbuzz as hb
from fontTools.ttLib import TTFont


class ComparisonMode(enum.Enum):
    FULL = "full"  # Record glyph names, offsets and advance widths.
    GLYPHSTREAM = "glyphstream"  # Just glyph names.


class Direction(enum.Enum):
    LTR = "ltr"
    RTL = "rtl"
    TTB = "ttb"
    BTT = "btt"


def shape_run(
    hb_face: hb.Face,
    text: str,
    script: Optional[str],
    language: Optional[str],
    direction: Direction,
    features: Dict[str, bool],
    shaping_comparison_mode: ComparisonMode,
    variations: Optional[Dict[str, float]] = None,
) -> str:
    font = hb.Font(hb_face)
    upem = hb_face.upem
    if variations is not None:
        font.set_variations(variations)

    font.scale = (upem, upem)
    hb.ot_font_set_funcs(font)

    buf = hb.Buffer()
    buf.add_str(text)
    buf.direction = direction.value
    if script is not None:
        buf.script = script
    if language is not None:
        buf.language = language
    buf.guess_segment_properties()
    hb.shape(font, buf, features)

    infos = buf.glyph_infos
    positions = buf.glyph_positions

    if shaping_comparison_mode is ComparisonMode.FULL:
        out = []
        for info, pos in zip(infos, positions):
            s = f"{font.get_glyph_name(info.codepoint)}={info.cluster}"
            if pos.x_offset or pos.y_offset:
                s += f"@{pos.x_offset},{pos.y_offset}"
            if pos.x_advance or pos.y_advance:
                s += f"+{pos.x_advance},{pos.y_advance}"
            out.append(s)
        return "|".join(out)
    elif shaping_comparison_mode is ComparisonMode.GLYPHSTREAM:
        return "|".join(font.get_glyph_name(info.codepoint) for info in infos)
    else:
        raise ValueError(f"Unknown comparison mode {shaping_comparison_mode}.")


def shape_texts(
    font: TTFont,
    hb_face: hb.Face,
    texts: List[str],
    script: Optional[str],
    language: Optional[str],
    direction: Direction,
    features: Dict[str, bool],
    shaping_comparison_mode: ComparisonMode,
) -> Union[Dict[str, List[str]], List[str]]:
    if "fvar" in font:
        result = {}
        for instance in font["fvar"].instances:
            coordinate_str = ",".join(
                f"{k}={v}" for k, v in instance.coordinates.items()
            )
            result[coordinate_str] = [
                shape_run(
                    hb_face,
                    text,
                    script,
                    language,
                    direction,
                    features,
                    shaping_comparison_mode,
                    instance.coordinates,
                )
                for text in texts
            ]
        return result
    else:
        return [
            shape_run(
                hb_face,
                text,
                script,
                language,
                direction,
                features,
                shaping_comparison_mode,
            )
            for text in texts
        ]


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("shaping_file", type=Path)
    parser.add_argument("fonts", nargs="+", type=TTFont)
    parsed_args = parser.parse_args()

    shaping_file: Path = parsed_args.shaping_file
    shaping_input_doc = json.loads(shaping_file.read_text())
    shaping_input = shaping_input_doc["input"]
    shaping_texts = shaping_input["text"]
    shaping_features = shaping_input["features"]
    shaping_script = shaping_input.get("script")
    shaping_language = shaping_input.get("language")
    shaping_comparison_mode = ComparisonMode(
        shaping_input.get("comparison_mode", "full")
    )
    shaping_direction = Direction(shaping_input.get("direction", "ltr"))

    if "output" not in shaping_input_doc:
        shaping_input_doc["output"] = {}

    font: TTFont
    for font in parsed_args.fonts:
        filename = Path(font.reader.file.name)
        with open(filename, "rb") as fontfile:
            hb_face = hb.Face(fontfile.read())
        shaping_input_doc["output"][filename.name] = shape_texts(
            font,
            hb_face,
            shaping_texts,
            shaping_script,
            shaping_language,
            shaping_direction,
            shaping_features,
            shaping_comparison_mode,
        )

    shaping_file.write_text(json.dumps(shaping_input_doc, indent=2, ensure_ascii=False))
