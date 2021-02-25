#!/usr/bin/env python3
# Copyright 2020 Google Sans Authors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import glob
import os

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

MIN_OPSZ_SIZE = 17
MAX_OPSZ_SIZE = 18

VARIABLE_DIR = "../build/GoogleSans/variable/expert"
VARIABLE_INPATH = f"{VARIABLE_DIR}/*.ttf"

FAMILY_MAX = "Google Sans"
FAMILY_MIN = "Google Sans Text"
NAMEID_1_MAX = f"{FAMILY_MAX}"
NAMEID_1_MIN = f"{FAMILY_MIN}"
NAMEID_2_UPRIGHT = "Regular"
NAMEID_2_ITALIC = "Italic"
NAMEID_4_MAX_UPRIGHT = f"{FAMILY_MAX}"
NAMEID_4_MIN_UPRIGHT = f"{FAMILY_MIN}"
NAMEID_4_MAX_ITALIC = f"{FAMILY_MAX} Italic"
NAMEID_4_MIN_ITALIC = f"{FAMILY_MIN} Italic"
NAMEID_6_MAX_UPRIGHT = "GoogleSans-Regular"
NAMEID_6_MIN_UPRIGHT = "GoogleSansText-Regular"
NAMEID_6_MAX_ITALIC = "GoogleSans-Italic"
NAMEID_6_MIN_ITALIC = "GoogleSansText-Italic"


def main():
    in_var_paths = glob.glob(VARIABLE_INPATH)
    assert len(in_var_paths) > 0
    for fontpath in in_var_paths:
        # determine if this is the italic or upright VF build
        is_italic = False
        if "Italic" in fontpath:
            is_italic = True

        vf_full = TTFont(fontpath)
        pre_axis_tags = [a.axisTag for a in vf_full["fvar"].axes]
        # assert len(pre_axis_tags) == 2
        assert "opsz" in pre_axis_tags
        assert "wght" in pre_axis_tags
        assert "GRAD" in pre_axis_tags

        # =================================================
        # BUILD partial instance of min optical size design
        # =================================================
        print(
            f"[PARTIAL INSTANCE] {fontpath} to min optical size instance "
            f"builds defined at opsz {MIN_OPSZ_SIZE}..."
        )
        vf_partial_min_opsz = instancer.instantiateVariableFont(
            vf_full, {"opsz": MIN_OPSZ_SIZE}
        )
        # =================================================
        # BUILD partial instance of max optical size design
        # =================================================
        print(
            f"[PARTIAL INSTANCE] {fontpath} to max optical size instance "
            f"builds defined at opsz {MAX_OPSZ_SIZE}..."
        )
        vf_partial_max_opsz = instancer.instantiateVariableFont(
            vf_full, {"opsz": MAX_OPSZ_SIZE}
        )

        # verify that partial instance builds include the expected axis
        # definitions
        for vf_partial in (vf_partial_min_opsz, vf_partial_max_opsz):
            post_axis_tags = [a.axisTag for a in vf_partial["fvar"].axes]
            # assert len(post_axis_tags) == 1
            assert "wght" in post_axis_tags

        # ========================================
        # FIX name tables after partial instancing
        # ========================================
        namerecord_list_min_opsz = vf_partial_min_opsz["name"].names
        namerecord_list_max_opsz = vf_partial_max_opsz["name"].names

        # -------------------------
        # *** min opsz name fix ***
        # -------------------------
        new_min_opsz_namerecords = []
        for record in namerecord_list_min_opsz:
            skip_record = False
            if record.nameID == 1:
                record.string = FAMILY_MIN
            elif record.nameID == 2:
                if is_italic:
                    record.string = NAMEID_2_ITALIC
                else:
                    record.string = NAMEID_2_UPRIGHT
            elif record.nameID == 3:
                nameID3 = record.toUnicode()
                if is_italic:
                    record.string = nameID3.replace(
                        "GoogleSans-TextItalic", "GoogleSansText-Italic"
                    )
                else:
                    record.string = nameID3.replace(
                        "GoogleSans-TextRegular", "GoogleSansText-Regular"
                    )
            elif record.nameID == 4:
                if is_italic:
                    record.string = NAMEID_4_MIN_ITALIC
                else:
                    record.string = NAMEID_4_MIN_UPRIGHT
            elif record.nameID == 6:
                if is_italic:
                    record.string = NAMEID_6_MIN_ITALIC
                else:
                    record.string = NAMEID_6_MIN_UPRIGHT
            elif record.nameID == 16:
                # eliminate nameID 16
                skip_record = True
            elif record.nameID == 17:
                # eliminate nameID 17
                skip_record = True
            elif (
                record.nameID == 268
                or record.nameID == 269
                or record.nameID == 270
                or record.nameID == 271
            ):
                # eliminate "Text" from the style names in the name table records
                # 268, 269, 270, 271
                # note that the space after Text must remain in the pre-string
                # platformID = 1 replacements
                record.string = record.string.replace(b"Text ", b"")
                # platformID = 3 replacements
                record.string = record.string.replace(b"\x00T\x00e\x00x\x00t\x00 ", b"")

            if not skip_record:
                new_min_opsz_namerecords.append(record)

        # define new min opsz name records following above edits
        vf_partial_min_opsz["name"].names = new_min_opsz_namerecords

        # -------------------------
        # *** max opsz name fix ***
        # -------------------------
        new_max_opsz_namerecords = []
        for record in namerecord_list_max_opsz:
            skip_record = False
            if record.nameID == 1:
                record.string = FAMILY_MAX
            elif record.nameID == 2:
                if is_italic:
                    record.string = NAMEID_2_ITALIC
                else:
                    record.string = NAMEID_2_UPRIGHT
            elif record.nameID == 3:
                nameID3 = record.toUnicode()
                if is_italic:
                    record.string = nameID3.replace("-TextItalic", "-Italic")
                else:
                    record.string = nameID3.replace("-TextRegular", "-Regular")
            elif record.nameID == 4:
                if is_italic:
                    record.string = NAMEID_4_MAX_ITALIC
                else:
                    record.string = NAMEID_4_MAX_UPRIGHT
            elif record.nameID == 6:
                if is_italic:
                    record.string = NAMEID_6_MAX_ITALIC
                else:
                    record.string = NAMEID_6_MAX_UPRIGHT
            elif record.nameID == 16:
                # eliminate nameID 16
                skip_record = True
            elif record.nameID == 17:
                # eliminate nameID 17
                skip_record = True

            if not skip_record:
                new_max_opsz_namerecords.append(record)

        # define new max opsz name records following above edits
        vf_partial_max_opsz["name"].names = new_max_opsz_namerecords

        # write to min + max opsz file paths
        vf_partial_min_opsz.save(os.path.abspath(fontpath) + ".MIN_INSTANCE")
        vf_partial_max_opsz.save(os.path.abspath(fontpath) + ".MAX_INSTANCE")


if __name__ == "__main__":
    main()
