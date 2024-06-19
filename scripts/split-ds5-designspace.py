#!/usr/bin/env python3
# Copyright 2024 Google Sans Authors

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

from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.designspaceLib.split import splitInterpolable

REPO_PATH = Path(__file__).parent.parent
MAIN_DESIGNSPACE_PATH = REPO_PATH / "source" / "GoogleSans" / "GoogleSans.designspace"

OUTPUT_DIRECTORY = REPO_PATH / "build" / "GoogleSans" / ".intermediate"
UPRIGHT_DESIGNSPACE_PATH = OUTPUT_DIRECTORY / "GoogleSansUprights.designspace"
ITALIC_DESIGNSPACE_PATH = OUTPUT_DIRECTORY / "GoogleSansItalics.designspace"


def main():
    main_ds = DesignSpaceDocument.fromfile(MAIN_DESIGNSPACE_PATH)
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    for axes_locations, designspace in splitInterpolable(main_ds):
        if axes_locations["Italic"] == 0.0:
            designspace.write(UPRIGHT_DESIGNSPACE_PATH)
            # print(f"Wrote {UPRIGHT_DESIGNSPACE_PATH.relative_to(REPO_PATH)}")
        else:
            designspace.write(ITALIC_DESIGNSPACE_PATH)
            # print(f"Wrote {ITALIC_DESIGNSPACE_PATH.relative_to(REPO_PATH)}")


if __name__ == "__main__":
    main()
