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


from fontbakery.checkrunner import Section
from fontbakery.fonts_profile import profile_factory

profile_imports = ("fontbakery.profiles.universal",)
profile = profile_factory(default_section=Section("Google Sans Outline Checks"))

OUTLINE_PROFILE_CHECKS = [
    "com.google.fonts/check/outline_jaggy_segments",
    "com.google.fonts/check/outline_semi_vertical",
]


def check_skip_filter(checkid, font=None, **iterargs):
    if font and checkid not in OUTLINE_PROFILE_CHECKS:
        return False, ("Check skipped in Google Sans outline profile")
    return True, None


profile.check_skip_filter = check_skip_filter
profile.auto_register(globals())
profile.test_expected_checks(OUTLINE_PROFILE_CHECKS)
