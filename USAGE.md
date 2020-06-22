# How to Use Google Sans

## Standard ligatures (On by default)

### Google logo ligatures

Google logo ligatures are available through the `liga` feature. These are available in both contextual and PUA encoded flavours.

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

## Other OpenType features

### [`aalt`](https://docs.microsoft.com/en-us/typography/opentype/spec/features_ae#tag-aalt)

Expert build target alternate outline form support. Supports access to glyph outlines defined as `*.alt` in the source files.

### [`calt`](https://docs.microsoft.com/en-us/typography/opentype/spec/features_ae#tag-calt)

Support for contextual alternates.

Special use cases of the calt feature:

#### Latin

- Google logo as `[Gg]oogle_logo` sequence
- Google super G as `google_G_logo` sequence

#### Greek

- Retain accent (tonos) in `ή` (disjunctive eta) in small caps transformation.

### [`case`](https://docs.microsoft.com/en-us/typography/opentype/spec/features_ae#tag-case)

Supports substitution of upper case sequence forms.

### [`ccmp`](https://docs.microsoft.com/en-us/typography/opentype/spec/features_ae#tag-ccmp)

Special handling of glyph decomposition and composition.

### [`c2sc`](https://docs.microsoft.com/en-us/typography/opentype/spec/features_ae#tag-c2sc)

Capitals to small caps support.

### [`dlig`](https://docs.microsoft.com/en-us/typography/opentype/spec/features_ae#tag-dlig)

Discretionary ligature support.

### [`dnom`](https://docs.microsoft.com/en-us/typography/opentype/spec/features_ae#tag-dnom)

Denominator figure outlines.

### [`frac`](https://docs.microsoft.com/en-us/typography/opentype/spec/features_fj#tag-frac)

Support for fraction presentation of figures separated by a slash pattern.

### [`lnum`](https://docs.microsoft.com/en-us/typography/opentype/spec/features_ko#tag-lnum)

Support for non-lininig figure to lining figure transformations.

### [`locl`](https://docs.microsoft.com/en-us/typography/opentype/spec/features_ko#tag-locl)

Support for localized writing system glyph forms.

#### Cyrillic

List of localized forms

##### Bashkir:

```
Ғ 0x0492 Ghestroke-cy
ғ 0x0493 ghestroke-cy
Ҙ 0x0498 Zedescender-cy
ҙ 0x0499 zedescender-cy
Ҫ 0x04AA Esdescender-cy
ҫ 0x04AB esdescender-cy
```

##### Bulgarian:

```
Д 0x0414 De-cy
Л 0x041B El-cy
Ф 0x0424 Ef-cy
в 0x0432 ve-cy
г 0x0433 ge-cy
д 0x0434 de-cy
ж 0x0436 zhe-cy
з 0x0437 ze-cy
и 0x0438 ii-cy
й 0x0439 iishort-cy
ѝ 0x045D iigrave-cy
к 0x043A ka-cy
л 0x043B el-cy
п 0x043F pe-cy
т 0x0442 te-cy
ф 0x0444 ef-cy
ц 0x0446 tse-cy
ш 0x0448 sha-cy
щ 0x0449 shcha-cy
ь 0x044C softsign-cy
ъ 0x044A hardsign-cy
ы 0x044B yeru-cy
ю 0x044E iu-cy
```

##### Chuvash:

```
Ҫ 0x04AA Esdescender-cy
ҫ 0x04AB esdescender-cy
```

##### Macedonian (Italic):

```
г 0x0433 ge-cy
ѓ 0x0433 gje-cy
д 0x0434 de-cy
п 0x043F pe-cy
т 0x0442 te-cy
ш 0x0448 sha-cy
```

##### Serbian and Macedonian (Upright):

```
б 0x0431 be-cy
```

##### Serbian (Italic):

```
б 0x0431 be-cy
г 0x0433 ge-cy
ѓ 0x0433 gje-cy
д 0x0434 de-cy
п 0x043F pe-cy
т 0x0442 te-cy
ш 0x0448 sha-cy
```

### [`numr`](https://docs.microsoft.com/en-us/typography/opentype/spec/features_ko#tag-numr)

Numerator figure outlines.

### [`ordn`](https://docs.microsoft.com/en-us/typography/opentype/spec/features_ko#tag-ordn)

Support for replacement of default alphabetic glyphs with their ordinal form after figures.

### [`pnum`](https://docs.microsoft.com/en-us/typography/opentype/spec/features_pt#-tag-pnum)

Proportional figure support.

### [`sinf`](https://docs.microsoft.com/en-us/typography/opentype/spec/features_pt#-tag-sinf)

Scientific inferior support.

### [`smcp`](https://docs.microsoft.com/en-us/typography/opentype/spec/features_pt#-tag-smcp)

Small caps support.

### [`subs`](https://docs.microsoft.com/en-us/typography/opentype/spec/features_pt#-tag-subs)

Subscript support.

### [`sups`](https://docs.microsoft.com/en-us/typography/opentype/spec/features_pt#-tag-sups)

Superscript support.

### [`tnum`](https://docs.microsoft.com/en-us/typography/opentype/spec/features_pt#-tag-tnum)

Support for tabular (monospaced) figures. Default figures are proportional width.

## Stylistic Sets

### `ss01`

- Number pad asterisk

### `ss02`

- Colon design for use in time displays

### `ss03`

- Thin numbers

### `ss04`

- Micro caps designs. These are the pre-v3.000 release "small caps" designs and are maintained for backward compatibility

### `ss05`

- Alternate arrows

### `ss06`

- Accented Greek small caps

#### Greek

- Accented Greek SC: keep all the accents in small caps transformation

### `ss07`

#### Greek

- iota adscript: transform `subscript iota` to `adscript iota`

### `ss08`

#### Bulgarian Locale

- Includes Bulgarian localized variants for the following glyphs:
  `ДЛФ` (and their respective Small Caps), `вгджзийѝклптфцшщьъыю`. May be useful for applications that do not support `locl` OpenType feature.
