# Google Sans Text

The first prototype of the Google Sans Text optical size has a series of user-configurable axes that allow granular modification of different aspects of Google Sans Regular for use in small point sizes and long body copy.

* The core output is a [variable font](betas/20190215/Variable/GoogleSansTextBeta-v2.004.ttf) in `.ttf` format. This is then viewed in the [web viewer](https://colophon-foundry.github.io/variable-web-viewer). Password `conway`
* The second output are [static instances](betas/20190225/Preset%20Instances) of our recommendations.
	* There is a PDF overview document detailing these in the [Docs](Docs) folder.

## Betas

* Variable font TTF
	* Variable TTF used in the web viewer. 
* Preset Instances
	* Local install ready static fonts (.TTF)
* Axes Maximums
	* Maximums of different Axes. Used for documentation purposes only. 	


## Variable Font Tool

The following are the current values and glyphs that are controllable within the Variable font preview document. For this initial phase, the following subset of characters have been adapted:

`ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 .,!? - – — _ @ ()`

This selection of characters are labelled as Light Green `glyph.color = 4` in GlyphsApp [markup](https://docu.glyphsapp.com/#GSGlyph.color).

Non-modified but exported glyphs are labelled as Yellow `glyph.color = 3`

## AXES


The axes are split into two categories. [Primary](#primary) being the over-arching axis that affect all characters, and [Secondary](#secondary) which changes specific characters only in a more detailed manner. These are listed under each definition.

### PRIMARY


* **Weighting:** `wght` : 300 — 400

For the purposes of this compilation, the fonts weight has been changed from `380` (Original Google Sans) to `400`.
`400` is the CURRENT weight. `300` is a new lighter weight.

* **X-Height:** `opsz` : 170 — 200

The x-height parameter alters the x-height of the lowercase. Default `170`

* **Spacing:** `ital` <sup>1</sup>  : 100 — 200

`100` is the CURRENT spacing. `200` is the wider, looser setting.


### SECONDARY

* **Character Width:** : `CUS2` : 0 — 100 — 200

Individual character width expansion and contraction to adjust the overall rhythm of the type in body copy.

Default is `0`.

Characters widening: `B E L R S`

Characters narrowing: `C D G O Q e h m n r t u v w y`


* **Ascender** : `CUS3` : 0 — 100

Ascender axis allows the increase in ascender height above the Cap height. Default is `0`.

`b d f h i j k l`

* **Counter**: `CUS4` : 0 — 100

Individual character modifications changing the aperture to an interior counter, and also to the terminal ending itself. Default is `100`. There are two options for expansion from the original GS design. `0` opens up the counter forms, whilst `200` closes them.

Characters changing: `C G J S a c e g s 1 2 3 5 6 7 9 ?` <sup>2</sup>

### TERTIARY TOGGLES

* **Stylistic Set 01**

Enabling `SS01` changes the characters `C G J O Q` to more Grotesque forms. This is controlled (in varying degrees of extremity) by changing the `Character Width` and `Counter` axis.


### Notes

1. The primary axes `SPACING` is set as `ITAL` due to the build script compiling standardised masters initially.
2. The numerals `1 6 7 9` do not animate, and snap-to once past the value `50` in the `CUS4` axes.


## Presets & Recommendations

The following are our initial presets and recommendations from the design process. These are linked to the Preset buttons in the [web viewer](https://colophon-foundry.github.io/variable-web-viewer). The first row is the original Google Sans Regular for point of reference.

### Google Text Options & Recommendations

| Name | Weight | Optical Size | Spacing | Character Width | Ascender | Counter |
| --- | --- | --- | --- | --- | --- | --- |
| **GS Regular** | **400** | **170** | **100** | **0** | **0** | **100** |
| Version 2: Option 1A | 400 | 200 | 100 | 100 | 100 | 200 |
| Version 2: Option 1B | 300 | 200 | 100 | 100 | 100 | 200 |
| Version 2: Option 2A | 400 | 200 | 200 | 100 | 100 | 200 |
| Version 2: Option 2B | 300 | 200 | 200 | 100 | 100 | 200 |
| Version 2: Option 3A | 400 | 190 | 150 | 60 | 100 | 50 |


1. Version **2**: Option **1A** — Spacing and weight as per Google Sans, all other changes pushed to the maximum
2. Version **2**: Option **1B** — Spacing as per Google Sans, all other changes pushed to the maximum
3. Version **2**: Option **2A** — Weight as per Google Sans, all other changes pushed to the maximum
4. Version **2**: Option **2B** — All changes pushed to the maximum
5. Version **2**: Option **3A** — Colophon Foundry’s currently favoured values

These presets are available in the [presets](betas/20190131/Preset%20Instances/) folder.

## Build Process

Unfortunately it is not possible to output the variable font through Glyphs App alone. Although you can see the output as intended in previews and also in static instance generation, the computation of the Deltas by Glyphsapp gives unexpected results. This is due to there being more than 3 axes in the design space.

Output is then needed to be done by [fontmake](https://github.com/googlei18n/fontmake), with the addition of it passing through a bash script (written by Mike LaGattuta) that recompiles all of the brace layers for individual characters. This does take a little while to export, but then generates a single variable TTF. 

``` console
$ cd scripts
$ source buildBrace/build.sh ../source/GoogleSansTextBeta-v2.X
```


**NOTE:** This export is **NOT** perfect. It is missing the `HVAR` information for all brace layers, which will affect the side bearings of any characters in the "Character Width" `CUS2` axes. However this does seem only to affect OSX > 10.12.3 (Mojave etc), as on 10.12.3 the issue is non-existent on the online viewer. Fontview however yields the issue regardless.

Additional note. Due to adding in an option for more open counters, the middle value (For Google Sans Regular) may not yield a like-for-like instance. Debugging shows that this is due to the computation of delta values in the `HVAR` table and incorrect interpolation. More investigation required.

## Build Your Own

It is possible to generate static instances that are more reliable than the variable file. This can be done by using [fontTools](https://github.com/fonttools/fonttools) Mutator function.

``` console
$ cd betas/20190131/Variable
$ fonttools varLib.mutator GoogleSansTextBeta-v2.001.ttf wght=400 opsz=170 ital=100 CUS2=100 CUS3=100 CUS4=100 -o Named-Instance.ttf
```

All parameters must be inside of the range listed in the [Axes](#axes) section. This will also just be output as "Regular" so only one instance (generated via this method) can be installed locally at any one time.*

\* Unless you are able to pass values into the `name` table via the mutator library?