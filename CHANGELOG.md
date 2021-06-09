# Google Sans Changelog

## Version 5.000

### New

- Add Armenian script support (#274)
- Add zero advance width control characters (issue #280, added in #306)

### Changed

- convert logo forms to components (#306)
- remove unnecessary outline data in U+00AD (soft hyphen)
- remove unnecessary outline data in U+200C (zero width nonjoiner)
- remove unnecessary outline data in U+200D (zero width joiner)

### Fixed

- added missing ldot (U+0140) small caps feature support (#276)
- swap outlines of K.alt into Ka-cy (#306)
- remove unneeded descender-cy and descender-cy.case glyphs (#306)
- remove unneeded ustraight-cy glyph (#306)
- remove unneeded localization ge-cy.loclSRB glyph (#306)
- remove unneeded G.ss06 glyph (#306)
- remove unneeded peace glyph (#306)
- remove unneeded whiteFrowningFace glyph (#306)
- remove unneeded whiteSmilingFace glyph (#306)
- remove unneeded apple glyph (#306)
- remove proprietary `#exit` anchor in Armenian designs (#306)
- remove duplicate logo glyph forms (#306)



## Version 4.000

### New

- new Latin, Greek, and Cyrillic script grade axis with a range of -50 to 200, variable font format only
- add LATIN CAPITAL LETTER SHARP S (U+1E9E)
- add LATIN CAPITAL LETTER SHARP S small cap form
- add c2sc feature support for new U+1E9E glyph
- add LATIN SMALL LETTER L WITH MIDDLE DOT (U+0140)

### Changed

- remove stylistic alternates
- remove `aalt` feature code
- reduce `ss04` character set to support only letters required for file size unit abbreviations
- rename `ss04` to "File Size Units"
- remove `ss08` Bulgarian locale stylistic set
- transition Latin and punctuation rvrn substitutions to interpolated forms with a sharp avar table
- improve location and scale of dagesh mark across the weight axis
- punctuation kerning improvements (includes double and single quote kerning changes)
- minor dollar, percent, and ampersand symbol design refinements
- execute subsetter on variable font format files (file size improvement)
- update fonttools dependency to v4.19.1
- update ufo2ft dependency to v2.19.2
- update glyphsLib dependency to v5.3.1


### Fixed

- fix logo ligatures have incorrect letter forms
- fix small caps `G` and `y` form bugs
- fix ligatures inappropriately exist in small caps
- eliminate transformed components, Cyrillic glyph set
- eliminate recursive component definitions

## Version 3.003

### New

- Add apostrophemod outline
- Add tetse-cy.sc outline
- Add ge-cy.loclSRB (italic only)
- Add gje-cy.loclMKD (italic only)

### Changed

- `[Uu]trait*-cy` glyph names changed to `[Uu]straight*-cy` and feature code updated
- Cyrillic kerning updates in Roman and Italic sets
- minor updates in Cyrillic Roman and Italic outlines
- glyphsLib normalization of *.glyphs type source files (addresses formatting inconsistencies between up/downstream files) with new Python source file and Makefile target
- removed unnecessary Robofont and RMXScaler metadata in glyphs source files
- updated attrs build dependency to v20.2.0
- updated cffsubr build dependency to v0.2.7
- updated fontmake build dependency to v2.2.0
- updated fontTools build dependency to v4.14.0
- updated glyphsLib build dependency to v5.1.11
- updated lxml build dependency to v4.5.2
- updated pyclipper build dependency to v1.2.0
- updated six build dependency to v1.15.0
- updated ufo2ft build dependency to v2.15.0
- updated ufolib2 build dependency to v0.8.0

### Fixed

- Removed Bulgarian language registration in `ss08` feature code

## Version 3.002

### New

The v3.002 release expands the Google Sans typeface with the Hebrew script (PR #76)

### Changed

- updated tabular zero design (`zero.tf`) to improve zero-zero spacing in time displays (#79)

### Fixed

- modified the `calt` feature source to use `colon.tf` as the replacement target in the contextual positioning of the colon between tabular figures (PR #80)

## Version 3.001

### New

The v3.001 release introduces production versions of the 2-axis variable font build format as our project default.

### Changed

- added `calt` feature support for figure centered colon position when the colon is set between numerals.  This addresses a request for always on/default behavior in time displays so that this appears when the SS02 design is not accessible in an environment

### Fixes

- Fix orientation of U+2998 and U+2999 arrow glyphs (PR #40)
- Fix rightArrow.ss05 path in regular max opsz master (addressed a non-interpolatable path issue)

### Technical

- Changed min optical size master definition to 17 px from 14 px to "remove" opsz axis interpolation
- Eliminated all brace layers in the design
- Move all bracket layers to 18 px
- Remove `build` directory and all build artifacts from version control (PR #8)
- Added partial instancing support for `wght` axis only variable font builds (PR #5)
  - adds new scripts/gs-partial-instancer.py script
  - adds new gs-stat-partial.py script
- Added one and two axis STAT table write support to the build pipeline
- Synchronized name, fvar, and STAT table naming so that there is a consistent naming approach across static and variable font format builds
- Added glyphs source file "Variable Font Origin" custom parameter with definition set to regular max opsz master to define our fvar table default
- Testing: transitioned fontbakery CI testing to GitHub Actions CI pipeline (PR #10)
- Testing: added OpenType Sanitizer checks to CI test pipeline (PR #13)
- Added support for git branch filtered test build artifact uploads (eliminates design team local build environment requirement) (PR #14)
- Added CLDR-based script and writing system coverage reporting to GitHub Actions CI pipeline (#16, #17)
- Added Python source file linting (flake8) to GitHub Actions CI pipeline (#18)
- Added setup.cfg configuration file with flake8 configuration settings
- Refactored Python scripts to address stylistic / logical linting issues identified by flake8
- Added `black` executable Python source formatting make target
- Dependency updates:
  - appdirs from 1.4.3 to 1.4.4
  - fontmake from 2.0.10 to 2.1.3
  - fontmath from 0.5.2 to 0.6.0 (required for VF scaling support)
  - fonttools from 4.4.1 to 4.10.2 (required for partial instancing support)
  - glyphslib from 5.1.7 to 5.1.10
  - lxml from 4.5.0 to 4.5.1
  - pytz from 2019.3 to 2020.1
  - adds typing-extensions requirement at 3.7.4.2
  - ufo2ft from 2.12.2 to 2.14.0
  - ufolib2 from 0.6.1 to 0.7.1
  - unicodedata2 from 12.1.0 to 13.0.0.post2
- Dependency management:
  - update wheel and setuptools on venv setup in make target
- Removed `tools/vf2s` source

## Version 3.000

### Deprecation Notice

- **The v3.xxx releases will be the last builds of Google Sans that include alternate glyph forms. This includes all `*.alt` glyphs and the `aalt` OpenType feature support for these characters**.

### General

- Transitioned to the `fontmake` font compiler from Glyphs application exports
- Removed Google Sans "Display" masters
- Eliminated "Android" build target
- Defined an "Expert" build target that includes the full source glyph set (default production build as of this release)
- Defined a "Default" build target that eliminates all `aalt` OpenType feature supported alternate glyph forms and associated feature support. These are not being released into production as of this release. We are posting a deprecation notice for all teams and will remove the alternates in the next major release of Google Sans.
- Removed TrueType instruction sets from all builds
- Added prep/gasp tables in place of TrueType instruction sets
- Moved underline position to -160 from -118 in max optical size designs

### Latin

- Added min opsz masters with a new design optimized for smaller text sizes
- Full Latin small caps with height set to the lower case alphabetic forms, this includes Vietnamese support
- moved the original small caps (A-Z a-z 0-9) with shorter glyph height metrics to a stylistic set (`ss04`)
- Change tabular figure (`tf`) width to `600` (Decrease of `-50`)
- `❛❝` Vertical rotation of incorrect form
- Add `ss05`; new stylistic set of arrows
- Vertical metrics adjusted to Roboto vertical metrics
- `U+0326` shrunk in Bold masters to accomodate Roboto vertical metrics
- Add additional input support for combining accent marks

### Greek

- Added min opsz masters with a new design optimized for smaller text sizes
- Extended Greek support added to meet the Google Fonts [Greek Plus](https://github.com/googlefonts/gftools/blob/master/Lib/gftools/encodings/GF%20Glyph%20Sets/Greek/GF-greek-plus.nam) glyph set encoding. This expansion includes extension to the Greek polytonic set.
- New small caps for the full Greek set with height set to the lower case alphabetic forms
- `ss06` Accented Greek small caps support
- `ss07` iota adscript support
- `dlig` updated to include Greek localisation support
- `calt` updated to include Greek localisation support

### Cyrillic

- Added min opsz masters with a new design optimized for smaller text sizes
- Extended Cyrillic support added to meet the Google Fonts [Cyrillic Plus](https://github.com/googlefonts/gftools/blob/master/Lib/gftools/encodings/GF%20Glyph%20Sets/Cyrillic/GF-cyrillic-plus_unique-glyphs.nam), [Cyrillic Plus Local Variants](https://github.com/googlefonts/gftools/blob/master/Lib/gftools/encodings/GF%20Glyph%20Sets/Cyrillic/GF-cyrillic-plus-locl_unique-glyphs.nam), and [Cyrillic Pro](https://github.com/googlefonts/gftools/blob/master/Lib/gftools/encodings/GF%20Glyph%20Sets/Cyrillic/GF-cyrillic-pro_unique-glyphs.nam) glyph set encodings
- New small caps for the full Cyrillic set with height set to the lower case alphabetic forms
- `locl` Updated feature code for localised alternates
- `ss08` Adds Bulgarian stylistic set support

## Version 2.004 (2019-07-22)

- **Note** – **NO** hinted versions were generated in this release. This is an unhinted build only bug fix release.

Android build generated to match Google Sans `yMin` and `yMax` values to that of the Roboto / Noto Sans UI font stack. ([#71](https://github.com/Colophon-Foundry/google-sans/issues/71))

- Added `U+FFFD` glyph. This glyph was required by the Android Text team. We designed it to match Roboto yMin/yMax values (uses two barely-visible rectangles at the extremes) so that any downstream edits to the files with libraries/executables that recalculate bounding boxes based on calculations across the glyph set identify and set these newly defined, desired yMin/yMax values. This is to address an issue with fixed vertical metrics Android UI layouts.
- The glyph `U+0326` was reduced in the Bold & Bold Italic masters to have a yMin of `-271`. This change subsequently affected `U+0312` in both the Medium & Bold weights.
- Values Updated: - `head.yMin` : `-271` - `head.yMax` : `1056`
- eliminated the yMin/yMax post-compile editing script as this is no longer necessary after the changes in this update
- Within Medium Italic instance, changed the name attribute entry to the correct specification: - `3 3 1 1033; Google;GoogleSans-MediumItalic`
- Fixed panose to match the values that are used in the `v2.003` release of the unhinted Android builds
- Update unicode value in `uniE007` (E007) to correct value in Italics source file.
- Updated vietnamese `O` characters to be auto-aligned within Glyphs.

## Version 2.003 (2019-04-29)

This build involved `ttx` based OpenType table edits of the v2.001 build of the Google Sans fonts to avoid reordering the glyphID (which would require repeat manual VTT hinting of the fonts).

- re-encoded the U+000A glyph (line feed) to a PUA encoded code point at U+E007 ([#51](https://github.com/Colophon-Foundry/google-sans/issues/51))
- Edit of OpenType name table record nameID 0 ([#24](https://github.com/Colophon-Foundry/google-sans/issues/24))
  - changed "Google, Inc" to "Google LLC"
  - changed copyright year to 2015 from 2017
- Edit of OpenType name table record nameID 8 ([#24](https://github.com/Colophon-Foundry/google-sans/issues/24))
  - changed "Google, Inc" to "Google LLC"
- Edit of OpenType name table record nameID 3 ([#52](https://github.com/Colophon-Foundry/google-sans/issues/52))
  - removed version number from the unique ID string and revised string format

* Glyphs Source: \* Added in `Name Table Entry` attribute to all Instances for future binary generation.

* **!! NOTE !! Subsequent versions built from `v2.001` Hint source WILL require the above process applied again!**

## Version 2.002 (2019-04-09)

- **Non-used, interim variant**

- Swap of `GID 1159` (Romans) and `GID 1164` (Italics) (`uni000A`) which was causing an issue with Android. See [Issue 51](https://github.com/Colophon-Foundry/google-sans/issues/51) for more info.
- Swap was done to binaries from `v2.001` with a shell script provided [here](Tools/glyph_replace.sh):
- Source files have been updated to Version `2.002`, and have had `uni000A` replaced with `uniE007`.
- Source files have had the new (zero width) glyphs inserted, along with a glyphOrder attribute.
- Hint source files remain as-is, as I _think_ that subsetting on these source files will cause issues. Further investigation required.
- All files have been run through a script to force the yMin and yMax glyphs. This sets the values to the files from v1.027. Can be found in the /tools folder.

- **!! NOTE !! Subsequent versions from `v2.001` Hint source WILL require the above process applied again!**

## Version 2.001 (2018-11-19)

- Add Vietnamese language support. See [Vietnamese Extension List](Docs/Lists/VietnameseGlyphs.xml)
- Added 116 new glyphs. The full language list that Google Sans & Google Sans Display can be found in [LanguageList.txt](Docs/Lists/LanguageList.txt).
- All files have been run through a script to force the `yMin` and `yMax` glyphs. This sets the values to the files from `v1.027`. Can be found in the [/tools](/tools) folder.
- Android vs Hinted files is that Hinted files do NOT have the `SS03` Thin Numerals (used on Android home screens).
- Character map is the same otherwise (includes the new Vietnamese glyphs and anchor marks for composition).
- Glyphs Version `Glyphs2.5.1-1141`

## Version 1.043

- Internal (Pre-release)
- [Commit Link](7ee6e0bb4b04d7f8e0bd780f36fe2ede29a49031)
- Update to Anchor positions in Latin, Cyrillic & Greek glyphs. Ensuring all base characters have `top` and `bottom` anchors for compositional diacritic creation.
- `ogonek` composed forms. Adjusted the `bottom` anchor to sit directly below the characters as opposed to the side.

## Version 1.042

- Internal (Pre-release)
- [Commit Link](3138538dc1c09ff2ffe99f8e1f583ef1c029c986)
- `dash_dash`kerning removed due to [Issue 9](https://github.com/Colophon-Foundry/google-sans/issues/9)
- `slash_slash` kerning removed due to [Issue 9](https://github.com/Colophon-Foundry/google-sans/issues/9)
- `slash` and `backslash` glyphs updated forms to negate the larger side bearings and redaction of kerning.
- Vietnamese Glyphs added back-in. See [Vietnamese Extension List](Docs/Lists/VietnameseGlyphs.xml)
- `peso` forms updated to have two inlines as opposed to one. All variants updated (standard, tabular and cap).
- Removed previous bracket layers found in [Version 1.038](#version-1.038)

## Version 1.041

- Internal (Pre-release)
- [Commit Link](a276e2b61a75dfc2d23e020af1da22eba908e1fe)
- Update to `dlig` feature code. Minor fix.

## Version 1.040

- Internal (Pre-release)
- [Commit Link](f5ac3761b708330b8f6ec928e5eed3e3df0acd12)
- Added bracklet layer to `Gcommaaccent` into Medium Instances
- Moved the bracket down to match `v1.027` `yMin` values

## Version 1.039

- Internal (Pre-release)
- Skip version number

## Version 1.038

- Internal (Pre-release)
- [Commit Link](5d568116acfbda71e0cd6089cdc1365bf1925e39)
- Added bracket layer into `horn.cap` character and raised the interpolation up by `1` unit to match the font `bBox` for `yMaxx`

## Version 1.037

- Internal (Pre-release)
- [Commit Link](9dbfaef009b9a1bbc6027cf67798eb0ffcce038c)
- Update maximum glyph bounding box to `964`

## Version 1.036

- Internal (Pre-release)
- [Commit Link](dcea705d991c7ca5151bc3f342f48d364e464a2a)
- Removal of Vietnamese Glyphs
- Remaining are the additional combination accent forms (used for Vietnamese), with the exception of the specifically designed `Ohorn` and `ohorn` glyphs.

## Version 1.035 (2018-10-11)

This release was made for Android (GMSCore) distribution:

- Overhaul and simplify design space within `.glyphs` file.
- ~~Add Vietnamese language support. See [Vietnamese Extension List](Docs/Lists/VietnameseGlyphs.xml). ~~
- ~~Added 116 new glyphs. The full language list that Google Sans & Google Sans Display can be found in [LanguageList.txt](Docs/Lists/LanguageList.txt).~~
- [Diff Report Images](Docs/Changelogs/gf-sans_v1.35_imgs) are available

## Version 1.034

- Internal (Pre-release)
- [Commit Link](52ef91e9b93a594c71ca07bdfa05619c250493a3)
- Display styles added
- Updated `mark` positioning (on Base forms)
- Final vietnamese marks
- Interpolation fixes
- Finalised feature code across both Romans & Italics

## Version 1.033

- Internal (Pre-release)
- [Commit Link](0771a50e7d173347fe10e1f3f2449583b5682193)
- Fixed vietnamese diacritic interpolation
- Italics Export
- Additional of supplementary glyphs for alt variants (e.g. `a.alt`)
- Updated feature code

## Version 1.032

- Internal (Pre-release)
- [Commit Link](4529d0965f08dcedaf02c05e5782d8f5ee2b017b)
- Update to the Android variants `liga` feature code

## Version 1.031

- Internal (Pre-release)
- [Commit Link](28e98b63902ef6262367cbd185be025098345fa7)
- New `liga` feature code containing modified Google_logo. See [Issue 13](https://github.com/Colophon-Foundry/google-sans/issues/13)

## Version 1.030

- Internal (Pre-release)
- [Commit Link](c65c6d5aeec0c8742a29bcf48d7f5d4e4bcd906c)
- Added PUA encoded glyphs for Google ligatures. See [Ligatures](../../README.md#ligatures) for more information.
- Versions < `v1.027` were exported with Glyphs version `1075`. With this build (Using version `1141`), there were significant changes to the way in which Glyphs interpolates using a three dimensional design space. It was impossible to repeat the same results with the same master files. Because of this we have made the extremes of the design to be masters, as opposed to interpolation/extrapolating the desired ranges.
  _ Removed masters of original Product Sans design space (Thin, Black).
  _ Removed control masters of original Google Sans (wider tracking, x-height axes etc).
  _ Axes are now `Weight` and `Display`. Four masters in total, Regular & Bold, and in both Standard and Display variants.
  _ Because of this, the Medium weight has altered very slightly. The changes in this instance is very minor. Both in stem weights and in interpolated spacing.

## Version 1.029

- Internal (Pre-release)
- Hardware variant inclusion (separate project)
- [Commit Link](af7584602a7d34c8686dc748160e2bb159d1a80f)

## Version 1.028

- **Available Release**
- Hot-fixed by @m4rc1e and @davelab6
- [Commit Link](87ce8f85f4311d774e90e38714fdb8b1a65af63e)

## Version 1.027 (2018-01-22)

- **Available Release**
- Last export done by EH
- [Commit Link](2ec29c65f5ea4c5e20556c333aa3ef063af53beb)
- All previous documentation done on Google Drive and Email chains.
- Beginning of repo.

This was distributed within Google as `GoogleSans-22Jan2018-v1_27.zip`

As of Version 1.27, the Android versions now have a CALT feature, with updated feature code.

Hinted files are v1.26, and then modified via ttx.
The additional (compiled) code from a straight export is then pasted into the calt rule to extend this.
Version number has been incremented.

**Note** – The VTT sources are STILL v1.26, so any subsequent versions will need to have all updates manually inserted from here.

- Source (glyph) files have been incremented and have the new additions in (just not the hinting).
