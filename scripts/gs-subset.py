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


def main():
    static_filepaths = glob.glob("../build/GoogleSans/static/*.ttf")

    for rel_filepath in static_filepaths:
        print(f"Subsetting {rel_filepath}...")

        local_filepath = os.path.abspath(rel_filepath)
        local_filepath_subset = f"{local_filepath}.subset"

        subset_args = [
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
            subset_main(subset_args)
        except Exception as e:
            sys.stderr.write(
                f"ERROR: subsetting error during attempt to subset {local_filepath}- {str(e)}"
            )
            sys.exit(1)

        try:
            shutil.move(local_filepath_subset, local_filepath)
        except Exception as e:
            sys.stderr.write(
                f"ERROR: during move of subset file {local_filepath} - {str(e)}"
            )
            sys.exit(1)


if __name__ == "__main__":
    main()
