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

from pathlib import Path

from fontTools.ttLib.ttFont import TTFont

from .compact_kern_feature_writer import compact

ROOT = (Path(__file__) / "../../../").resolve()
TEST_OUTPUT = (Path(__file__) / "../test_output/").resolve()


def float_range(start, stop, step):
    while start <= stop:
        yield start
        start += step


if __name__ == "__main__":
    path = ROOT / "build/GoogleSans/variable/GoogleSans[GRAD,opsz,wght].ttf"
    ttf = TTFont(path)
    size = path.stat().st_size
    for lines_per_cluster in float_range(1, 10, 0.2):
        ttf = TTFont(path)  # Need to re-open because compact is actually in-place!
        ttf2 = compact(
            ttf,
            mode="auto",
            clustering_kwargs={"lines_per_cluster": lines_per_cluster},
        )
        path2 = (
            TEST_OUTPUT
            / f"GoogleSans[GRAD,opsz,wght]_compact_auto_nik_{lines_per_cluster}.ttf"
        )
        ttf2.save(path2)
        size2 = path2.stat().st_size
        percent = (size2 - size) / size * 100
        print(f"Nikolaus {lines_per_cluster:5.1f} {size2:10,d} bytes {percent:+5.1f}%")

    for linkage in ("ward", "complete", "average", "single"):
        for distance_threshold in float_range(0, 10, 0.5):
            ttf = TTFont(path)  # Need to re-open because compact is actually in-place!
            ttf2 = compact(
                ttf,
                mode="auto",
                clustering_kwargs={
                    "linkage": linkage,
                    "distance_threshold": distance_threshold,
                },
            )
            path2 = (
                TEST_OUTPUT / "GoogleSans[GRAD,opsz,wght]_compact_auto"
                f"_{linkage}_{distance_threshold:.1f}.ttf"
            )
            ttf2.save(path2)
            size2 = path2.stat().st_size
            percent = (size2 - size) / size * 100
            print(
                f"{linkage:>10} {distance_threshold:5.1f} {size2:10,d} bytes "
                f"{percent:+5.1f}%"
            )
