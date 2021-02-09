import argparse
from pathlib import Path

import fontTools.feaLib.parser

parser = argparse.ArgumentParser()
parser.add_argument("feature_file", nargs="+", type=Path)
parsed_args = parser.parse_args()

for path in parsed_args.feature_file:
    fea = fontTools.feaLib.parser.Parser(path, followIncludes=False).parse().asFea()
    with open(path, "w") as f:
        f.write(fea)
