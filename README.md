# Google Sans

[![Static CI](https://github.com/googlefonts/googlesans/workflows/Static%20CI/badge.svg)](https://github.com/googlefonts/googlesans/actions?query=workflow%3A%22Static+CI%22)
[![Variable CI](https://github.com/googlefonts/googlesans/workflows/Variable%20CI/badge.svg)](https://github.com/googlefonts/googlesans/actions?query=workflow%3A%22Variable+CI%22)

Google Sans is a geometric sans-serif typeface for use as the corporate branding typeface. Originally based off of Product Sans (Design by Jesse Kaczmarek, Google Sans (Design by Colophon Foundry) has been modified for more general use.

Currently in 2 Optical Sizes (Google Sans & Google Sans Text), across three weights – Regular, Medium & Bold with corresponding Italics.

## Google Sans Source

The Google Sans project is developed in a two design axis design space with separate upright and italics `*.glyphs` source files. The design axes are defined as:

- `wght`: Regular and Bold masters
- `opsz`: min optical size is named "Google Sans Text" and max optical size is named "Google Sans"

The optical size axis range spans 14 pt (min master) to 18 pt (max master).

## Builds

We build 12 static instances that include interpolated Medium and Medium Italic builds. The static instance builds are our current production format. These builds can be found in `build/GoogleSans/static`.

Variable font builds are not production ready files at this stage. We currently build to two 2-axis variable font testing files. These include upright and italic build artifacts. These builds can be found in `build/GoogleSans/variable`.

You will find documentation to build the files from the glyphs source files in the [`docs/BUILD.md`](docs/BUILD.md) document.

## Usage

Usage documentation is available in [`USAGE.md`](USAGE.md).

## Other Documentation

Maintainer documentation can be found in [`docs/MAINTAINER.md`](docs/MAINTAINER.md).

## License

Google offers many fonts on open source terms. Google Sans is **not** one of them. Please see google.com/fonts for alternatives.
