# Copyright 2021 Google Sans Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Update the GDEF definition in the feature file.

We want our own because Glyphs has the habit of propagating anchors on
_everything_, even symbols that happen to contain components of latin
glyphs with anchors.
"""

# pyright: basic

from typing import Dict, Optional

import glyphsLib.builder.constants
import glyphsLib.glyphdata
import ufoLib2

KNOWN_BASES = {
    "k_ssa-deva",
    "j_nya-deva",
    "k_ss-deva",
    "k_ss-deva.alt2",
    "k_ss-deva.alt3",
    "k_ss-deva.alt4",
    "k_ss-deva.alt5",
    "k_ss-deva.alt6",
    "k_ss-deva.alt7",
    "j_ny-deva",
    "j_ny-deva.alt2",
    "j_ny-deva.alt3",
    "j_ny-deva.alt4",
    "j_ny-deva.alt5",
    "j_ny-deva.alt6",
    "j_ny-deva.alt7",
    "j_ny-deva.alt8",
    "ng_ya-deva",
    "ch_ya-deva",
    "tt_tta-deva",
    "tt_ttha-deva",
    "tt_ya-deva",
    "tth_ttha-deva",
    "tth_ya-deva",
    "dd_dda-deva",
    "dd_ddha-deva",
    "dd_ya-deva",
    "ddh_ddha-deva",
    "ddh_ya-deva",
    "t_ta-deva",
    "t_ra-deva",
    "d_ga-deva",
    "d_gha-deva",
    "d_da-deva",
    "d_dha-deva",
    "d_dh_ya-deva",
    "d_ba-deva",
    "d_bha-deva",
    "d_ma-deva",
    "d_ya-deva",
    "d_ra-deva",
    "d_va-deva",
    "p_ta-deva",
    "sh_ra-deva",
    "ss_tta-deva",
    "ss_ttha-deva",
    "h_nna-deva",
    "h_na-deva",
    "h_ma-deva",
    "h_ya-deva",
    "h_ra-deva",
    "h_la-deva",
    "h_va-deva",
    "h_ra_uMatra-deva",
    "h_ra_uuMatra-deva",
}


def update_opentype_categories(ufo: ufoLib2.Font) -> Dict[str, str]:
    """Returns a `public.openTypeCategories` dictionary.

    Building it requires anchor propagation or user care to work as
    expected, as Glyphs.app also looks at anchors for classification:

    * base: any glyph that has an attaching anchor (such as "top"; "_top" does
      not count) and is neither classified as Ligature nor Mark using the
      definitions below;
    * ligature: if subCategory is "Ligature" and the glyph has at least one
      attaching anchor;
    * mark: if category is "Mark" and subCategory is either "Nonspacing" or
      "Spacing Combining";
    * composite: never assigned by Glyphs.app.

    See:

    * https://github.com/googlefonts/glyphsLib/issues/85
    * https://github.com/googlefonts/glyphsLib/pull/100#issuecomment-275430289
    """

    # Drop glyphs that don't exist in font anymore.
    existing: Dict[str, str] = ufo.lib.get("public.openTypeCategories", {})
    categories: Dict[str, str] = {k: v for k, v in existing.items() if k in ufo}

    category_key = glyphsLib.builder.constants.GLYPHLIB_PREFIX + "category"
    subcategory_key = glyphsLib.builder.constants.GLYPHLIB_PREFIX + "subCategory"

    for glyph in ufo:
        assert glyph.name is not None
        has_attaching_anchor = False
        for anchor in glyph.anchors:
            name = anchor.name
            if not name:
                continue
            if not name.startswith("_"):
                has_attaching_anchor = True

        # First check glyph.lib for category/subCategory overrides. Otherwise,
        # use global values from GlyphData.
        glyphinfo = glyphsLib.glyphdata.get_glyph(glyph.name)
        category: Optional[str] = glyph.lib.get(category_key, glyphinfo.category)
        subcategory: Optional[str] = glyph.lib.get(subcategory_key, glyphinfo.subCategory)

        if glyph.name in KNOWN_BASES:
            categories[glyph.name] = "base"
        elif subcategory == "Ligature" and has_attaching_anchor:
            categories[glyph.name] = "ligature"
        elif category == "Mark" and (
            subcategory == "Nonspacing" or subcategory == "Spacing Combining"
        ):
            categories[glyph.name] = "mark"
        elif category == "Letter" and has_attaching_anchor:
            categories[glyph.name] = "base"

    return categories
