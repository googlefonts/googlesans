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


DEFAULT_GRADE_UFO_MAP = {
    "GoogleSans-opsz17-wght380-GRAD0.ufo": [
        "GoogleSans-opsz17-wght380-GRAD-50.ufo",
        "GoogleSans-opsz17-wght380-GRAD200.ufo",
    ],
    "GoogleSans-opsz18-wght380-GRAD0.ufo": [
        "GoogleSans-opsz18-wght380-GRAD-50.ufo",
        "GoogleSans-opsz18-wght380-GRAD200.ufo",
    ],
    "GoogleSansItalic-opsz17-wght380-GRAD0.ufo": [
        "GoogleSansItalic-opsz17-wght380-GRAD-50.ufo",
        "GoogleSansItalic-opsz17-wght380-GRAD200.ufo",
    ],
    "GoogleSansItalic-opsz18-wght380-GRAD0.ufo": [
        "GoogleSansItalic-opsz18-wght380-GRAD-50.ufo",
        "GoogleSansItalic-opsz18-wght380-GRAD200.ufo",
    ],
}


TARGET_DIR = Path("source/GoogleSans/")

for src, grad_master_list in DEFAULT_GRADE_UFO_MAP.items():
    default_master = Font(TARGET_DIR / src)
    min_master_path = grad_master_list[0]
    max_master_path = grad_master_list[1]
    min_master = Font(TARGET_DIR / min_master_path)
    max_master = Font(TARGET_DIR / max_master_path)

    for glyph in default_master:
        min_target_glyph = min_master[glyph.name]
        max_target_glyph = max_master[glyph.name]

        if min_target_glyph.width != glyph.width:
            print(
                f"{min_master_path}::{min_target_glyph.name}: "
                f"update width to {glyph.width}"
            )
            # set glyph advance widths to GRAD 0 value
            min_target_glyph.width = glyph.width

        if max_target_glyph.width != glyph.width:
            print(
                f"{max_master_path}::{max_target_glyph.name}: "
                f"update width to {glyph.width}"
            )
            max_target_glyph.width = glyph.width

    min_master.save(TARGET_DIR / min_master_path, overwrite=True)
    max_master.save(TARGET_DIR / max_master_path, overwrite=True)
