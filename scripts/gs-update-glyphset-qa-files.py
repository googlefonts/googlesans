from pathlib import Path

from fontTools.ttLib import TTFont

for font_path in (
    "build/GoogleSans/static/GoogleSans-Bold.ttf",
    "build/GoogleSans/static/GoogleSans-BoldItalic.ttf",
    "build/GoogleSans/static/GoogleSans-Italic.ttf",
    "build/GoogleSans/static/GoogleSans-Medium.ttf",
    "build/GoogleSans/static/GoogleSans-MediumItalic.ttf",
    "build/GoogleSans/static/GoogleSans-Regular.ttf",
    "build/GoogleSans/static/GoogleSansText-Bold.ttf",
    "build/GoogleSans/static/GoogleSansText-BoldItalic.ttf",
    "build/GoogleSans/static/GoogleSansText-Italic.ttf",
    "build/GoogleSans/static/GoogleSansText-Medium.ttf",
    "build/GoogleSans/static/GoogleSansText-MediumItalic.ttf",
    "build/GoogleSans/static/GoogleSansText-Regular.ttf",
    "build/GoogleSans/variable/GoogleSans-Italic[GRAD,opsz,wght].ttf",
    "build/GoogleSans/variable/GoogleSans[GRAD,opsz,wght].ttf",
):
    font = TTFont(font_path)
    font_glyphsetdef = Path(
        "qa/definitions", Path(font_path).with_suffix(".ttf.glyphsetdef").name
    )
    with open(font_glyphsetdef, "w+") as f:
        f.write("\n".join(font.getGlyphOrder()))
