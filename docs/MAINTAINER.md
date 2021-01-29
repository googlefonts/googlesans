# Google Sans Repository Maintainer Documentation

## Project Dependency Management

The Google Sans typeface build workflow requires the following:

- Python 3.6+ interpreter
- [`fontmake`](https://github.com/googlefonts/fontmake) Python package
- `make`

Optional dependencies for project maintainers include:

- [`pip-tools` Python package](https://github.com/jazzband/pip-tools) - used to maintain the dependencies defined in the `requirements.txt` file

Install the `pip-tools` package with:

```
$ pip3 install --upgrade pip-tools
```

### How to Update Project Dependency Versions

The Python dependencies are defined in the `requirements.txt` file at the root of the repository.  This file is generated from the `requirements.in` file with the `pip-compile` executable, a tool that is part of the free [`pip-tools` Python package](https://github.com/jazzband/pip-tools).

Execute the following command in the root of the project repository to update the depenency version numbers to current release versions:

```
$ pip-compile --upgrade
```

This command is included in a `make` target as a convenience:

```
$ make update-deps
```

The updated `requirements.txt` file should be committed to the git version control history.  Project builders must be aware that this file was updated so that existing venv's can be synchronized with the new version definitions.  The changes will be reflected immediately in any new venv's that are generated as of the `requirements.txt` file change commit.

### How to List Project Dependency Versions Installed in `.venv`

```
$ make list-deps
```

### How to Synchronize Project Dependencies in an Existing `.venv` with Updated `requirements.txt` Definitions

```
$ make sync-deps
```

## Source Conventions

Our source code style guidance is documented in [STYLE.md](STYLE.md).

The font sources we receive from vendors are scrubbed with custom scripts and stored as Designspaces and UFOs. The primary objective of the sources is to build the fonts and serve as a base for vendors to split off from to work on new scripts.

<details>
<summary><strong>Source Normalization Details (click to open)</strong></summary>

The sources are normalized according to [fontTools.ufoLib](https://fonttools.readthedocs.io/en/latest/ufoLib/) formatting and contain only:

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

### Normalizing Sources and Updating GDEF

Normalize the sources (reset formatting, scrub data and remake the GDEF table) with

```
$ python3 scripts/gs-normalize-designspace.py
```

### Conventions for External Vendors

To make merges into the main source base as seamless as possible, vendors should

* Place their source files into the existing `source/GoogleSans/` directory but use different names from the base sources.
* Ideally make no use of intermediate (brace) layers if the design allows it.
* Name all glyphs according to the naming standard used by Glyphs.app and ideally not change them after the first time they've been imported to the base sources.
* Keep the sources buildable with `fontmake`. Various advanced Glyphs.app features are off-limits because the open-source pipeline does not support them, among them smart components.
* Provide a list of glyph names and group names to import into the base sources ([see below](#getting-a-list-of-glyphs-and-kerning-groups)).
* Notify us if they want to change something in the base sources with their sources, as we will screen the changes out otherwise. This includes the names or contents of existing kerning groups or OpenType classes.
* Bundle up test documents for checking the correct shaping of text and application of features, to have tests for functionality after merging.

#### Getting a List Of Glyphs and (Kerning) Groups

Getting a list of glyph names usually involves selecting everything relevant in the editor and looking for the "copy glyph names" menu entry. The list should be saved to a text file with one line per glyph name and appended to the PR. Example file contents:

```
thai_koKai
thai_thoThung
thai_phoSamphao
```

Getting a group list needs a script, as Glyphs.app and Fontlab name kerning groups differently, making retrieval tedious. For Glyphs.app files, use:

```
$ python3 scripts/gs-print-kerning-groups.py source/GoogleSans/GoogleSansSomeScript.glyphs > import_groups.txt
```

Example file contents:

```
public.kern1.thai_saraE
public.kern1.space
public.kern2.thai_boBaimai
public.kern2.thai_khoKhuat
```

The resulting list in the file `import_groups.txt` should be screened to contain only what should be imported and appended to the PR. The name prefix `public.kern1.` marks groups "to the left" (RTL: right) and `public.kern2.` marks groups "to the right" (RTL: left).

## Workflow

Vendors can use Glyphs.app to work on *.glyphs source files or work directly on UFOs and Designspaces with any editor. Vendors can go off and work on their script and come back once it is ready to be merged or commit their changes regularly to a branch, where we will do the merge process.

glyphsLib is used to generate Glyphs.app files for those who need it.

![Script Workflow](assets/scripts.png)

### Importing a Glyphs.app File

![External Vendor Glyphs Workflow](assets/new_situation_glyphs.png)

First, run the `gs-glyphs2ufo.py` script for the upright and italic source to convert the source files and place them into `source/GoogleSans/staging/`.

```
$ python3 scripts/gs-glyphs2ufo.py source/GoogleSans/GoogleSansSomeScript.glyphs --target-dir source/GoogleSans/staging/

$ python3 scripts/gs-glyphs2ufo.py source/GoogleSans/GoogleSansSomeScript-Italic.glyphs --target-dir source/GoogleSans/staging/
```

Next, import the resulting Designspaces into their intended target Designspaces:

```
$ python3 scripts/gs-merge-designspace.py \
    --source source/GoogleSans/staging/GoogleSansSomeScript.designspace \
    --target source/GoogleSans/GoogleSans.designspace \
    --import-glyphs-file import_glyphs.txt \
    --import-groups-file import_groups.txt

$ python3 scripts/gs-merge-designspace.py \
    --source source/GoogleSans/staging/GoogleSansSomeScript-Italic.designspace \
    --target source/GoogleSans/GoogleSans-Italic.designspace \
    --import-glyphs-file import_glyphs_italic.txt \
    --import-groups-file import_groups_italic.txt
```

Now extract the features from the staging UFOs and manually massage them into the existing sources. The font info may also need to be updated, chiefly Unicode and codepage ranges. Additionally, consider which of the imported glyphs need anchor propagation (the list is kept in `scripts/internal/normalize.py`, re-run `scripts/gs-normalize-designspace.py` when you modify it).

![Quality Assurance Workflow](assets/merge_process.png)

### Importing Designspaces with UFOs

The same as the [Glyphs.app workflow](#importing-a-glyphsapp-file), except we don't convert anything beforehand.

![External Vendor UFO Workflow](assets/new_situation_ufo.png)

## Quality Assurance

Relies on testing material provided by vendors. Testing material should serve as a reference for how text should look and how features work. For testing, the vendor provided font is swapped with the merged font; if everything stays the same, the test is considered passed.

![Quality Assurance Workflow](assets/qa_process.png)
