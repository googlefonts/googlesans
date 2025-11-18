# Copyright 2020 Google Sans Authors

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
import os

# Hack to have this be conditional but without appending later
# Only run on main & releases:
# https://github.com/googlefonts/googlesans/issues/316#issuecomment-2120825286
# https://docs.github.com/en/actions/learn-github-actions/variables#default-environment-variables
INTERPOLATION_ISSUES = (
    ()
    if "CI" in os.environ
    and (
        os.environ.get("GITHUB_REF_NAME") == "main"
        or os.environ.get("GITHUB_REF_TYPE") == "tag"
    )
    else ("interpolation_issues",)
)

PROFILE = {
    "include_profiles": ["universal"],
    # The checks are in a separate file, because Simon says that eventually this
    # file will become pure data.
    "check_definitions": [Path(__file__).parent / "check-googlesans-checks.py"],
    "sections": {
        "Google Fonts Checks": ["varfont/duplexed_axis_reflow"],
        "Google Sans Custom Checks": [
            "googlesans/opentype/os2/fsselectionbit7",
            "googlesans/opentype/os2/winascent",
            "googlesans/opentype/os2/windescent",
            "googlesans/opentype/hhea/ascent",
            "googlesans/opentype/hhea/descent",
            "googlesans/opentype/hhea/linegap",
            "googlesans/opentype/os2/strikeout",
            "googlesans/opentype/os2/typodescender",
            "googlesans/opentype/os2/typoascender",
            "googlesans/opentype/os2/typolinegap",
            "googlesans/opentype/os2/unicode_range_bits",
            "googlesans/opentype/post/underline",
            "googlesans/vf/fvaraxes",
            "googlesans/vf/fvardefault",
            "varfont/duplexed_axis_reflow",
        ],
    },
    "exclude_checks": [
        # replaced by custom checks
        "family/win_ascent_and_descent",
        # we do want our opsz definition
        "opentype/fvar/regular_coords_correct",
        # "os2_metrics_match_hhea",
        # "unwanted_tables",
        # too many unactionable warnings
        "outline_jaggy_segments",
        # design rather than QA problem
        "outline_semi_vertical",
        # design rather than QA problem
        "contour_count",
        "opentype/varfont/valid_default_instance_nameids",  # Bogus
        "varfont/bold_wght_coord",  # Buggy in 0.8.9
        # https://github.com/googlefonts/googlesans/issues/576:
        "soft_dotted",
        # We intentionally set the family names as they are
        "opentype/family/consistent_family_name",
        # See declaration
        *INTERPOLATION_ISSUES,
        # Ignore issue about a Khmer glyph that Cadson-Demak confirmed to be OK
        # https://github.com/googlefonts/googlesans/pull/656#issuecomment-3130940361
        "base_has_width",
        # Ignore mac names, Marianna confirmed we don't change the fonts at the moment
        # https://github.com/googlefonts/googlesans/pull/656#issuecomment-3103220308
        "no_mac_entries",
        # Ignore family name issue, it's on purpose
        # https://github.com/googlefonts/googlesans/pull/656#issuecomment-3103220308
        "typographic_family_name",
        # Not applicable to Google Sans fonts:
        "fontdata_namecheck",
        # We're not that worried about Microsoft Office support
        # https://github.com/googlefonts/googlesans/issues/693#issuecomment-3480871914
        "name/family_and_style_max_length",
    ],
    "configuration_defaults": {
        "googlesans/opentype/os2/fsselectionbit7": {
            "os2_fsselection_bit7": 1
        },
        "googlesans/opentype/hhea/ascent": {
            "hhea_ascent": 966  # set to match typo metrics values
        },
        "googlesans/opentype/hhea/descent": {
            "hhea_descent": -286  # set to match typo metrics values
        },
        "googlesans/opentype/hhea/linegap": {"hhea_linegap": 0},
        "googlesans/opentype/os2/strikeout": {
            "os2_strikeout_position": 306,
            "os2_strikeout_size": 84,
        },
        "googlesans/opentype/os2/typodescender": {
            "os2_typodescender": -286,
        },
        "googlesans/opentype/os2/typoascender": {
            "os2_typoascender": 966,  # set to match hhea metrics values
        },
        "googlesans/opentype/os2/typolinegap": {
            "os2_typolinegap": 0,
        },
        "googlesans/vf/fvaraxes": {
            "expected_fvar_axes": ["opsz", "wght", "GRAD"]
        },
        "googlesans/vf/fvardefault": {
            "axis_defaults": {"opsz": 18.0, "wght": 400.0, "grad": 0.0}
        },
        "googlesans/opentype/post/underline": {
            "post_underline_position": -160,
            "post_underline_thickness": 84,
        },
    },
}
