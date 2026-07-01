# Copyright 2021 Google Sans Authors
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
