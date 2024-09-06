#!/usr/bin/env python3

# Copyright 2024 Google Sans Authors
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
Extract language subsets from TTFs containing all languages.

Uses subsets found in source/GoogleSans/subsets. The name of the subset file is
appended to the font's file name, with output fonts landing in
build/GoogleSans/android. Each subset includes Latin.
"""

from argparse import ArgumentParser
import multiprocessing
from pathlib import Path

from fontTools.subset import main as pyftsubset, Subsetter


BUILD_DIR = Path("build/GoogleSans/android")

SUBSETS_DIR = Path("source/GoogleSans/subsets")
SUBSET_FILES = sorted(path for path in SUBSETS_DIR.glob("*.txt") if path.stem != "Latn")
LATIN_SUBSET = SUBSETS_DIR / "Latn.txt"


def main(ttfs: list[Path]) -> None:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    with multiprocessing.Pool() as pool:
        for ttf in ttfs:
            pool.apply_async(extract_subsets, (ttf,))
        pool.close()
        pool.join()


def extract_subsets(base_ttf: Path) -> None:
    for unicodes_list_path in SUBSET_FILES:
        output_path = BUILD_DIR / f"{base_ttf.stem}-{unicodes_list_path.stem}.ttf"
        print(f"Making {output_path} with pyftsubset")

        args = (
            str(base_ttf),
            f"--unicodes-file={LATIN_SUBSET}",
            f"--unicodes-file={unicodes_list_path}",
            f"--output-file={output_path}",
        )
        # print(f"pyftsubset {' '.join(args)}")
        try:
            pyftsubset(args)
        except Subsetter.MissingGlyphsSubsettingError as e:
            missing_glyphs = sorted(e.args[0])
            print(
                f"pyftsubset of {unicodes_list_path.stem}",
                "failed due to missing glyphs:\n-",
                "\n- ".join(missing_glyphs),
            )
        except Exception as e:
            print(f"pyftsubset of {unicodes_list_path.stem} failed: {e}")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "base_ttfs",
        help="TTF(s) to extract subsets from",
        metavar="ttf",
        nargs="*",
        type=Path,
        default=[Path("build/GoogleSans/static/GoogleSans-Regular.ttf")],
    )

    args = parser.parse_args()
    main(args.base_ttfs)
