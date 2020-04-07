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

## TODO: Edd, Irene, Alexei

### `aalt`

### `ccmp`

### `locl`

**Cyrillic**
List of localized forms

- Bashkir:
```
Ғ 0x0492 Ghestroke-cy 
ғ 0x0493 ghestroke-cy 
Ҙ 0x0498 Zedescender-cy 
ҙ 0x0499 zedescender-cy
Ҫ 0x04AA Esdescender-cy
ҫ 0x04AB esdescender-cy
```

- Chuvash:
```
Ҫ 0x04AA Esdescender-cy
ҫ 0x04AB esdescender-cy
```

- Bulgarian:
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

* Serbian and Macedonian (Upright): 
```
б 0x0431 be-cy
```

* Serbian (Italic):
```
б 0x0431 be-cy
г 0x0433 ge-cy
ѓ 0x0433 gje-cy
д 0x0434 de-cy
п 0x043F pe-cy
т 0x0442 te-cy
ш 0x0448 sha-cy

```

* Macedonian (Italic):
```
г 0x0433 ge-cy
ѓ 0x0433 gje-cy
д 0x0434 de-cy
п 0x043F pe-cy
т 0x0442 te-cy
ш 0x0448 sha-cy
```

### `frac`

### `numr`

### `dnom`

### `lnum`

### `tnum`

### `ordn`

### `case`

### `sups`

### `subs`

### `sinf`

### `pnum`

### `c2sc`

### `smcp`

### `dlig`

### `calt`

**Greek**

- Retain accent (tonos) in `ή` (disjunctive eta) in small caps transformation.

## Stylistic Sets

### `ss01`

### `ss02`

### `ss03`

### `ss04`

### `ss05`

### `ss06`

**Greek**

- Accented Greek SC: keep all the accents in small caps transformation

### `ss07`

**Greek**

- iota adscript: transform `subscript iota` to `adscript iota`

### `ss08`

-Bulgarian Locale

Includes Bulgarian localized variants for the following glyphs:
`ДЛФ` (and their respective Small Caps), `вгджзийѝклптфцшщьъыю`. May be useful for applications that do not support `locl` OpenType feature.
