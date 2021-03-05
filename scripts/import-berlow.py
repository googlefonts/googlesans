# flake8: noqa
# Copyright 2021 Google Sans Authors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid
from pathlib import Path
from typing import List

from ufoLib2 import Font

MAPPING = {
    "Regular/Google Sans-opsz17-wght400-GRAD-50.ufo": "GoogleSans-opsz17-wght380-GRAD-50.ufo",
    "Regular/Google Sans-opsz17-wght400-GRAD0.ufo": "GoogleSans-opsz17-wght380-GRAD0.ufo",
    "Regular/Google Sans-opsz17-wght400-GRAD200.ufo": "GoogleSans-opsz17-wght380-GRAD200.ufo",
    "Regular/Google Sans-opsz17-wght700-GRAD0.ufo": "GoogleSans-opsz17-wght734-GRAD0.ufo",
    "Regular/Google Sans-opsz18-wght400-GRAD-50.ufo": "GoogleSans-opsz18-wght380-GRAD-50.ufo",
    "Regular/Google Sans-opsz18-wght400-GRAD0.ufo": "GoogleSans-opsz18-wght380-GRAD0.ufo",
    "Regular/Google Sans-opsz18-wght400-GRAD200.ufo": "GoogleSans-opsz18-wght380-GRAD200.ufo",
    "Regular/Google Sans-opsz18-wght700-GRAD0.ufo": "GoogleSans-opsz18-wght734-GRAD0.ufo",
    "Italic/Google Sans Italic-opsz17-wght400-GRAD-50.ufo": "GoogleSansItalic-opsz17-wght380-GRAD-50.ufo",
    "Italic/Google Sans Italic-opsz17-wght400-GRAD0.ufo": "GoogleSansItalic-opsz17-wght380-GRAD0.ufo",
    "Italic/Google Sans Italic-opsz17-wght400-GRAD200.ufo": "GoogleSansItalic-opsz17-wght380-GRAD200.ufo",
    "Italic/Google Sans Italic-opsz17-wght700-GRAD0.ufo": "GoogleSansItalic-opsz17-wght734-GRAD0.ufo",
    "Italic/Google Sans Italic-opsz18-wght400-GRAD-50.ufo": "GoogleSansItalic-opsz18-wght380-GRAD-50.ufo",
    "Italic/Google Sans Italic-opsz18-wght400-GRAD0.ufo": "GoogleSansItalic-opsz18-wght380-GRAD0.ufo",
    "Italic/Google Sans Italic-opsz18-wght400-GRAD200.ufo": "GoogleSansItalic-opsz18-wght380-GRAD200.ufo",
    "Italic/Google Sans Italic-opsz18-wght700-GRAD0.ufo": "GoogleSansItalic-opsz18-wght734-GRAD0.ufo",
}

DEFAULT = {
    "GoogleSans-opsz17-wght380-GRAD-50.ufo": "GoogleSans-opsz17-wght380-GRAD0.ufo",
    "GoogleSans-opsz17-wght380-GRAD200.ufo": "GoogleSans-opsz17-wght380-GRAD0.ufo",
    "GoogleSans-opsz18-wght380-GRAD-50.ufo": "GoogleSans-opsz18-wght380-GRAD0.ufo",
    "GoogleSans-opsz18-wght380-GRAD200.ufo": "GoogleSans-opsz18-wght380-GRAD0.ufo",
    "GoogleSansItalic-opsz17-wght380-GRAD-50.ufo": "GoogleSansItalic-opsz17-wght380-GRAD0.ufo",
    "GoogleSansItalic-opsz17-wght380-GRAD200.ufo": "GoogleSansItalic-opsz17-wght380-GRAD0.ufo",
    "GoogleSansItalic-opsz18-wght380-GRAD-50.ufo": "GoogleSansItalic-opsz18-wght380-GRAD0.ufo",
    "GoogleSansItalic-opsz18-wght380-GRAD200.ufo": "GoogleSansItalic-opsz18-wght380-GRAD0.ufo",
}

STYLE_SUFFIX = {
    "GoogleSans-opsz17-wght380-GRAD-50.ufo": "GRAD-50",
    "GoogleSans-opsz17-wght380-GRAD200.ufo": "GRAD200",
    "GoogleSans-opsz18-wght380-GRAD-50.ufo": "GRAD-50",
    "GoogleSans-opsz18-wght380-GRAD200.ufo": "GRAD200",
    "GoogleSansItalic-opsz17-wght380-GRAD-50.ufo": "GRAD-50",
    "GoogleSansItalic-opsz17-wght380-GRAD200.ufo": "GRAD200",
    "GoogleSansItalic-opsz18-wght380-GRAD-50.ufo": "GRAD-50",
    "GoogleSansItalic-opsz18-wght380-GRAD200.ufo": "GRAD200",
}

SOURCE_DIR = Path("../GoogleSans-fb/sources/GS Cubic Sources/")
TARGET_DIR = Path("source/GoogleSans/")

for src, dst in MAPPING.items():
    source = Font(SOURCE_DIR / src)
    if dst in DEFAULT:
        target = Font(TARGET_DIR / DEFAULT[dst])

        layers_to_delete = []
        for layer in target.layers:
            if layer is target.layers.defaultLayer:
                continue
            if layer.name.startswith(("[", "{")) and ".background" not in layer.name:
                continue
            layers_to_delete.append(layer.name)
        for layer_name in layers_to_delete:
            del target.layers[layer_name]

        if target.info.guidelines:
            target.info.guidelines.clear()

        target.info.styleName += " " + STYLE_SUFFIX[dst]
        target.lib["com.schriftgestaltung.fontMasterID"] = str(uuid.uuid4())
    else:
        target = Font(TARGET_DIR / dst)

    # One intentional kerning change for all masters.
    target.kerning[("public.kern1.period", "public.kern2.quoteright")] = -80

    postscript_names_source = source.lib["public.postscriptNames"]
    postscript_names_target = target.lib["public.postscriptNames"]
    for k, v in postscript_names_source.items():
        if v.startswith("uniE"):
            continue  # Skip PUA names
        if k not in postscript_names_target:
            postscript_names_target[k] = v

    glyph_order: List[str] = target.lib["public.glyphOrder"]
    for glyph in source:
        if glyph.name in {
            "finalpedagesh-hb",
            "pedagesh-hb",
            "shindageshshindot-hb",
            "shindageshsindot-hb",
            "shindagesh-hb",
        }:
            # Upstream is better than downstream.
            continue
        # Clear out PUA codepoints.
        if glyph.unicode in range(0xE000, 0xF8FF + 1):
            glyph.unicode = None
        if glyph.name not in target:
            target.layers.defaultLayer.insertGlyph(glyph)
            glyph_order.append(glyph.name)
            continue
        target_glyph = target[glyph.name]
        # if glyph.getLeftMargin(source) != target_glyph.getLeftMargin(target):
        #     logging.warning(f"UFO {src} has different width for ")
        target_glyph.width = glyph.width
        target_glyph.contours = glyph.contours
        target_glyph.components = glyph.components

    target.save(TARGET_DIR / dst, overwrite=True)
