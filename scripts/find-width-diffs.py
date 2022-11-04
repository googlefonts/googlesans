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
        for glyph_name in mismatches:
            print(
                f"  {glyph_name}: width is {ufo[glyph_name].width}, but should be {comparison_ufo[glyph_name].width}"
            )
