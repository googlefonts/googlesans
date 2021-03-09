# Google Sans

[![Static CI](https://github.com/googlefonts/googlesans/workflows/Static%20CI/badge.svg)](https://github.com/googlefonts/googlesans/actions?query=workflow%3A%22Static+CI%22)
[![Variable CI](https://github.com/googlefonts/googlesans/workflows/Variable%20CI/badge.svg)](https://github.com/googlefonts/googlesans/actions?query=workflow%3A%22Variable+CI%22)

Google Sans is a geometric sans-serif typeface for use as the corporate branding typeface. Originally based off of Product Sans, the Google Sans design has been modified for more general purpose use across systems, product areas, advertising, and marketing.

The typeface currently supports optical size, weight, and grade design axes.

## Google Sans Source

The Google Sans project is developed in a three axis design space with separate Roman and Italic UFO source masters.

- `wght`: range 400 - 700; default=400
- `opsz`: range 17 - 18; default=18. The min optical size design is named "Google Sans Text" and the max optical size design is named "Google Sans"
- `GRAD`: range -50 to 200; default=0

GRAD axis support is available in the variable font format only.

## Builds

We build 12 static instance artifacts that include interpolated Medium and Medium Italic files.

We build separate Roman and Italic variable font artifacts.

Production files are available in our project [Releases](https://github.com/googlefonts/googlesans/releases).

Our continuous integration test suite compiles files at each commit. You can access commit level builds by pushing a branch that uses the prefix `build-*` in the branch name.  The builds are available through the GitHub UI in our [Artifact Uploads action](https://github.com/googlefonts/googlesans/actions/workflows/upload-artifacts.yml).

You will find documentation to build the files from the designspace + UFO source files in the [`docs/BUILD.md`](docs/BUILD.md) document.

## Usage

Usage documentation is available in [`USAGE.md`](USAGE.md).

## Other Documentation

Maintainer documentation can be found in [`docs/MAINTAINER.md`](docs/MAINTAINER.md).

## License

Google offers many fonts on open source terms. Google Sans is **not** one of them. Please see google.com/fonts for alternatives.
