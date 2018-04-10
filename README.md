# Google Sans
## Version 1.27
• As of Version 1.27, the Android versions now have a CALT feature, with updated feature code.

* Hinted files are v1.26, and then ttx ran. The additional (compiled) code from a straight export is then pasted into the calt rule to extend this. Version number has been incremented.

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

#Instances
There are 18 Instances set up Google Sans. Some of which are purely referential.

##Hinted

###Google Sans Regular
* Weight: 380
* Width: 170
* Custom: 70
* State: Active
	- These remove the calt and ss03 feature, and then update the feature code and are NOT hinted. 
	- This is an export ready for VTT

###Google Sans Display Regular
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

###Google Sans Display Bold
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

##Android

**Android** files are exported straight from Glyphs. They then have the ```fontbakery-fix-cmap.py``` command ran with the ```-f4 -k0 -dm``` sub options.

##Hinted

**Hinted** files are exported from VTT. Upon export, these have then been through ```ttx``` to remove `nameID=14` (this was included in an old binary and now has to be removed manually). 
Version numbers are incremented via ```fontbakery-update-version.py```