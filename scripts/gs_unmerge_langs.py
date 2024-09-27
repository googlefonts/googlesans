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

import ufo2ft.fontInfoData
import ufo2ft.util
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
    scripts: list[str]

    @property
    def codepoints(self) -> list[Path]:
        return [SUBSETS_DIR / f"{script}.txt" for script in self.scripts]


SUBSETS = [
    ###########################################
    ### Latin, Greek, Cyrillic, and Unknown ###
    ###########################################
    # EVERY Latin glyph, original vertical metrics:
    Subset(
        name="LGC-Full",
        ascender=966,
        descender=-286,
        scripts=[
            "LatnSmall",
            "LatnTall",
            "Grek",
            "Cyrl",
            # TODO: Confirm new clipping and/or find a new home
            "Zinh",
            "Zyyy",
            "Zzzz",
        ],
    ),
    # ONLY PREVIOUSLY NON-CLIPPING Latin glyphs, original vertical metrics:
    Subset(
        name="LGC-Small",
        ascender=966,
        descender=-286,
        scripts=[
            "LatnSmall",
            "Grek",
            "Cyrl",
            # TODO: Confirm new clipping and/or find a new home
            "Zinh",
            "Zyyy",
            "Zzzz",
        ],
    ),
    # ONLY PREVIOUSLY CLIPPING Latin glyphs, taller vertical metrics:
    Subset(name="LGC-Tall", ascender=1115, descender=-292, scripts=["LatnTall"]),
    ##########################
    ### Per-script Subsets ###
    ##########################
    # TODO: Final metrics
    Subset(name="Armn", ascender=1040, descender=-286, scripts=["Armn"]),
    Subset(name="Beng", ascender=1172, descender=-604, scripts=["Beng"]),
    Subset(name="Deva", ascender=1058, descender=-527, scripts=["Deva"]),
    Subset(name="Ethi", ascender=975, descender=-286, scripts=["Ethi"]),
    Subset(name="Geor", ascender=966, descender=-286, scripts=["Geor"]),
    Subset(name="Gujr", ascender=1244, descender=-565, scripts=["Gujr"]),
    Subset(name="Guru", ascender=1056, descender=-655, scripts=["Guru"]),
    Subset(name="Hebr", ascender=966, descender=-469, scripts=["Hebr"]),
    Subset(name="Khmr", ascender=1070, descender=-559, scripts=["Khmr"]),
    Subset(name="Knda", ascender=985, descender=-800, scripts=["Knda"]),
    Subset(name="Laoo", ascender=1375, descender=-474, scripts=["Laoo"]),
    Subset(name="Mlym", ascender=1070, descender=-395, scripts=["Mlym"]),
    Subset(name="Orya", ascender=1213, descender=-1076, scripts=["Orya"]),
    Subset(name="Sinh", ascender=1093, descender=-362, scripts=["Sinh"]),
    Subset(name="Taml", ascender=989, descender=-482, scripts=["Taml"]),
    Subset(name="Telu", ascender=1204, descender=-962, scripts=["Telu"]),
    Subset(name="Thai", ascender=1319, descender=-570, scripts=["Thai"]),
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
        "--notdef-outline",
        "--layout-features=*",
        "--recalc-bounds",
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

    # Set per-subset vertical metrics:
    ttf["OS/2"].sTypoAscender = subset.ascender  # type: ignore
    ttf["OS/2"].sTypoDescender = subset.descender  # type: ignore

    # Append suffix to differentiate subsets from each other and main VF:
    for rec in ttf["name"].names:  # type: ignore
        match rec.nameID:
            case 1 | 4:
                replace = ("Google Sans", f"Google Sans Alpha {subset.name}")
            case 3 | 6:
                replace = ("GoogleSans", f"GoogleSansAlpha{subset.name}")
            case 0 | 2 | 5 | 7 | 8 | 9 | 11 | 13:
                replace = None
            case n if n >= 256:  # User ID
                replace = None
            case n:
                raise ValueError(f"Unrecognised name ID for post-processing: {n}")

        if replace is not None:
            before, after = replace
            assert before in rec.toUnicode(), "Incorrect family name"
            rec.string = rec.toUnicode().replace(before, after)

    # Change version to 0.013
    ttf["head"].fontRevision = 0.013  # type: ignore

    for rec in ttf["name"].names:  # type: ignore
        rec.string = rec.toUnicode().replace("12.000", "0.013")

    # Update codepage ranges
    # API usage derived from here:
    #   https://github.com/googlefonts/ufo2ft/blob/5fd168e65/Lib/ufo2ft/outlineCompiler.py#L670-L672
    # TODO: When we bump fonttools, we can ask the subsetter to do this itself
    codepages = ufo2ft.util.calcCodePageRanges(set(ttf["cmap"].getBestCmap().keys()))  # type: ignore
    ttf["OS/2"].ulCodePageRange1 = ufo2ft.fontInfoData.intListToNum(codepages, 0, 32)  # type: ignore
    ttf["OS/2"].ulCodePageRange2 = ufo2ft.fontInfoData.intListToNum(codepages, 32, 32)  # type: ignore

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
