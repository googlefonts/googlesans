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
import shutil
import sys

from fontTools.subset import main as subset_main

STATIC_INPATH = "../build/GoogleSans/static/expert/*.ttf"
VARIABLE_INPATH = "../build/GoogleSans/variable/expert/*.ttf"


def main():
    # ===============================================
    #
    #  Expert Subset build
    #
    # ===============================================
    #
    # This build includes all shaping and OT feature support,
    # *including* all alternate designs supported through the
    # `aalt` OpenType feature
    in_static_filepaths = glob.glob(STATIC_INPATH)

    for rel_filepath in in_static_filepaths:
        print(f"[SUBSET] {rel_filepath} to Expert build...")

        local_filepath = os.path.abspath(rel_filepath)
        local_filepath_subset = f"{local_filepath}.subset"

        # Expert subset argument definitions
        subset_args_expert = [
            local_filepath,
            "--unicodes=*",
            "--no-ignore-missing-glyphs",
            "--notdef-outline",
            "--layout-features=*",
            "--drop-tables= ",
            "--passthrough-tables",
            "--name-IDs=*",
            "--name-languages=*",
            "--glyph-names",
            "--no-prune-unicode-ranges",
            f"--output-file={local_filepath_subset}",
        ]

        try:
            subset_main(subset_args_expert)
        except Exception as e:
            sys.stderr.write(
                f"ERROR: subsetting error during attempt to subset {local_filepath}"
                f"- {str(e)}"
            )
            sys.exit(1)

        try:
            shutil.move(local_filepath_subset, local_filepath)
        except Exception as e:
            sys.stderr.write(
                f"ERROR: during move of subset file {local_filepath} - {str(e)}"
            )
            sys.exit(1)

    # ===============================================
    #
    #  Default Subset build
    #
    # ===============================================
    #
    # This build eliminates the OpenType `aalt` feature
    # support and all alternate glyph designs.

    in_static_filepaths = glob.glob(STATIC_INPATH)

    for rel_filepath in in_static_filepaths:
        print(f"[SUBSET] {rel_filepath} to Default build...")

        local_filepath = os.path.abspath(rel_filepath)
        local_filepath_subset = f"{local_filepath}.subset"

        # Default subset argument definitions
        #  eliminate `aalt` feature support and all alternate glyph definitions
        #  keep all other features that are included in the Expert build targets
        subset_args_default = [
            local_filepath,
            "--layout-features-=aalt",
            "--layout-features+=c2sc",
            "--layout-features+=case",
            "--layout-features+=ccmp",
            "--layout-features+=dlig",
            "--layout-features+=dnom",
            "--layout-features+=frac",
            "--layout-features+=kern",
            "--layout-features+=liga",
            "--layout-features+=lnum",
            "--layout-features+=locl",
            "--layout-features+=mark",
            "--layout-features+=mkmk",
            "--layout-features+=numr",
            "--layout-features+=ordn",
            "--layout-features+=pnum",
            "--layout-features+=sinf",
            "--layout-features+=smcp",
            "--layout-features+=ss01",
            "--layout-features+=ss02",
            "--layout-features+=ss03",
            "--layout-features+=ss04",
            "--layout-features+=ss05",
            "--layout-features+=ss06",
            "--layout-features+=ss07",
            "--layout-features+=ss08",
            "--layout-features+=subs",
            "--layout-features+=sups",
            "--layout-features+=tnum",
            "--unicodes=*",
            "--no-ignore-missing-glyphs",
            "--notdef-outline",
            "--drop-tables= ",
            "--passthrough-tables",
            "--name-IDs=*",
            "--name-languages=*",
            "--glyph-names",
            "--no-prune-unicode-ranges",
            f"--output-file={local_filepath_subset}",
        ]

        try:
            subset_main(subset_args_default)
        except Exception as e:
            sys.stderr.write(
                f"ERROR: subsetting error during attempt to subset {local_filepath}"
                f"- {str(e)}"
            )
            sys.exit(1)

        # define outpath for the default build target files
        # this defines "default" directory as the path for the subset files
        outpath_default_static = local_filepath.replace("expert", "default")
        print(f"[MOVE] default subset build to '{outpath_default_static}'")

        try:
            shutil.move(local_filepath_subset, outpath_default_static)
        except Exception as e:
            sys.stderr.write(
                f"ERROR: during move of subset file {local_filepath} - {str(e)}"
            )
            sys.exit(1)


if __name__ == "__main__":
    main()
