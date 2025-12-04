#!/usr/bin/env python3
r"""
Simple merge of per-master FEA files into variable-scalar FEA.

Assumes all input files have IDENTICAL meaningful lines (same statements, same order).
Comments are stripped (except Glyphs magic comments); empty lines preserved.
Numeric values inside < > brackets are replaced with variable scalars if they differ.

Usage:
    python merge-variable-fea.py \
        telugu-opsz17-wght380.fea telugu-opsz17-wght734.fea \
        telugu-opsz18-wght380.fea telugu-opsz18-wght734.fea \
        -o telugu-variable.fea \
        -l "opsz=17,wght=400" "opsz=17,wght=700" "opsz=18,wght=400" "opsz=18,wght=700"

Each location string specifies the user-space axis coordinates for its corresponding
input file. The order of locations must match the order of input files.
These location strings are used verbatim in variable scalar output.
"""

import argparse
import re


# insertion markers used by Glyphs for auto-generated feature code
MAGIC_COMMENT_PREFIX = "# Automatic Code"

BRACKET_RE = re.compile(r"<[^>]+>")
NUMBER_RE = re.compile(r"-?\d+")


def is_meaningful(line: str) -> bool:
    """Return True if line contains FEA code (not comment/blank)."""
    stripped = line.strip()
    return stripped and not stripped.startswith("#")


def make_var_scalar(values: list[int], locations: list[str]) -> str:
    """Create variable scalar string, or plain int if all values equal."""
    if len(set(values)) == 1:
        return str(values[0])
    return "(" + " ".join(f"{loc}:{val}" for loc, val in zip(locations, values)) + ")"


def merge_line(lines: list[str], locations: list[str]) -> str:
    """Merge corresponding lines from all masters."""
    base = lines[0]

    # Find all < > brackets and process right-to-left
    for bracket in reversed(list(BRACKET_RE.finditer(base))):
        bracket_start, bracket_end = bracket.start(), bracket.end()
        bracket_text = bracket.group()

        # Get corresponding bracket from each master
        master_brackets = []
        for line in lines:
            m = BRACKET_RE.search(line[bracket_start:])
            master_brackets.append(m.group() if m else bracket_text)

        # Find numbers in base bracket, merge each
        new_bracket = bracket_text
        for num in reversed(list(NUMBER_RE.finditer(bracket_text))):
            idx = len(list(NUMBER_RE.finditer(bracket_text[: num.start()])))
            values = []
            for mb in master_brackets:
                nums = list(NUMBER_RE.finditer(mb))
                values.append(
                    int(nums[idx].group()) if idx < len(nums) else int(num.group())
                )

            new_bracket = (
                new_bracket[: num.start()]
                + make_var_scalar(values, locations)
                + new_bracket[num.end() :]
            )

        base = base[:bracket_start] + new_bracket + base[bracket_end:]

    return base


def merge_files(input_files: list[str], output_file: str, locations: list[str]):
    """Merge multiple FEA files into one with variable scalars."""
    all_lines = [open(f).readlines() for f in input_files]

    # Extract meaningful lines from each file
    meaningful = [[l for l in lines if is_meaningful(l)] for lines in all_lines]

    # Verify same count of meaningful lines
    counts = [len(m) for m in meaningful]
    if len(set(counts)) != 1:
        raise ValueError(f"Files have different statement counts: {counts}")

    # Verify line structures match (everything except numbers inside brackets)
    def structure(line: str) -> str:
        return NUMBER_RE.sub("#", line)

    for i in range(counts[0]):
        structures = [structure(m[i]) for m in meaningful]
        if len(set(structures)) != 1:
            raise ValueError(
                f"Line {i + 1} structure mismatch:\n"
                + "\n".join(
                    f"  {f}: {s.strip()}" for f, s in zip(input_files, structures)
                )
            )

    # Build output: empty lines preserved, most comments removed, statements merged
    result = []
    mi = 0
    for line in all_lines[0]:
        stripped = line.strip()
        if not stripped:
            result.append(line)  # Keep empty lines
        elif stripped.startswith("#"):
            if stripped.startswith(MAGIC_COMMENT_PREFIX):
                result.append(line)  # Keep magic comments
        else:
            lines_to_merge = [m[mi] for m in meaningful]
            result.append(merge_line(lines_to_merge, locations))
            mi += 1

    with open(output_file, "w") as f:
        f.writelines(result)

    text = "".join(result)
    var_count = sum(
        1 for _ in re.finditer(r"\(" + re.escape(locations[0].split(",")[0]), text)
    )
    print(f"Merged {counts[0]} statements, created {var_count} variable scalars")


def main():
    p = argparse.ArgumentParser(description="Merge per-master FEA into variable FEA")
    p.add_argument("files", nargs="+", help="Input FEA files")
    p.add_argument("-o", "--output", required=True, help="Output file")
    p.add_argument(
        "-l",
        "--locations",
        nargs="+",
        required=True,
        help="Master location in user-space coordinates for each input file "
        '(e.g. "opsz=17,wght=400"); must have same count as input files',
    )
    args = p.parse_args()

    if len(args.files) != len(args.locations):
        p.error("Number of files must match number of locations")

    merge_files(args.files, args.output, args.locations)


if __name__ == "__main__":
    main()
