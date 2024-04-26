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

PROFILE = {
    "include_profiles": ["universal"],
    # The checks are in a separate file, because Simon says that eventually this
    # file will become pure data.
    "check_definitions": [Path(__file__).parent / "check-googlesans-checks.py"],
    "sections": {
        "Google Fonts Checks": ["com.google.fonts/check/varfont/duplexed_axis_reflow"],
        "Google Sans Custom Checks": [
            "com.google.fonts/check/googlesans/opentype/os2/fsselectionbit7",
            "com.google.fonts/check/googlesans/opentype/os2/winascent",
            "com.google.fonts/check/googlesans/opentype/os2/windescent",
            "com.google.fonts/check/googlesans/opentype/hhea/ascent",
            "com.google.fonts/check/googlesans/opentype/hhea/descent",
            "com.google.fonts/check/googlesans/opentype/hhea/linegap",
            "com.google.fonts/check/googlesans/opentype/os2/strikeout",
            "com.google.fonts/check/googlesans/opentype/os2/typodescender",
            "com.google.fonts/check/googlesans/opentype/os2/typoascender",
            "com.google.fonts/check/googlesans/opentype/os2/typolinegap",
            "com.google.fonts/check/googlesans/opentype/os2/unicode_range_bits",
            "com.google.fonts/check/googlesans/opentype/post/underline",
            "com.google.fonts/check/googlesans/vf/fvaraxes",
            "com.google.fonts/check/googlesans/vf/fvardefault",
            "com.google.fonts/check/varfont/duplexed_axis_reflow",
        ],
    },
    "exclude_checks": [
        "com.google.fonts/check/ftxvalidator_is_available",
        "com.google.fonts/check/dsig",
        # replaced by custom checks
        "com.google.fonts/check/family/win_ascent_and_descent",
        # we do want our opsz definition
        "com.google.fonts/check/varfont/regular_opsz_coord",
        # "com.google.fonts/check/os2_metrics_match_hhea",
        # "com.google.fonts/check/unwanted_tables",
        # too many unactionable warnings
        "com.google.fonts/check/outline_jaggy_segments",
        # design rather than QA problem
        "com.google.fonts/check/outline_semi_vertical",
        # design rather than QA problem
        "com.google.fonts/check/contour_count",
        "com.adobe.fonts/check/varfont/valid_default_instance_nameids",  # Bogus
        "com.google.fonts/check/varfont/regular_wght_coord",  # Buggy in 0.8.9
        "com.google.fonts/check/varfont/bold_wght_coord",  # Buggy in 0.8.9
        # https://github.com/googlefonts/googlesans/issues/576:
        "com.google.fonts/check/soft_dotted",
        # We intentionally set the family names as they are
        "com.adobe.fonts/check/family/consistent_family_name",
        # Exclusion requested in https://github.com/googlefonts/googlesans/issues/316
        "com.google.fonts/check/interpolation_issues",
    ],
    "overrides": {
        "com.google.fonts/check/googlesans/opentype/os2/fsselectionbit7": {
            "os2_fsselection_bit7": 1
        },
        "com.google.fonts/check/googlesans/opentype/hhea/ascent": {
            "hhea_ascent": 966  # set to match typo metrics values
        },
        "com.google.fonts/check/googlesans/opentype/hhea/descent": {
            "hhea_descent": -286  # set to match typo metrics values
        },
        "com.google.fonts/check/googlesans/opentype/hhea/linegap": {"hhea_linegap": 0},
        "com.google.fonts/check/googlesans/opentype/os2/strikeout": {
            "os2_strikeout_position": 306,
            "os2_strikeout_size": 84,
        },
        "com.google.fonts/check/googlesans/opentype/os2/typodescender": {
            "os2_typodescender": -286,
        },
        "com.google.fonts/check/googlesans/opentype/os2/typoascender": {
            "os2_typoascender": 966,  # set to match hhea metrics values
        },
        "com.google.fonts/check/googlesans/opentype/os2/typolinegap": {
            "os2_typolinegap": 0,
        },
        "com.google.fonts/check/googlesans/vf/fvaraxes": {
            "expected_fvar_axes": ["opsz", "wght", "GRAD"]
        },
        "com.google.fonts/check/googlesans/vf/fvardefault": {
            "axis_defaults": {"opsz": 18.0, "wght": 400.0, "grad": 0.0}
        },
        "com.google.fonts/check/googlesans/opentype/post/underline": {
            "post_underline_position": -160,
            "post_underline_thickness": 84,
        },
    },
}
