from pathlib import Path

from fontTools.ttLib import TTFont

for font_path in (
    "build/GoogleSans/static/expert/GoogleSans-Bold.ttf",
    "build/GoogleSans/static/expert/GoogleSans-BoldItalic.ttf",
    "build/GoogleSans/static/expert/GoogleSans-Italic.ttf",
    "build/GoogleSans/static/expert/GoogleSans-Medium.ttf",
    "build/GoogleSans/static/expert/GoogleSans-MediumItalic.ttf",
    "build/GoogleSans/static/expert/GoogleSans-Regular.ttf",
    "build/GoogleSans/static/expert/GoogleSansText-Bold.ttf",
    "build/GoogleSans/static/expert/GoogleSansText-BoldItalic.ttf",
    "build/GoogleSans/static/expert/GoogleSansText-Italic.ttf",
    "build/GoogleSans/static/expert/GoogleSansText-Medium.ttf",
    "build/GoogleSans/static/expert/GoogleSansText-MediumItalic.ttf",
    "build/GoogleSans/static/expert/GoogleSansText-Regular.ttf",
    "build/GoogleSans/variable/expert/GoogleSans-Italic[opsz,wght].ttf",
    "build/GoogleSans/variable/expert/GoogleSans[opsz,wght].ttf",
):
    font = TTFont(font_path)
    font_glyphsetdef = Path(
        "qa/definitions", Path(font_path).with_suffix(".ttf.glyphsetdef").name
    )
    with open(font_glyphsetdef, "w+") as f:
        f.write("\n".join(font.getGlyphOrder()))
