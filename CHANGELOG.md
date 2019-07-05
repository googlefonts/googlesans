# Google Sans Changelog

## Version 2.004 (2019-07-05)

Android build generated to match Google Sans `yMin` and `yMax` values to that of Roboto. ([#71](https://github.com/Colophon-Foundry/google-sans/issues/71))

- Added `U+FFFD` glyph to match Roboto maximum values (Uses two barely-visible rectangles at the extremes).
- Within the Bold weights, the commaaccent combinational glyphs exceeded the yMin of Roboto. The `force_ymin_ymax_match_roboto.py` python script was run to force these values.
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

## Version 1.035 (2018-10-11)

This release was made for Android (GMSCore) distribution:

* Overhaul and simplify design space within `.glyphs` file.
* ~~Add Vietnamese language support. See [Vietnamese Extension List](Docs/Lists/VietnameseGlyphs.xml). ~~
* ~~Added 116 new glyphs. The full language list that Google Sans & Google Sans Display can be found in [LanguageList.txt](Docs/Lists/LanguageList.txt).~~
* [Diff Report Images](Docs/Changelogs/gf-sans_v1.35_imgs) are available