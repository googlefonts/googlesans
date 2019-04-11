# Google Sans

## Version 2.003 (2019-04-11)

* **AWAITING APPROVAL OF RELEASE**
* Fixes for Issue #24 and Issue #52
* Fixes done via TTX:
	* Manufacturer Name
	* Copyright Notice	
	* nameID 3
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


### Ligatures

Google Ligatures are now available in both contextual and PUA encoded flavours.

```
Glogo => E000
ologo => E001
glogo => E002 
llogo => E003
elogo => E004
Gsuper => E005
Googlelogo => E006
```

Additional code is now in the `liga` feature:

```
[Gg]oogleligature => Google.logo
Glogoligature => G.logo
ologoligature => o.logo
glogoligature => g.logo
llogoligature => l.logo
elogoligature => e.logo
```

### Styles Updated

* Google Sans
	* Regular
	* Italic
	* Medium
	* Medium Italic
	* Bold
	* Bold Italic
* Google Sans Display
	* Regular
	* Italic
	* Medium
	* Medium Italic
	* Bold
	* Bold Italic

## GlyphsApp Update

When GlyphsApp updated from v1075 to v1141, there was significant changes to the way in-which it interpolated a 3 dimensional design space. It is impossible to produce the same results of which the previous master files (v1.028 and before) output originally. Because of this, we have created the extreme corners of the design space to ensure consistent interpolation. These are now Regular, Bold, Display Regular and Display Bold; across two axes, Weight and Width.

Compiled with Glyphs v1075 ([Glyphs2.4.4-1075.zip](https://updates.glyphsapp.com/Glyphs2.4.4-1075.zip))

## Version 1.27 (2018-01-22)

This was distributed within Google asn `GoogleSans-22Jan2018-v1_27.zip`

As of Version 1.27, the Android versions now have a CALT feature, with updated feature code.

Hinted files are v1.26, and then modified via ttx.
The additional (compiled) code from a straight export is then pasted into the calt rule to extend this.
Version number has been incremented.

**Note** – The VTT sources are STILL v1.26, so any subsequent versions will need to have all updates manually inserted from here.

* Source (glyph) files have been incremented and have the new additions in (just not the hinting).

# Glyphs
Within /Master Files/Glyphs are two .glyphs files containing the master drawings for both the Upright drawings and the Italics. They are set up identically for ease-of-use.

## Masters
There are six masters set up for Google Sans:

* **Thin**
> Taken from Product Sans. The thinnest style

* **Thin X-Height**
> Latest Master to create Google Hardware addition

* **Regular**
> Base Product Sans Regular
 
* **X-Height**
> Drawn as a super high x-height. Used as a custom master for adjusting the x-height of Google Sans
* **Thin Extended**
> A duplicate of the Thin master. Has extended metrics needed for increasing overall letterspacing.
* **Extended**
> As Thin Extended, but for the Regular style
* **Black**
> Taken from Product Sans. The boldest style. Used to interolate the Bold/Medium styles

# Instances
There are 18 Instances set up Google Sans. Some of which are purely referential.

## Hinted

### Google Sans Regular
* Weight: 380
* Width: 170
* Custom: 70
* State: Active
	- These remove the calt and ss03 feature, and then update the feature code and are NOT hinted. 
	- This is an export ready for VTT

### Google Sans Display Regular
* Weight: 380
* Width: 150
* Custom: 22
* State: Active
	- These remove the calt and ss03 feature, and then update the feature code and are NOT hinted. 
	- This is an export ready for VTT

### Google Sans Medium
* Weight: 555
* Width: 170
* Custom: 70
* State: Active
	- These remove the calt and ss03 feature, and then update the feature code and are NOT hinted. 
	- This is an export ready for VTT

### Google Sans Display Medium
* Weight: 555
* Width: 150
* Custom: 22
* State: Active
	- These remove the calt and ss03 feature, and then update the feature code and are NOT hinted. 
	- This is an export ready for VTT

### Google Sans Bold
* Weight: 734
* Width: 170
* Custom: 70
* State: Active
	- These remove the calt and ss03 feature, and then update the feature code and are NOT hinted. 
	- This is an export ready for VTT

### Google Sans Display Bold
* Weight: 734
* Width: 150
* Custom: 22
* State: Active
	- These remove the calt and ss03 feature, and then update the feature code and are NOT hinted. 
	- This is an export ready for VTT

## Android

### Google Sans Regular
* State: Inactive
	- Has additional 'ss03' opentype in the Upright, removed 'calt' feature.

### Google Sans Display Regular
* State: Inactive
	- As above, but ready for Hinting

### Google Sans Medium
* State: Inactive
	- As above, but ready for Hinting

### Google Sans Display Medium
* State: Inactive
	- As above, but ready for Hinting

### Google Sans Bold
* State: Inactive
	- As above, but ready for Hinting

### Google Sans Display Bold
* State: Inactive
	- As above, but ready for Hinting
	

## LEGACY PRODUCT SANS

* Product Sans Thin
* Product Sans Light
* Product Sans Regular
* Product Sans Medium
* Product Sans Bold
* Product Sans Black

>	Not used. A reference to original Product Sans Designs

# VTT Master Files

All these files contain high-level TrueType instructions (hence the large file size [~700kb]).
For exports, go to: `Ship Font`.

These will then need the `CALT` feature code and version number adding/incrementing.

# Exports

Hinted files (from VTT) have been made into webfonts with the following terminal commands:

```console
$ sfnt2off
$ woff2_compress
$ ttf2eot
```

# Process

## Android

**Android** files are exported straight from Glyphs. They then have the ```fontbakery-fix-cmap.py``` command ran with the ```-f4 -k0 -dm``` sub options.

## Hinted

**Hinted** files are exported from VTT. Upon export, these have then been through ```ttx``` to remove `nameID=14` (this was included in an old binary and now has to be removed manually). 
Version numbers are incremented via ```fontbakery-update-version.py```

## Hardware 

The latest hardware build has been branched out of the main design space. This has been created by making an instance in the main design space, and then generating this as a master. This was down primarily to inconistent curves and drawing which could only be rectified by manual intervention.

## Site

https://colophon-foundry.github.io/variable-web-viewer/
pw conway
