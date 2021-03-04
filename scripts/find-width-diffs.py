from pathlib import Path

from ufoLib2 import Font


TARGET_DIR = Path("source/GoogleSans/")
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

comparison_ufos = {}

for ufo_path, comparison_ufo_path in DEFAULT.items():
    ufo = Font.open(TARGET_DIR / ufo_path)
    if comparison_ufo_path in comparison_ufos:
        comparison_ufo = comparison_ufos[comparison_ufo_path]
    else:
        comparison_ufo = Font.open(TARGET_DIR / comparison_ufo_path)
        comparison_ufos[comparison_ufo_path] = comparison_ufo

    mismatches = [
        glyph.name for glyph in ufo if glyph.width != comparison_ufo[glyph.name].width
    ]
    if mismatches:
        print(f"UFO {ufo_path} width mismatches compared to {comparison_ufo_path}:")
        print("\n".join(f"  {x}" for x in mismatches))
