#!/usr/bin/env python3
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
"""
metadata-builder.py

Writes the Google Sans project Fonts API METADATA.pb subsetting
configuration file.
"""

import os
import subprocess
from pathlib import Path

SUBSETS = (
    "armenian",
    "cyrillic",
    "devanagari",
    "georgian",
    "greek",
    "gurmukhi",
    "hebrew",
    "latin",
    "latin-ext",
    "menu",
    "vietnamese",
)

KEEP_FEATURES = (
    "hist",
    "lnum",
    "pnum",
    "ss02",
    "tnum",
)

TEMPLATE = """name: "Google Sans"
designer: "Google"
license: "GOOGLE_RESTRICTED"
visibility: "INTERNAL"
category: "SANS_SERIF"
date_added: 1496646000000  # 2017-06-05
version: "v***"  # repository commit: {{gitcommit}}
fonts {
  name: "Google Sans"
  style: "normal"
  weight: 400
  filename: "GoogleSans[GRAD,opsz,wght].ttf"
  post_script_name: "GoogleSans-Regular"
  full_name: "Google Sans Regular"
  [google.fonts.copyright]: "Copyright 2017 Google, Inc. All Rights Reserved."
}
fonts {
  name: "Google Sans"
  style: "italic"
  weight: 400
  filename: "GoogleSans-Italic[GRAD,opsz,wght].ttf"
  post_script_name: "GoogleSans-Italic"
  full_name: "Google Sans Italic"
  [google.fonts.copyright]: "Copyright 2017 Google, Inc. All Rights Reserved."
}
{{subsets}}
experiments: "dont_send_all_subset_through_subsetter"
experiments: "layout_features={{features}}"
foundry: "GOOGLE"
android_version: "v26"
axes {
  tag: "GRAD"
  min_value: -50
  max_value: 200
}
axes {
  tag: "opsz"
  min_value: 17
  max_value: 18
}
axes {
  tag: "wght"
  min_value: 400.0
  max_value: 700.0
}
registry_default_overrides {
  key: "opsz"
  value: 18
}
[google.fonts.size]: {{filesize}}

"""


def get_git_commit_sha():
    git_sha = subprocess.check_output(
        "git rev-parse HEAD", stderr=subprocess.STDOUT, shell=True
    ).strip()
    return git_sha.decode("utf-8")


def main():
    # font paths
    root_font_dir = Path("../build/GoogleSans/variable").resolve()
    fontpaths = root_font_dir.glob("*.ttf")

    # define subset strings
    subset_str = ""
    for subset in sorted(SUBSETS):
        subset_str += f'subsets: "{subset}"\n'
    # remove the final newline
    subset_str = subset_str[0:-1]

    # define keep feature list
    feature_str = ""
    for feature in sorted(KEEP_FEATURES):
        feature_str += f"{feature},"

    # remove the final comma
    feature_str = feature_str[0:-1]

    # define total file size with variable build artifacts
    total_filesize = 0
    for fontpath in fontpaths:
        total_filesize += os.path.getsize(fontpath)

    # template replacements
    template = TEMPLATE
    template = template.replace("{{subsets}}", subset_str)
    template = template.replace("{{features}}", feature_str)
    template = template.replace("{{filesize}}", str(total_filesize))
    template = template.replace("{{gitcommit}}", get_git_commit_sha())

    with open("METADATA.pb", "w") as f:
        f.write(template)


if __name__ == "__main__":
    main()
