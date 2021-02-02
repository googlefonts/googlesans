from __future__ import annotations

import enum
from pathlib import Path
from typing import Any, Dict, List, Optional

import uharfbuzz as hb
from fontTools.ttLib import TTFont


class ComparisonMode(enum.Enum):
    FULL = "full"  # Record glyph names, offsets and advance widths.
    GLYPHSTREAM = "glyphstream"  # Just glyph names.


def shape_text(
    font_path: str,
    text: str,
    script: str,
    language: str,
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
    features: Dict[str, bool],
    shaping_comparison_mode: ComparisonMode,
) -> List[Dict[str, Any]]:
    filename = Path(font.reader.file.name)
    return [
        shape_text(filename, text, script, language, features, shaping_comparison_mode)
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
    shaping_input = json.loads(shaping_file.read_text())
    shaping_texts = shaping_input["input"]["text"]
    shaping_features = shaping_input["input"]["features"]
    shaping_script = shaping_input["input"]["script"]
    shaping_language = shaping_input["input"]["language"]
    if "comparison_mode" in shaping_input["input"]:
        shaping_comparison_mode = ComparisonMode(
            shaping_input["input"]["comparison_mode"]
        )
    else:
        shaping_comparison_mode = ComparisonMode.FULL

    if "output" not in shaping_input:
        shaping_input["output"] = {}

    font: TTFont
    for font in parsed_args.fonts:
        filename = Path(font.reader.file.name)
        if "fvar" in font:
            result = shape_variable(
                font,
                shaping_texts,
                shaping_script,
                shaping_language,
                shaping_features,
                shaping_comparison_mode,
            )
        else:
            result = shape_static(
                font,
                shaping_texts,
                shaping_script,
                shaping_language,
                shaping_features,
                shaping_comparison_mode,
            )

        shaping_input["output"][filename.name] = result

    shaping_file.write_text(json.dumps(shaping_input, indent=2, ensure_ascii=False))
