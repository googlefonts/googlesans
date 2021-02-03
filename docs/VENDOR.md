# Google Sans Vendor Documentation

This document summarizes how vendors contribute changes to the Google Sans project.  Detailed [maintainer documentation](MAINTAINER.md) is available if you would like to review additional details about build dependency installation, virtual environment management, and the fontmake compiler based build approach.

## Source Format

The Google Sans project uses [Unified Font Object](https://unifiedfontobject.org/) (UFO) version 3 formatted source files to build production fonts. Vendors may develop in glyphs format version 2 or UFO format version 3 source files. Scripts are provided in this repository to facilitate transformations between glyphs and UFO source file formats.

## UFO Source Conventions

The font sources that we receive from vendors are cleaned with custom scripts and stored as Designspaces and UFOs to create our production source files. The primary objective of the upstream UFO sources is to build the production fonts and serve as a basis for future development of the type software.

Please refer to the [Source Normalization Details section of the MAINTAINER.md document](MAINTAINER.md#source-conventions) for additional information about the source normalization process.

## Font Format

We compile to OpenType variable and static instance fonts with quadratic outlines (*.ttf).

## Hinting

We do not use TrueType instruction sets.

## Style

Please refer to [STYLE.md](STYLE.md) for source style guidelines.  The document includes information on how to format your source files in order to contribute to this project.

## Requirements for Vendors

We ask the following from vendors who contribute to the Google Sans project:

* Follow type design conventions
* Use a required directory and file path structure
* Name glyphs, glyph classes, kerning groups, and lookups with the required format
* Develop and submit test documentation that allows us to perform initial and regression testing of shaping, new feature code, and feature code changes that are included in your updates

## Contributing to the Google Sans Project

### Generating Glpyhs.app Source Files

If you work in Glyphs.app and want to generate sources for modification, skip using Glyphs.app's built-in im- and exporter functionality. Instead, run:

```
$ python3 scripts/gs-ufo2glyphs.py source/GoogleSans/GoogleSans.designspace

$ python3 scripts/gs-ufo2glyphs.py source/GoogleSans/GoogleSans-Italic.designspace
```

It's best to rename the files to include the script you're working on, e.g. "GoogleSans_Devanagari.glyphs".

You can post those source files directly to us, no back-conversion necessary, see below.

### How to Submit Updates

1. Open a new issue with the title `[YOUR SCRIPT] merge: [OPTIONAL BRIEF DESCRIPTION]` on our [issue tracker](https://github.com/googlefonts/googlesans/issues).
2. Prepare a zip archive with your source files and associated test strings, documentation, and quality assurance testing tools.
3. Drag and drop the zip archive into the GitHub issue post that you opened in #1 above
