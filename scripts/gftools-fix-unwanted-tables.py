#!/usr/bin/env python3

# Copyright 2019 The Google Font Tools Authors
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
#
# See AUTHORS.txt for the list of Authors and LICENSE.txt for the License.
#

import argparse
import logging
import os
import sys

from fontTools.ttLib import TTFont

UNWANTED_TABLES = [
    "FFTM",
    "TTFA",
    "TSI0",
    "TSI1",
    "TSI2",
    "TSI3",
    "TSI5",
    "prop",
]


def parse_tables(table_string):
    return table_string.split(",")


def main():
    description = "Removes unwanted tables from one or more font files"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-t", "--tables", type=str, help="One or more comma separated table names"
    )
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("FONTPATH", nargs="+", help="One or more font files")
    args = parser.parse_args()

    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.WARNING)
    LOGGER = logging.getLogger(__name__)
    if args.verbose:
        LOGGER.setLevel(logging.INFO)

    if args.tables:
        user_table_request = parse_tables(args.tables)
        # validate user table removal request
        for table in user_table_request:
            if table not in UNWANTED_TABLES:
                LOGGER.error(
                    "'%s' table cannot be removed with this script because it "
                    "is not defined as an unwanted table.",
                    table,
                )
                LOGGER.error(
                    "The unwanted table list includes the following tables: %s",
                    UNWANTED_TABLES,
                )
                sys.exit(1)
    else:
        user_table_request = UNWANTED_TABLES

    for fontpath in args.FONTPATH:
        # validate file
        if not os.path.exists(fontpath):
            LOGGER.error("The file path '%s' does not appear to be valid.", fontpath)
            sys.exit(1)

        try:
            tt = TTFont(fontpath)

            removed_table_list = []
            for table in user_table_request:
                if table in tt:
                    removed_table_list.append(table)
                    del tt[table]
                else:
                    LOGGER.info("'%s' table was not found in '%s'", table, fontpath)

            # save edited font
            tt.save(fontpath)

            # validate table removals
            tt_edited = TTFont(fontpath)
            for removed_table in removed_table_list:
                assert removed_table not in tt_edited
                LOGGER.info("'%s' table removed from '%s'", removed_table, fontpath)
        except Exception as e:
            LOGGER.error("Error during execution: %s", str(e))
            sys.exit(1)


if __name__ == "__main__":
    main()
