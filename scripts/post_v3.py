from pathlib import Path

from fontTools.ttLib import TTFont


def process_font(read_from: Path, write_to: Path) -> None:
    ttf = TTFont(read_from)
    ttf["post"].formatType = 3.0  # type: ignore
    ttf.save(write_to)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "font",
        type=Path,
        help="path to TTF",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="path to write patched TTF to",
    )

    args = parser.parse_args()
    output = args.output or args.font
    process_font(args.font, output)
    print(f"Wrote {args.font.name} to {output} with post v3")
