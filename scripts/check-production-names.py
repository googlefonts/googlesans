#!/usr/bin/env python3

# Copyright 2022 Google Sans Authors
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

"""Lint production names, checking for mistakes including overloaded names and
inconsistency within the same designspace.

TODO: If possible, check that naming convention is followed too (e.g. uni* where
      appropriate).
TODO: Check if production name locale matches glyph name locale.
TODO: Run this automatically on builds.
"""

from __future__ import annotations

import sys
from argparse import ArgumentParser
from collections import defaultdict
from dataclasses import dataclass

from fontTools.designspaceLib import DesignSpaceDocument  # pyright: ignore
from ufoLib2 import Font


@dataclass
class OverloadedName:
    production_name: str
    glyph_names: set[str]


def check_names(by_glyph_name: dict[str, str]):
    """Look for issues in a given public.postscriptNames dictionary."""

    # Store glyph names under their production name.
    by_prod_name: defaultdict[str, set[str]] = defaultdict(set)
    for glyph, prod in by_glyph_name.items():
        by_prod_name[prod].add(glyph)

    # Look for production names shared by multiple glyphs.
    for prod, glyphs in by_prod_name.items():
        if len(glyphs) > 1:
            yield OverloadedName(production_name=prod, glyph_names=glyphs)


def check_designspace(doc: DesignSpaceDocument):
    """Look for issues in the scope of an entire designspace."""

    # Get production names, and check for consensus across UFOs.
    first_source, first_names = None, None
    for source in doc.sources:
        path: str = source.path  # pyright: ignore
        ufo = Font.open(path)

        prod_names = ufo.lib["public.postscriptNames"]
        # TODO: This is just explicit production names; include implicit
        # production names too.

        if first_names is None:
            first_source, first_names = path, prod_names
        elif first_names != prod_names:
            print(
                f"Incompatible names in {doc.path}:",  # pyright: ignore
                f"definitions in {first_source} and {path} are different",
            )
            print()
            return False

    # Check that the designspace contained at least one UFO, and satisfy
    # type-checker.
    if first_names is None:
        print(
            f"Designspace {doc.path} has no source UFOs",  # pyright: ignore
        )
        print()
        return False

    # Check the production names we found for errors.
    overloadeds = list(check_names(first_names))
    if len(overloadeds) > 0:
        print(f"Overloaded names in {doc.path}:")  # pyright: ignore
        for overloaded in overloadeds:
            print(f"- {overloaded.production_name}: {sorted(overloaded.glyph_names)}")
        print()
        return False

    # No issues found.
    return True


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(
        "designspaces", nargs="+", type=DesignSpaceDocument.fromfile  # pyright: ignore
    )

    args = parser.parse_args()

    # Check every designspace given.
    were_errors = False
    for doc in args.designspaces:
        if not check_designspace(doc):
            were_errors = True
    if were_errors:
        sys.exit(1)
