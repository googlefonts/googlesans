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

import os
import sys

from glyphsLib import GSFont


def main(argv):
    for fontpath in argv:
        removed_rmxscaler = False
        removed_robofont_guides = False
        removed_robofont_mark = False

        try:
            font = GSFont(fontpath)
            print(f"Beginning normalization of {fontpath}")
            for glyph in font.glyphs:
                # remove extraneous user data definitions
                if len(glyph.userData) > 0:
                    # RMXScaler user data
                    if "RMXScaler" in glyph.userData.keys():
                        del glyph.userData["RMXScaler"]
                        removed_rmxscaler = True
                    # Robofont user data
                    if "com.typemytype.robofont.guides" in glyph.userData.keys():
                        del glyph.userData["com.typemytype.robofont.guides"]
                        removed_robofont_guides = True
                    if "com.typemytype.robofont.mark" in glyph.userData.keys():
                        del glyph.userData["com.typemytype.robofont.mark"]
                        removed_robofont_mark = True

            font.save(fontpath)

            # report changes
            if removed_rmxscaler:
                print(f"Removed 'RMXScaler' user data from {fontpath}")
            if removed_robofont_guides:
                print(
                    f"Removed 'com.typemytype.robofont.guides' user data from {fontpath}"
                )
            if removed_robofont_mark:
                print(
                    f"Removed 'com.typemytype.robofont.mark' user data from {fontpath}"
                )
            print(f"Glyphs source file normalization successful for {fontpath}")
            print(f"Updated file saved in place on path {fontpath}")
        except Exception as e:
            sys.stderr.write(f"[ERROR] gs-glyphs-norm.py: {e}{os.linesep}")
            sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
