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

"""Delete .cap glyphs now that the default figures are cap-height.

See: https://github.com/googlefonts/googlesans/pull/412#issuecomment-1785380958
"""
from __future__ import annotations

from pathlib import Path

import ufoLib2

GLYPHS_TO_DELETE = """
zero.cap
one.cap
two.cap
three.cap
four.cap
five.cap
six.cap
seven.cap
eight.cap
nine.cap
baht.cap
cent.cap
currency.cap
dollar.cap
dong.cap
euro.cap
franc.cap
hryvnia.cap
lira.cap
liraTurkish.cap
peso.cap
ruble.cap
rupeeIndian.cap
sheqel.cap
sterling.cap
tenge.cap
tugrik.cap
won.cap
yen.cap
percent.cap
pertenthousand.cap
perthousand.cap
lari.cap
sheqel.cap
dram-arm.cap
""".strip().split()

FEA_CAP_ON = """franc.cap ringcomb.cap gravecomb.cap acutecomb.cap dieresiscomb.cap caroncomb.cap brevecomb.cap macroncomb.cap circumflexcomb.cap at.cap tildecomb.cap hungarumlautcomb.cap dotaccentcomb.cap bracketleft.cap bracketright.cap parenleft.cap parenright.cap braceleft.cap braceright.cap questiondown.cap exclamdown.cap hyphen.cap endash.cap emdash.cap guilsinglleft.cap guilsinglright.cap guillemetleft.cap guillemetright.cap zero.cap one.cap two.cap three.cap four.cap five.cap six.cap seven.cap eight.cap nine.cap currency.cap dollar.cap euro.cap sterling.cap yen.cap lira.cap won.cap tugrik.cap peso.cap tenge.cap rupeeIndian.cap liraTurkish.cap ruble.cap dong.cap numbersign.cap percent.cap perthousand.cap pertenthousand.cap cent.cap baht.cap bullet.cap hryvnia.cap anoteleia.case brevecombcy.cap sheqel.cap"""
FEA_CAP_OFF = """franc ring grave acute dieresis caron breve macron circumflex at tilde hungarumlaut dotaccent bracketleft bracketright parenleft parenright braceleft braceright questiondown exclamdown hyphen endash emdash guilsinglleft guilsinglright guillemetleft guillemetright zero one two three four five six seven eight nine currency dollar euro sterling yen lira won tugrik peso tenge rupeeIndian liraTurkish ruble dong numbersign percent perthousand pertenthousand cent baht bullet hryvnia anoteleia brevecombcy sheqel"""

UFOS = [
    "GoogleSans-opsz17-wght380-GRAD-50.ufo",
    "GoogleSans-opsz17-wght380-GRAD0.ufo",
    "GoogleSans-opsz17-wght380-GRAD200.ufo",
    "GoogleSans-opsz17-wght734-GRAD0.ufo",
    "GoogleSans-opsz18-wght380-GRAD-50.ufo",
    "GoogleSans-opsz18-wght380-GRAD0.ufo",
    "GoogleSans-opsz18-wght380-GRAD200.ufo",
    "GoogleSans-opsz18-wght734-GRAD0.ufo",
    "GoogleSansItalic-opsz17-wght380-GRAD-50.ufo",
    "GoogleSansItalic-opsz17-wght380-GRAD0.ufo",
    "GoogleSansItalic-opsz17-wght380-GRAD200.ufo",
    "GoogleSansItalic-opsz17-wght734-GRAD0.ufo",
    "GoogleSansItalic-opsz18-wght380-GRAD-50.ufo",
    "GoogleSansItalic-opsz18-wght380-GRAD0.ufo",
    "GoogleSansItalic-opsz18-wght380-GRAD200.ufo",
    "GoogleSansItalic-opsz18-wght734-GRAD0.ufo",
]
ROOT_DIR = Path(__file__).parent.parent.parent
SOURCE_DIR = ROOT_DIR / "source" / "GoogleSans"


def main():
    print("Feature code:")
    cap_on = []
    cap_off = []
    for on, off in zip(FEA_CAP_ON.split(), FEA_CAP_OFF.split()):
        if on not in GLYPHS_TO_DELETE:
            cap_on.append(on)
            cap_off.append(off)
    print(f"@cap_on = [{' '.join(cap_on)}];")
    print(f"@cap_off = [{' '.join(cap_off)}];")

    for glyphsetdef in (ROOT_DIR / "qa" / "definitions").glob("*.glyphsetdef"):
        glyphs = glyphsetdef.read_text().splitlines()
        glyphs = [g for g in glyphs if g not in GLYPHS_TO_DELETE]
        glyphsetdef.write_text("\n".join(glyphs) + "\n")

    for ufo in UFOS:
        font = ufoLib2.Font.open(SOURCE_DIR / ufo)
        for glyph in GLYPHS_TO_DELETE:
            if glyph in font:
                del font[glyph]

        kerning_groups_to_be_cleaned = []
        for group_name in list(font.groups.keys()):
            members = font.groups[group_name]
            new_members = [
                member for member in members if member not in GLYPHS_TO_DELETE
            ]
            if new_members:
                font.groups[group_name] = new_members
            else:
                del font.groups[group_name]
                kerning_groups_to_be_cleaned.append(group_name)
        font.kerning = {
            (f, s): v
            for (f, s), v in font.kerning.items()
            if f not in kerning_groups_to_be_cleaned
            and f not in GLYPHS_TO_DELETE
            and s not in kerning_groups_to_be_cleaned
            and s not in GLYPHS_TO_DELETE
        }

        font.save(overwrite=True)


if __name__ == "__main__":
    main()
