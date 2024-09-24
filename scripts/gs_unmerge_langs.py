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

import multiprocessing
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path

from fontTools.subset import Subsetter
from fontTools.subset import main as pyftsubset
from fontTools.ttLib import TTFont

BUILD_DIR = Path("build/GoogleSans/android")
SUBSETS_DIR = Path("source/GoogleSans/subsets")


@dataclass(frozen=True, kw_only=True)
class Subset:
    """All of the ingredients to make a subset."""

    name: str
    ascender: int
    descender: int

    @property
    def codepoints(self) -> list[Path]:
        return [SUBSETS_DIR / f"{self.name}.txt"]


SUBSETS = [
    Subset(name="Latn", ascender=966, descender=-286),
    Subset(name="Armn", ascender=966, descender=-286),  # TODO: Add final metrics
    Subset(name="Beng", ascender=966, descender=-286),  # TODO: Add final metrics
    Subset(name="Cyrl", ascender=966, descender=-286),  # TODO: Add final metrics
    Subset(name="Deva", ascender=966, descender=-286),  # TODO: Add final metrics
    Subset(name="Ethi", ascender=966, descender=-286),  # TODO: Add final metrics
    Subset(name="Geor", ascender=966, descender=-286),  # TODO: Add final metrics
    Subset(name="Grek", ascender=966, descender=-286),  # TODO: Add final metrics
    Subset(name="Gujr", ascender=966, descender=-286),  # TODO: Add final metrics
    Subset(name="Guru", ascender=966, descender=-286),  # TODO: Add final metrics
    Subset(name="Hebr", ascender=966, descender=-286),  # TODO: Add final metrics
    Subset(name="Khmr", ascender=966, descender=-286),  # TODO: Add final metrics
    Subset(name="Knda", ascender=966, descender=-286),  # TODO: Add final metrics
    Subset(name="Laoo", ascender=966, descender=-286),  # TODO: Add final metrics
    Subset(name="Mlym", ascender=966, descender=-286),  # TODO: Add final metrics
    Subset(name="Orya", ascender=966, descender=-286),  # TODO: Add final metrics
    Subset(name="Sinh", ascender=966, descender=-286),  # TODO: Add final metrics
    Subset(name="Taml", ascender=966, descender=-286),  # TODO: Add final metrics
    Subset(name="Telu", ascender=966, descender=-286),  # TODO: Add final metrics
    Subset(name="Thai", ascender=966, descender=-286),  # TODO: Add final metrics
    Subset(name="Zinh", ascender=966, descender=-286),  # TODO: Add final metrics
    Subset(name="Zyyy", ascender=966, descender=-286),  # TODO: Add final metrics
    Subset(name="Zzzz", ascender=966, descender=-286),  # TODO: Add final metrics
]


def main(ttfs: list[Path]) -> None:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    for ttf in ttfs:
        extract_subsets(ttf)


def extract_subsets(base_ttf: Path) -> None:
    with multiprocessing.Pool() as pool:
        pool.starmap(
            extract_subset,
            ((base_ttf, subset) for subset in SUBSETS),
        )


def extract_subset(base_ttf: Path, subset: Subset) -> None:
    output_path = BUILD_DIR / f"{base_ttf.stem}-{subset.name}.ttf"
    print(f"Making {output_path} with pyftsubset")

    # Produce new TTF with subset of glyphs.
    args = (
        str(base_ttf),
        *(f"--unicodes-file={path}" for path in subset.codepoints),
        f"--output-file={output_path}",
        "--name-IDs=*",
        "--name-languages=*",
    )
    try:
        pyftsubset(args)
    except Subsetter.MissingGlyphsSubsettingError as e:
        missing_glyphs = sorted(e.args[0])
        print(
            f"pyftsubset of {subset.name}",
            "failed due to missing glyphs:\n-",
            "\n- ".join(missing_glyphs),
        )
        raise
    except:
        print(f"pyftsubset of {subset.name} failed")
        raise

    # Post-process TTF metadata (e.g. names, metrics).
    ttf = TTFont(output_path)
    ttf["OS/2"].sTypoAscender = subset.ascender  # type: ignore
    ttf["OS/2"].sTypoDescender = subset.descender  # type: ignore
    ttf.save(output_path)


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
