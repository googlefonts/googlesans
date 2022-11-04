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
* Provide a list of glyph names to import into the base sources ([see below](#getting-a-list-of-glyphs-and-kerning-groups)).
* Notify us if they want to change something in the base sources with their sources, as we will screen the changes out otherwise. This includes the names or contents of existing kerning groups or OpenType classes.
* Bundle up test documents for checking the correct shaping of text and application of features, to have tests for functionality after merging.

#### Getting a List Of Glyphs and (Kerning) Groups

Getting a list of glyph names usually involves selecting everything relevant in the editor and looking for the "copy glyph names" menu entry. The list should be saved to a text file (e.g. `import_glyphs.txt`) with one line per glyph name and appended to the PR. Example file contents:

```
thai_koKai
thai_thoThung
thai_phoSamphao
```

A glyph list is enough for the import. The import script will grab all kerning groups and pairs that contain any of the imported glyphs.

If you want more control over what groups are imported, you can provide a group list. Getting a group list needs a script, as Glyphs.app and Fontlab name kerning groups differently, making retrieval tedious. For Glyphs.app files, use:

```
$ python3 scripts/gs-print-kerning-groups.py source/GoogleSans/GoogleSansSomeScript.glyphs --glyphs-list import_glyphs.txt > import_groups.txt
```

Example file contents:

```
public.kern1.thai_saraE
public.kern1.space
public.kern2.thai_boBaimai
public.kern2.thai_khoKhuat
```

The resulting list in the file `import_groups.txt` will only contain groups that contain at least one glyph that is going to be imported. If you want to include more groups, add them manually. The name prefix `public.kern1.` marks groups "to the left" (RTL: right) and `public.kern2.` marks groups "to the right" (RTL: left). Note that the import process will grab all kerning pairs that include either a listed kerning group name or a glyph inside that kerning group.

Typically, you need to do both lists just once for your script and only change them if you actually add or remove a glyph or kerning group. If something needs to be remerged, the existing lists will work fine.

## Workflow

Vendors can use Glyphs.app to work on *.glyphs source files or work directly on UFOs and Designspaces with any editor. Vendors can go off and work on their script and come back once it is ready to be merged or commit their changes regularly to a branch, where we will do the merge process.

glyphsLib is used to generate Glyphs.app files for those who need it.

![Script Workflow](assets/scripts.png)

Vendors can either supply Designspace + UFO directly, or Glyphs.app files.
The merge process is the same, except that Glyphs.app files will first be
converted to the Designspace + UFO format.

![External Vendor Glyphs Workflow](assets/new_situation_glyphs.png)

![External Vendor UFO Workflow](assets/new_situation_ufo.png)



### Steps needed only when importing a Glyphs.app File

1. Place the vendor's Glyphs.app sources in the `source/GoogleSans/staging/` folder in this repository. If the folder does not yet exist, create it.

2. Turn the vendor's Glyphs.app sources into UFOs, in the same `source/GoogleSans/staging/` folder:

```bash
$ python scripts/gs-glyphs2ufo.py source/GoogleSans/staging/*.glyphs
```

Assuming the vendor delivered 2 Glyphs.app source files, uprights and italics, the `gs-glyphs2ufo.py` script will convert both to Designspace + UFOs and place them into the same `source/GoogleSans/staging/` folder.

### Steps in common for Designspace + UFO or Glyphs.app imports

3. Import the resulting Designspaces into their intended target Designspaces:

```bash
$ python3 scripts/gs-merge-designspace.py --source source/GoogleSans/staging/GoogleSansSomeScript.designspace --target source/GoogleSans/GoogleSans.designspace --import-glyphs-file source/GoogleSans/staging/import_glyphs.txt

$ python3 scripts/gs-merge-designspace.py --source source/GoogleSans/staging/GoogleSansSomeScript-Italic.designspace --target source/GoogleSans/GoogleSans-Italic.designspace --import-glyphs-file source/GoogleSans/staging/import_glyphs_italic.txt
```

(Note: if you also have a group list, specify it as an additional switch like so: `--import-groups-file import_groups_italic.txt`)

4. Check that glyphs, especially ligatures, have the correct production name set. Something like `k_ssa_uMatra-tamil` should have the production name `uni0B950BCD0BB70BC1`. Using Glyphs.app's naming conventions, you can cross-check names in Glyphs.app's macro panel with the following snippet:

```python
print(Glyphs.productionGlyphName("k_ssa_uMatra-tamil"))
```

5. Extract the features from the staging UFOs and manually merge them into the existing sources. The font info may also need to be updated, chiefly Unicode and codepage ranges.

6. Consider which of the imported glyphs need anchor propagation; edit the list kept in `scripts/internal/normalize.py`

7. Run `python3 scripts/gs-normalize-designspace.py`.

![Quality Assurance Workflow](assets/merge_process.png)

## Quality Assurance

Relies on testing material provided by vendors. Testing material should serve as a reference for how text should look and how features work. For testing, the vendor provided font is swapped with the merged font; if everything stays the same, the test is considered passed.

![Quality Assurance Workflow](assets/qa_process.png)

### Adding and Updating Text Shaping Regression Test Files

To ensure adding and changing feature code does not break existing font functionality, text shaping comparisons are run using HarfBuzz.

The directory `qa/shaping/` contains `.json` files of the following format:

```json5
{
  "input": {
    // Required, a list of strings to shape.
    "text": [
      "GS ĢȘ",
      "ԵԳԶՋԷԾ,;"
    ],
    // Required, a dictionary of features to enable (true) or disable (false).
    // Can be empty.
    "features": {
      "c2sc": true,
      "ss04": true
    },
    // Optional, the ISO 15924 script tag for the text.
    "script": "armn",
    // Optional, the BCP 47 language tag for the text.
    "language": "hy",
    // Optional, the script direction, one of "ltr", "rtl", "ttb" or "btt".
    "direction": "ltr",
    // Optional, the shaping output. Either "full", which includes offsets and
    // advance widths, or "glyphstream" for just the glyph names.
    "comparison_mode": "full"
  },
  "output": {
      // Per font file output goes here...
  }
}
```

The files currently have to be created by hand. Give them a descriptive name, ideally prefixed by the script they pertain to. To fill them with the shaping results of a list of fonts, essentially setting their output in stone, run:

```bash
$ python3 qa/update_shaping_test_data.py qa/shaping/my_file.json \
    build/GoogleSans/variable/*.ttf build/GoogleSans/static/*.ttf
```

To update all files in one go:

```bash
$ cd qa/
$ ./update_all_shaping.sh
```

The FontBakery QA tests will pick up the file automatically.

### Updating glyphset definitions

To ensure the built fonts contain all glyph definitions necessary, and no glyph definitions erroneously, lists of the glyph definitions expected of each font are maintained independently. In addition, the order of the definitions is recorded.

These lists are stored in `qa/definitions`.

After a merge, the lists must be updated to reflect the new definitions expected of the font. This can be performed as follows:

1. Rebuild the font, if this has not already been done after the merge.

2. Produce new lists based on the newly built fonts' glyph definitions.

```bash
$ python3 scripts/gs-update-glyphset-qa-files.py
```

3. Manually review the changes, to ensure that only the appropriate definitions have changed.

## Using Continuous Integration/Continuous Deployment (CI/CD) for Ongoing Development and Deployment

### Continuous Integration

The project uses GitHub Actions to automatically run build and checking jobs for Pull Requests.

When adding a new script or doing any font-related work, do so in a branch and open a Pull Request. By default, only the variable fonts are built and checked to save computing resources. If you want to trigger a build of the static and interpolated fonts, make a new branch with the same name, prefixed by "build-". So, your branch named "import-some-script" would become "build-import-some-script". Continuous Integration is set up to automatically build everything for branches with such a prefix. Avoid opening a Pull Request for these branches, as Continuous Integration will run twice.

### Continuous Deployment

When making a release, you can tag any commit (on the main branch or any other). It will compile everything for you and create a draft release for you to finalise, along with a Zip file with the release artifacts.
