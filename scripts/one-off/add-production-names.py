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

from ufoLib2 import Font

# Production names for the Latin extension
PRODUCTION_NAMES = {
    "Schwa": "uni018F",
    "schwa": "uni0259",
    "IJ": None,
    "ij": None,
    "Bhook": "uni0181",
    "bhook": "uni0253",
    "Dhook": "uni018A",
    "dhook": "uni0257",
    "Khook": "uni0198",
    "khook": "uni0199",
    "Yhook": "uni01B3",
    "yhook": "uni01B4",
    "Sdotbelow": "uni1E62",
    "sdotbelow": "uni1E63",
    "Oopen": "uni0186",
    "oopen": "uni0254",
    "Eopen": "uni0190",
    "eopen": "uni025B",
    "G.circ": None,
    "bhook.sc": "uni0253.sc",
    "dhook.sc": "uni0257.sc",
    "oopen.sc": "uni0254.sc",
    "ij.sc": None,
    "khook.sc": "uni0199.sc",
    "eopen.sc": "uni025B.sc",
    "schwa.sc": "uni0259.sc",
    "sdotbelow.sc": "uni1E63.sc",
    "yhook.sc": "uni01B4.sc",
}

for ufo_path in Path("source/GoogleSans").glob("*.ufo"):
    font = Font.open(ufo_path)
    production_names = font.lib["public.postscriptNames"]
    for design, production in PRODUCTION_NAMES.items():
        if production is not None:
            production_names[design] = production
    font.save()
