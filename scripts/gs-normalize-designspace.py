"""Normalize all Designspaces and attached UFOs in a directory to match the
source conventions."""

import argparse
from pathlib import Path

from fontTools.designspaceLib import DesignSpaceDocument

from internal import normalize

ROOT_DIR = Path(__file__).parent.parent

parser = argparse.ArgumentParser()
parser.add_argument(
    "--source-dir",
    type=Path,
    default=ROOT_DIR / "source" / "GoogleSans",
    help="Path to source directory.",
)
parsed_args = parser.parse_args()

for designspace_path in parsed_args.source_dir.glob("*.designspace"):
    designspace = DesignSpaceDocument.fromfile(designspace_path)

    normalize.scrub_designspace(designspace, ROOT_DIR)

    for source in designspace.sources:
        source.font.save()
    designspace.write(designspace_path)
