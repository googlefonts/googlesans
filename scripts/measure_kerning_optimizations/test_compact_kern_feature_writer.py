from pathlib import Path

from fontTools.ttLib.ttFont import TTFont

from .compact_kern_feature_writer import compact

ROOT = (Path(__file__) / "../../../").resolve()
TEST_OUTPUT = (Path(__file__) / "../test_output/").resolve()


def test_compact_one():
    ttf = TTFont(ROOT / "build/GoogleSans/variable/GoogleSans[GRAD,opsz,wght].ttf")
    ttf2 = compact(ttf, mode="one")
    ttf2.save(TEST_OUTPUT / "GoogleSans[GRAD,opsz,wght]_compact_one.ttf")


def test_compact_max():
    ttf = TTFont(ROOT / "build/GoogleSans/variable/GoogleSans[GRAD,opsz,wght].ttf")
    ttf2 = compact(ttf, mode="max")
    ttf2.save(TEST_OUTPUT / "GoogleSans[GRAD,opsz,wght]_compact_max.ttf")


def test_compact_auto():
    ttf = TTFont(ROOT / "build/GoogleSans/variable/GoogleSans[GRAD,opsz,wght].ttf")
    ttf2 = compact(ttf, mode="auto")
    ttf2.save(TEST_OUTPUT / "GoogleSans[GRAD,opsz,wght]_compact_auto.ttf")
