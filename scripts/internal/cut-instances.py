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

from __future__ import annotations

import argparse
import multiprocessing
import multiprocessing.pool
import subprocess
import sys
from pathlib import Path

from fontTools.designspaceLib import DesignSpaceDocument


def cut_instance(
    variable_font: Path, user_location: dict[str, float], output_file: Path
) -> None:
    user_location_args = [f"{k}={v}" for k, v in user_location.items()]

    print(f"Cutting {user_location_args} from {variable_font}")
    subprocess.check_call(
        [
            "fonttools",
            "varLib.instancer",
            "--quiet",
            "--remove-overlaps",
            "-o",
            str(output_file),
            str(variable_font),
            *user_location_args,
        ]
    )


def main(args: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "variable_font", type=Path, help="Variable font to cut instances from."
    )
    parser.add_argument(
        "designspace",
        type=DesignSpaceDocument.fromfile,
        help="Designspace to take instances from.",
    )
    parser.add_argument("output_dir", type=Path, help="Output directory.")
    parsed_args = parser.parse_args(args)
    designspace: DesignSpaceDocument = parsed_args.designspace
    output_dir: Path = parsed_args.output_dir
    variable_font: Path = parsed_args.variable_font

    pool = multiprocessing.pool.Pool(processes=multiprocessing.cpu_count())
    processes = []
    name2tag = {axis.name: axis.tag for axis in designspace.axes}
    name2axis = {axis.name: axis for axis in designspace.axes}
    for instance in designspace.instances:
        user_location = {
            name2tag[k]: name2axis[k].map_backward(v)
            for k, v in instance.location.items()
        }
        output_file = output_dir / Path(instance.filename).with_suffix(".ttf").name

        processes.append(
            pool.apply_async(cut_instance, (variable_font, user_location, output_file))
        )

    pool.close()
    pool.join()
    for process in processes:
        process.get()

    return 0


if __name__ == "__main__":
    sys.exit(main())
