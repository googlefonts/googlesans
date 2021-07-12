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

import hashlib
import sys

from pathlib import Path

SOURCES = {
    "roman_opsz17": [
        "source/GoogleSans/GoogleSans-opsz17-wght380-GRAD-50.ufo/kerning.plist",
        "source/GoogleSans/GoogleSans-opsz17-wght380-GRAD0.ufo/kerning.plist",
        "source/GoogleSans/GoogleSans-opsz17-wght380-GRAD200.ufo/kerning.plist",
    ],
    "roman_opsz18": [
        "source/GoogleSans/GoogleSans-opsz18-wght380-GRAD-50.ufo/kerning.plist",
        "source/GoogleSans/GoogleSans-opsz18-wght380-GRAD0.ufo/kerning.plist",
        "source/GoogleSans/GoogleSans-opsz18-wght380-GRAD200.ufo/kerning.plist",
    ],
    "italic_opsz17": [
        "source/GoogleSans/GoogleSansItalic-opsz17-wght380-GRAD-50.ufo/kerning.plist",
        "source/GoogleSans/GoogleSansItalic-opsz17-wght380-GRAD0.ufo/kerning.plist",
        "source/GoogleSans/GoogleSansItalic-opsz17-wght380-GRAD200.ufo/kerning.plist",
    ],
    "italic_opsz18": [
        "source/GoogleSans/GoogleSansItalic-opsz18-wght380-GRAD-50.ufo/kerning.plist",
        "source/GoogleSans/GoogleSansItalic-opsz18-wght380-GRAD0.ufo/kerning.plist",
        "source/GoogleSans/GoogleSansItalic-opsz18-wght380-GRAD200.ufo/kerning.plist",
    ],
}


def main():
    for space in SOURCES.keys():
        fifty = SOURCES[space][0]
        zero = SOURCES[space][1]
        twohundred = SOURCES[space][2]

        with open(Path(fifty).resolve(), "rb") as f50:
            bytes = f50.read()
            hash_50 = hashlib.sha256(bytes).hexdigest()
            print(f"{hash_50} : {fifty}")

        with open(Path(zero).resolve(), "rb") as f0:
            bytes = f0.read()
            hash_0 = hashlib.sha256(bytes).hexdigest()
            print(f"{hash_0} : {zero}")

        with open(Path(twohundred).resolve(), "rb") as f200:
            bytes = f200.read()
            hash_200 = hashlib.sha256(bytes).hexdigest()
            print(f"{hash_200} : {twohundred}")

        if (hash_50 != hash_0) or (hash_200 != hash_0):
            print(
                f"[FAIL] SHA256 hashes are different across GRAD axis in the {space} "
                f"area of the design space.\n"
            )
            sys.exit(1)
        else:
            print("")


if __name__ == "__main__":
    main()
