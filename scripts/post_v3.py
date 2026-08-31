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
        help="path to write patched TTF to (defaults to fonts/release)",
    )

    args = parser.parse_args()
    output: Path = args.output or Path("fonts/release") / args.font.relative_to("fonts")
    output.parent.mkdir(parents=True, exist_ok=True)
    process_font(args.font, output)
    print(f"Wrote {args.font} to {output} with post v3")
