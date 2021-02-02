from __future__ import annotations

import enum
from pathlib import Path
from typing import Any, Dict, List, Optional

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


def shape_text(
    font_path: str,
    text: str,
    script: str,
    language: str,
    direction: Direction,
    features: Dict[str, bool],
    shaping_comparison_mode: ComparisonMode,
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
    buf.direction = direction.value
    buf.script = script
    buf.language = language
    buf.guess_segment_properties()
    hb.shape(font, buf, features)

    infos = buf.glyph_infos
    positions = buf.glyph_positions

    if shaping_comparison_mode is ComparisonMode.FULL:
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
    elif shaping_comparison_mode is ComparisonMode.GLYPHSTREAM:
        return [font.get_glyph_name(info.codepoint) for info in infos]
    else:
        raise ValueError(f"Unknown comparison mode {shaping_comparison_mode}.")


def shape_variable(
    font: TTFont,
    texts: List[str],
    script: str,
    language: str,
    direction: Direction,
    features: Dict[str, bool],
    shaping_comparison_mode: ComparisonMode,
) -> Dict[str, List[Dict[str, Any]]]:
    filename = Path(font.reader.file.name)
    fvar = font["fvar"]
    result = {}
    for instance in fvar.instances:
        coordinate_str = ",".join(f"{k}={v}" for k, v in instance.coordinates.items())
        result[coordinate_str] = [
            shape_text(
                filename,
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


def shape_static(
    font: TTFont,
    texts: List[str],
    script: str,
    language: str,
    direction: Direction,
    features: Dict[str, bool],
    shaping_comparison_mode: ComparisonMode,
) -> List[Dict[str, Any]]:
    filename = Path(font.reader.file.name)
    return [
        shape_text(
            filename,
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
    shaping_script = shaping_input["script"]
    shaping_language = shaping_input["language"]
    shaping_comparison_mode = ComparisonMode(
        shaping_input.get("comparison_mode", "full")
    )
    shaping_direction = Direction(shaping_input.get("direction", "ltr"))

    if "output" not in shaping_input_doc:
        shaping_input_doc["output"] = {}

    font: TTFont
    for font in parsed_args.fonts:
        filename = Path(font.reader.file.name)
        if "fvar" in font:
            result = shape_variable(
                font,
                shaping_texts,
                shaping_script,
                shaping_language,
                shaping_direction,
                shaping_features,
                shaping_comparison_mode,
            )
        else:
            result = shape_static(
                font,
                shaping_texts,
                shaping_script,
                shaping_language,
                shaping_direction,
                shaping_features,
                shaping_comparison_mode,
            )

        shaping_input_doc["output"][filename.name] = result

    shaping_file.write_text(json.dumps(shaping_input_doc, indent=2, ensure_ascii=False))
