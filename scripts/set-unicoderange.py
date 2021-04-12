#!/usr/bin/env python3

#    Copyright 2021 Source Foundry Authors
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

# ~~~ SOURCE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# https://github.com/source-foundry/set-unicoderange
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~ USAGE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# This script automatically sets OpenType OS/2.ulUnicodeRange bit flags 1 to 4
# in fonts based on the Unicode code points that are present in one or more
# fonts passed as command line arguments.
#
# Dependencies: fontTools Python package, cPython 3.6+
#
# Syntax:
#  $ python3 set-unicoderange.py [FONT PATH 1] (FONT PATH 2) ... (FONT PATH n)
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import re
import sys

from fontTools.ttLib import TTFont

VERSION = "0.1.0"

bit0 = [(0x0000, 0x007F)]
bit1 = [(0x0080, 0x00FF)]
bit2 = [(0x0100, 0x017F)]
bit3 = [(0x0180, 0x024F)]
bit4 = [(0x0250, 0x02AF), (0x1D00, 0x1D7F), (0x1D80, 0x1DBF)]
bit5 = [(0x02B0, 0x02FF), (0xA700, 0xA71F)]
bit6 = [(0x0300, 0x036F), (0x1DC0, 0x1DFF)]
bit7 = [(0x0370, 0x03FF)]
bit8 = [(0x2C80, 0x2CFF)]
bit9 = [(0x0400, 0x04FF), (0x0500, 0x052F), (0x2DE0, 0x2DFF), (0xA640, 0xA69F)]
bit10 = [(0x0530, 0x058F)]
bit11 = [(0x0590, 0x05FF)]
bit12 = [(0xA500, 0xA63F)]
bit13 = [(0x0600, 0x06FF), (0x0750, 0x077F)]
bit14 = [(0x07C0, 0x07FF)]
bit15 = [(0x0900, 0x097F)]
bit16 = [(0x0980, 0x09FF)]
bit17 = [(0x0A00, 0x0A7F)]
bit18 = [(0x0A80, 0x0AFF)]
bit19 = [(0x0B00, 0x0B7F)]
bit20 = [(0x0B80, 0x0BFF)]
bit21 = [(0x0C00, 0x0C7F)]
bit22 = [(0x0C80, 0x0CFF)]
bit23 = [(0x0D00, 0x0D7F)]
bit24 = [(0x0E00, 0x0E7F)]
bit25 = [(0x0E80, 0x0EFF)]
bit26 = [(0x10A0, 0x10FF), (0x2D00, 0x2D2F)]
bit27 = [(0x1B00, 0x1B7F)]
bit28 = [(0x1100, 0x11FF)]
bit29 = [(0x1E00, 0x1EFF), (0x2C60, 0x2C7F), (0xA720, 0xA7FF)]
bit30 = [(0x1F00, 0x1FFF)]
bit31 = [(0x2000, 0x206F), (0x2E00, 0x2E7F)]

bit32 = [(0x2070, 0x209F)]
bit33 = [(0x20A0, 0x20CF)]
bit34 = [(0x20D0, 0x20FF)]
bit35 = [(0x2100, 0x214F)]
bit36 = [(0x2150, 0x218F)]
bit37 = [(0x2190, 0x21FF), (0x27F0, 0x27FF), (0x2900, 0x297F), (0x2B00, 0x2BFF)]
bit38 = [(0x2200, 0x22FF), (0x2A00, 0x2AFF), (0x27C0, 0x27EF), (0x2980, 0x29FF)]
bit39 = [(0x2300, 0x23FF)]
bit40 = [(0x2400, 0x243F)]
bit41 = [(0x2440, 0x245F)]
bit42 = [(0x2460, 0x24FF)]
bit43 = [(0x2500, 0x257F)]
bit44 = [(0x2580, 0x259F)]
bit45 = [(0x25A0, 0x25FF)]
bit46 = [(0x2600, 0x26FF)]
bit47 = [(0x2700, 0x27BF)]
bit48 = [(0x3000, 0x303F)]
bit49 = [(0x3040, 0x309F)]
bit50 = [(0x30A0, 0x30FF), (0x31F0, 0x31FF)]
bit51 = [(0x3100, 0x312F), (0x31A0, 0x31BF)]
bit52 = [(0x3130, 0x318F)]
bit53 = [(0xA840, 0xA87F)]
bit54 = [(0x3200, 0x32FF)]
bit55 = [(0x3300, 0x33FF)]
bit56 = [(0xAC00, 0xD7AF)]
bit57 = [(0x10000, 0x10FFFF)]
bit58 = [(0x10900, 0x1091F)]
bit59 = [
    (0x4E00, 0x9FFF),
    (0x2E80, 0x2EFF),
    (0x2F00, 0x2FDF),
    (0x2FF0, 0x2FFF),
    (0x3400, 0x4DBF),
    (0x20000, 0x2A6DF),
    (0x3190, 0x319F),
]
bit60 = [(0xE000, 0xF8FF)]
bit61 = [(0x31C0, 0x31EF), (0xF900, 0xFAFF), (0x2F800, 0x2FA1F)]
bit62 = [(0xFB00, 0xFB4F)]
bit63 = [(0xFB50, 0xFDFF)]

bit64 = [(0xFE20, 0xFE2F)]
bit65 = [(0xFE10, 0xFE1F), (0xFE30, 0xFE4F)]
bit66 = [(0xFE50, 0xFE6F)]
bit67 = [(0xFE70, 0xFEFF)]
bit68 = [(0xFF00, 0xFFEF)]
bit69 = [(0xFFF0, 0xFFFF)]
bit70 = [(0x0F00, 0x0FFF)]
bit71 = [(0x0700, 0x074F)]
bit72 = [(0x0780, 0x07BF)]
bit73 = [(0x0D80, 0x0DFF)]
bit74 = [(0x1000, 0x109F)]
bit75 = [(0x1200, 0x137F), (0x1380, 0x139F), (0x2D80, 0x2DDF)]
bit76 = [(0x13A0, 0x13FF)]
bit77 = [(0x1400, 0x167F)]
bit78 = [(0x1680, 0x169F)]
bit79 = [(0x16A0, 0x16FF)]
bit80 = [(0x1780, 0x17FF), (0x19E0, 0x19FF)]
bit81 = [(0x1800, 0x18AF)]
bit82 = [(0x2800, 0x28FF)]
bit83 = [(0xA000, 0xA48F), (0xA490, 0xA4CF)]
bit84 = [(0x1700, 0x171F), (0x1720, 0x173F), (0x1740, 0x175F), (0x1760, 0x177F)]
bit85 = [(0x10300, 0x1032F)]
bit86 = [(0x10330, 0x1034F)]
bit87 = [(0x10400, 0x1044F)]
bit88 = [(0x1D000, 0x1D0FF), (0x1D100, 0x1D1FF), (0x1D200, 0x1D24F)]
bit89 = [(0x1D400, 0x1D7FF)]
bit90 = [(0xF0000, 0xFFFFD), (0x100000, 0x10FFFD)]
bit91 = [(0xFE00, 0xFE0F), (0xE0100, 0xE01EF)]
bit92 = [(0xE0000, 0xE007F)]
bit93 = [(0x1900, 0x194F)]
bit94 = [(0x1950, 0x197F)]
bit95 = [(0x1980, 0x19DF)]

bit96 = [(0x1A00, 0x1A1F)]
bit97 = [(0x2C00, 0x2C5F)]
bit98 = [(0x2D30, 0x2D7F)]
bit99 = [(0x4DC0, 0x4DFF)]
bit100 = [(0xA800, 0xA82F)]
bit101 = [(0x10000, 0x1007F), (0x10080, 0x100FF), (0x10100, 0x1013F)]
bit102 = [(0x10140, 0x1018F)]
bit103 = [(0x10380, 0x1039F)]
bit104 = [(0x103A0, 0x103DF)]
bit105 = [(0x10450, 0x1047F)]
bit106 = [(0x10480, 0x104AF)]
bit107 = [(0x10800, 0x1083F)]
bit108 = [(0x10A00, 0x10A5F)]
bit109 = [(0x1D300, 0x1D35F)]
bit110 = [(0x12000, 0x123FF), (0x12400, 0x1247F)]
bit111 = [(0x1D360, 0x1D37F)]
bit112 = [(0x1B80, 0x1BBF)]
bit113 = [(0x1C00, 0x1C4F)]
bit114 = [(0x1C50, 0x1C7F)]
bit115 = [(0xA880, 0xA8DF)]
bit116 = [(0xA900, 0xA92F)]
bit117 = [(0xA930, 0xA95F)]
bit118 = [(0xAA00, 0xAA5F)]
bit119 = [(0x10190, 0x101CF)]
bit120 = [(0x101D0, 0x101FF)]
bit121 = [(0x102A0, 0x102DF), (0x10280, 0x1029F), (0x10920, 0x1093F)]
bit122 = [(0x1F030, 0x1F09F), (0x1F000, 0x1F02F)]


UNICODE_RANGES = [
    bit0,
    bit1,
    bit2,
    bit3,
    bit4,
    bit5,
    bit6,
    bit7,
    bit8,
    bit9,
    bit10,
    bit11,
    bit12,
    bit13,
    bit14,
    bit15,
    bit16,
    bit17,
    bit18,
    bit19,
    bit20,
    bit21,
    bit22,
    bit23,
    bit24,
    bit25,
    bit26,
    bit27,
    bit28,
    bit29,
    bit30,
    bit31,
    bit32,
    bit33,
    bit34,
    bit35,
    bit36,
    bit37,
    bit38,
    bit39,
    bit40,
    bit41,
    bit42,
    bit43,
    bit44,
    bit45,
    bit46,
    bit47,
    bit48,
    bit49,
    bit50,
    bit51,
    bit52,
    bit53,
    bit54,
    bit55,
    bit56,
    bit57,
    bit58,
    bit59,
    bit60,
    bit61,
    bit62,
    bit63,
    bit64,
    bit65,
    bit66,
    bit67,
    bit68,
    bit69,
    bit70,
    bit71,
    bit72,
    bit73,
    bit74,
    bit75,
    bit76,
    bit77,
    bit78,
    bit79,
    bit80,
    bit81,
    bit82,
    bit83,
    bit84,
    bit85,
    bit86,
    bit87,
    bit88,
    bit89,
    bit90,
    bit91,
    bit92,
    bit93,
    bit94,
    bit95,
    bit96,
    bit97,
    bit98,
    bit99,
    bit100,
    bit101,
    bit102,
    bit103,
    bit104,
    bit105,
    bit106,
    bit107,
    bit108,
    bit109,
    bit110,
    bit111,
    bit112,
    bit113,
    bit114,
    bit115,
    bit116,
    bit117,
    bit118,
    bit119,
    bit120,
    bit121,
    bit122,
]


def generate_unicoderange_128bit_bitflag(ttFont):
    cmap = sorted(ttFont.getBestCmap())
    bitflag = 0
    for codepoint in cmap:
        for offset, bit_ranges in enumerate(UNICODE_RANGES):
            for bit_range in bit_ranges:
                if codepoint >= bit_range[0] and codepoint <= bit_range[1]:
                    bitflag |= 1 << offset
                    break

    return bitflag


def generate_128bit_bitflag_from_32bit_bitflags(bitflag1, bitflag2, bitflag3, bitflag4):
    return bitflag1 | bitflag2 << 32 | bitflag3 << 64 | bitflag4 << 96


def generate_shifted_32bit_unicoderange(bitflag, shift):
    # 32-bit int with all 32 bits set as & operator mask
    mask = 2 ** 32 - 1
    return (bitflag >> shift) & mask


def green(pre_string):
    return f"\033[32m{pre_string}\033[0m"


def main(argv):
    for fontpath in argv:
        if not os.path.isfile(fontpath):
            sys.stderr.write(f"{fontpath} does not appear to be a valid file path\n")
            sys.exit(1)
        # font os2, cmap
        tt = TTFont(fontpath)
        os2 = tt["OS/2"]

        # ulUnicodeRange bit flags
        unicode_range_1_int = os2.ulUnicodeRange1
        unicode_range_2_int = os2.ulUnicodeRange2
        unicode_range_3_int = os2.ulUnicodeRange3
        unicode_range_4_int = os2.ulUnicodeRange4

        expected_unicode_range_bits = generate_unicoderange_128bit_bitflag(tt)
        observed_unicode_range_bits = generate_128bit_bitflag_from_32bit_bitflags(
            unicode_range_1_int,
            unicode_range_2_int,
            unicode_range_3_int,
            unicode_range_4_int,
        )

        if expected_unicode_range_bits != observed_unicode_range_bits:
            # define ulUnicodeRange bit flags 1 - 4
            exp_uni_bitflag_1 = generate_shifted_32bit_unicoderange(
                expected_unicode_range_bits, 0
            )
            exp_uni_bitflag_2 = generate_shifted_32bit_unicoderange(
                expected_unicode_range_bits, 32
            )
            exp_uni_bitflag_3 = generate_shifted_32bit_unicoderange(
                expected_unicode_range_bits, 64
            )
            exp_uni_bitflag_4 = generate_shifted_32bit_unicoderange(
                expected_unicode_range_bits, 96
            )
            # set bits on the font
            tt["OS/2"].ulUnicodeRange1 = exp_uni_bitflag_1
            tt["OS/2"].ulUnicodeRange2 = exp_uni_bitflag_2
            tt["OS/2"].ulUnicodeRange3 = exp_uni_bitflag_3
            tt["OS/2"].ulUnicodeRange4 = exp_uni_bitflag_4

            # save font in place
            tt.save(fontpath)

            # reporting
            obs_128_str = f"{observed_unicode_range_bits:0128b}"
            exp_128_str = f"{expected_unicode_range_bits:0128b}"

            formatted_obs = re.sub("(.{32})", "\\1 ", obs_128_str, 0, re.DOTALL)
            formatted_exp = re.sub("(.{32})", "\\1 ", exp_128_str, 0, re.DOTALL)

            colored_change_string = ""

            # color changed bits in report string
            for index, c in enumerate(formatted_exp):
                if formatted_obs[index] != c:
                    colored_change_string += green(c)
                else:
                    colored_change_string += c

            print(f"{fontpath}:")
            print(f" PRE: {formatted_obs}")
            print(f"POST: {colored_change_string}\n")
        else:
            print(f"No change required in {fontpath}\n")


if __name__ == "__main__":
    if sys.argv[1] == "-v" or sys.argv[1] == "--version":
        print(VERSION)
    else:
        main(sys.argv[1:])
