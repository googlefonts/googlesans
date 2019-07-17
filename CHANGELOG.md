# Google Sans Changelog

## Version 2.004 (2019-07-05)

Android build generated to match Google Sans `yMin` and `yMax` values to that of Roboto. ([#71](https://github.com/Colophon-Foundry/google-sans/issues/71))

- Added `U+FFFD` glyph to match Roboto maximum values (Uses two barely-visible rectangles at the extremes).
- The glyph `U+0326` was reduced in the Bold & Bold Italic masters to have a yMax of `-271`. This change subsequently affected `U+0312` in both the Medium & Bold weights.
- Values Updated:
	- `yMin` : `-271`
	- `yMax` : `1056`
- Note – **NO** hinted versions were generated in this release.

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
    
    
* Glyphs Source:
	* Added in `Name Table Entry` attribute to all Instances for future binary generation.

* **!! NOTE !! Subsequent versions built from `v2.001` Hint source WILL require the above process applied again!**

## Version 2.002 (2019-04-09)

* **Non-used, interim variant**

* Swap of `GID 1159` (Romans) and `GID 1164` (Italics) (`uni000A`) which was causing an issue with Android. See [Issue 51](https://github.com/Colophon-Foundry/google-sans/issues/51) for more info.
* Swap was done to binaries from `v2.001` with a shell script provided [here](Tools/glyph_replace.sh):
	
* Source files have been updated to Version `2.002`, and have had `uni000A` replaced with `uniE007`.
* Source files have had the new (zero width) glyphs inserted, along with a glyphOrder attribute.
* Hint source files remain as-is, as I _think_ that subsetting on these source files will cause issues. Further investigation required.
* All files have been run through a script to force the yMin and yMax glyphs. This sets the values to the files from v1.027. Can be found in the /tools folder.

* **!! NOTE !! Subsequent versions from `v2.001` Hint source WILL require the above process applied again!**

## Version 2.001 (2018-11-19)

* Add Vietnamese language support. See [Vietnamese Extension List](Docs/Lists/VietnameseGlyphs.xml)
* Added 116 new glyphs. The full language list that Google Sans & Google Sans Display can be found in [LanguageList.txt](Docs/Lists/LanguageList.txt).
* All files have been run through a script to force the `yMin` and `yMax` glyphs. This sets the values to the files from `v1.027`. Can be found in the [/tools](/tools) folder.
* Android vs Hinted files is that Hinted files do NOT have the `SS03` Thin Numerals (used on Android home screens).
* Character map is the same otherwise (includes the new Vietnamese glyphs and anchor marks for composition).
* Glyphs Version `Glyphs2.5.1-1141`

## Version 1.043

* Internal (Pre-release)
* [Commit Link](7ee6e0bb4b04d7f8e0bd780f36fe2ede29a49031)
* Update to Anchor positions in Latin, Cyrillic & Greek glyphs. Ensuring all base characters have `top` and `bottom` anchors for compositional diacritic creation.
* `ogonek` composed forms. Adjusted the `bottom` anchor to sit directly below the characters as opposed to the side.

## Version 1.042

* Internal (Pre-release)
* [Commit Link](3138538dc1c09ff2ffe99f8e1f583ef1c029c986)
* `dash_dash`kerning removed due to [Issue 9](https://github.com/Colophon-Foundry/google-sans/issues/9)
* `slash_slash` kerning removed due to [Issue 9](https://github.com/Colophon-Foundry/google-sans/issues/9)
* `slash` and `backslash` glyphs updated forms to negate the larger side bearings and redaction of kerning.
* Vietnamese Glyphs added back-in. See [Vietnamese Extension List](Docs/Lists/VietnameseGlyphs.xml)
* `peso` forms updated to have two inlines as opposed to one. All variants updated (standard, tabular and cap).
* Removed previous bracket layers found in [Version 1.038](#version-1.038) 

## Version 1.041

* Internal (Pre-release)
* [Commit Link](a276e2b61a75dfc2d23e020af1da22eba908e1fe)
* Update to `dlig` feature code. Minor fix.

## Version 1.040

* Internal (Pre-release)
* [Commit Link](f5ac3761b708330b8f6ec928e5eed3e3df0acd12)
* Added bracklet layer to `Gcommaaccent` into Medium Instances
* Moved the bracket down to match `v1.027` `yMin` values

## Version 1.039

* Internal (Pre-release)
* Skip version number

## Version 1.038

* Internal (Pre-release)
* [Commit Link](5d568116acfbda71e0cd6089cdc1365bf1925e39)
* Added bracket layer into `horn.cap` character and raised the interpolation up by `1` unit to match the font `bBox` for `yMaxx`


## Version 1.037

* Internal (Pre-release)
* [Commit Link](9dbfaef009b9a1bbc6027cf67798eb0ffcce038c)
* Update maximum glyph bounding box to `964`

## Version 1.036

* Internal (Pre-release)
* [Commit Link](dcea705d991c7ca5151bc3f342f48d364e464a2a)
* Removal of Vietnamese Glyphs
* Remaining are the additional combination accent forms (used for Vietnamese), with the exception of the specifically designed `Ohorn` and `ohorn` glyphs.

## Version 1.035 (2018-10-11)

This release was made for Android (GMSCore) distribution:

* Overhaul and simplify design space within `.glyphs` file.
* ~~Add Vietnamese language support. See [Vietnamese Extension List](Docs/Lists/VietnameseGlyphs.xml). ~~
* ~~Added 116 new glyphs. The full language list that Google Sans & Google Sans Display can be found in [LanguageList.txt](Docs/Lists/LanguageList.txt).~~
* [Diff Report Images](Docs/Changelogs/gf-sans_v1.35_imgs) are available

## Version 1.034

* Internal (Pre-release)
* [Commit Link](52ef91e9b93a594c71ca07bdfa05619c250493a3)
* Display styles added
* Updated `mark` positioning (on Base forms)
* Final vietnamese marks
* Interpolation fixes
* Finalised feature code across both Romans & Italics

## Version 1.033

* Internal (Pre-release)
* [Commit Link](0771a50e7d173347fe10e1f3f2449583b5682193)
* Fixed vietnamese diacritic interpolation
* Italics Export
* Additional of supplementary glyphs for alt variants (e.g. `a.alt`)
* Updated feature code

## Version 1.032

* Internal (Pre-release)
* [Commit Link](4529d0965f08dcedaf02c05e5782d8f5ee2b017b)
* Update to the Android variants `liga` feature code

## Version 1.031

* Internal (Pre-release)
* [Commit Link](28e98b63902ef6262367cbd185be025098345fa7)
* New `liga` feature code containing modified Google_logo. See [Issue 13](https://github.com/Colophon-Foundry/google-sans/issues/13)


## Version 1.030

* Internal (Pre-release)
* [Commit Link](c65c6d5aeec0c8742a29bcf48d7f5d4e4bcd906c)
* Added PUA encoded glyphs for Google ligatures. See [Ligatures](../../README.md#ligatures) for more information.
* Versions < `v1.027` were exported with Glyphs version `1075`. With this build (Using version `1141`), there were significant changes to the way in which Glyphs interpolates using a three dimensional design space. It was impossible to repeat the same results with the same master files. Because of this we have made the extremes of the design to be masters, as opposed to interpolation/extrapolating the desired ranges.
	* Removed masters of original Product Sans design space (Thin, Black).
	* Removed control masters of original Google Sans (wider tracking, x-height axes etc).
	* Axes are now `Weight` and `Display`. Four masters in total, Regular & Bold, and in both Standard and Display variants.
	* Because of this, the Medium weight has altered very slightly. The changes in this instance is very minor. Both in stem weights and in interpolated spacing. 

## Version 1.029

* Internal (Pre-release)
* Hardware variant inclusion (separate project)
* [Commit Link](af7584602a7d34c8686dc748160e2bb159d1a80f)

## Version 1.028

* **Available Release**
* Hot-fixed by @m4rc1e and @davelab6
* [Commit Link](87ce8f85f4311d774e90e38714fdb8b1a65af63e)

## Version 1.027

* **Available Release**
* Last export done by EH
* [Commit Link](2ec29c65f5ea4c5e20556c333aa3ef063af53beb)
* All previous documentation done on Google Drive and Email chains.
* Beginning of repo.