# Google Sans Vendor Documentation

 These docs summarize how vendors contribute changes to the Google Sans project.  Detailed [maintainer documentation](MAINTAINER.md) is available if you would like to review additional details about build dependency installation, virtual environment management, and the fontmake compiler based build approach.

## Source Format

The Google Sans project uses [Unified Font Object](https://unifiedfontobject.org/) (UFO) version 3 formatted source files to build production fonts. Vendors may develop in glyphs version 2 or UFO version 3 formatted source files.  Scripts are provided to facilitate transformations between glyphs and UFO source file formats.

## UFO Source Conventions

The font sources we receive from vendors are scrubbed with custom scripts and stored as Designspaces and UFOs. The primary objective of the upstream UFO sources is to build the production fonts and serve as a base for vendors to split off from to make project changes.
<details>
<summary><strong>Source Normalization Details (click to open)</strong></summary>

The sources are normalized to be formatted in the way [fontTools.ufoLib](https://fonttools.readthedocs.io/en/latest/ufoLib/) formats sources and contain only:

* Foreground, intermediate (brace) and conditional (bracket) glyphs, no draft or background layers
  * whose metadata (lib keys) contains only semantically relevant data like Glyphs.app's metrics keys, but not color marks.
* Groups and kerning
* Manually merged and arranged features
* Manually maintained font info data
* Automatically managed UFO [lib.plist files](https://unifiedfontobject.org/versions/ufo3/lib.plist/), that contain:
  * `public.glyphOrder` for determining the order of glyphs in the final fonts
  * `public.postscriptNames` for determining the production glyph names in the final fonts
  * `public.skipExportGlyphs` for listing glyph names that should not be exported to the final fonts
  * `com.github.googlei18n.ufo2ft.filters` for listing filters and their options for compile-time font processing
    * `propagateAnchors`: inherits anchors of base glyphs to their composites automatically to help with building the `mark` and `mkmk` features.
  * `com.schriftgestaltung.customParameter.GSFont.Enforce Compatibility Check` for telling Glyphs.app to always run compatibility checks, not relevant for the build
  * `com.schriftgestaltung.customParameter.GSFont.disablesLastChange` for telling Glyphs.app to not put "last changed" markers into glyphs, which we don't need in the UFO format
  * `com.schriftgestaltung.fontMasterID` for making it easier to match vendor Glyphs.app files to be imported to the target UFOs
* Automatically managed UFO layer [layerinfo.plist files](https://unifiedfontobject.org/versions/ufo3/glyphs/layerinfo.plist/), that contain:
  * `com.schriftgestaltung.layerId` for hopefully helping exchange with Glyphs.app.
* Manually managed Designspace `<rules>` for describing conditional (bracket) glyphs
* Automatically managed Designspace instance and global libs, that contain:
  * Instances:
    * `com.schriftgestaltung.customParameters` for carrying build-relevant metadata like PANOSE values
  * Global:
    * `GSDimensionPlugin.Dimensions` for storing Glyphs.app's metadata for stem thicknesses
    * `com.github.googlei18n.ufo2ft.featureWriters` for build-relevant options on how to generate OpenType layout data
    * `public.skipExportGlyphs` for listing glyph names that should not be exported to the final fonts

</details>

## Font Format

We compile to OpenType variable and static instance fonts with quadratic outlines (*.ttf).

## Hinting

We do not use TrueType instruction sets.

## Requirements for Vendors

We ask the following from vendors who contribute to the Google Sans project:

* Follow type design conventions
* Use a required directory and file path structure
* Name glyphs, glyph classes, kerning groups, and lookups with the required format
* Develop and submit test documentation that allows us to perform initial and regression testing of shaping, new feature code, and feature code changes that are included in your updates

## Contributing to the Google Sans Project

### How to Submit Updates

1. Open a new issue with the title `[YOUR SCRIPT] merge: [OPTIONAL BRIEF DESCRIPTION]` on our [issue tracker](https://github.com/googlefonts/googlesans/issues).
2. Prepare a zip archive with your source files and associated test strings, documentation, and quality assurance testing tools.
3. Drag and drop the zip archive into the GitHub issue post that you opened in #1 above
