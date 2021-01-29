# Google Sans Style Guidelines

This document details the source style guidelines for the Google Sans project.

## Contents

- [Definitions](#definitions)
- [Style](#style)
- [Examples](#examples)

## Definitions

### Script Tags

"Script tags" in this document refer to the script tag strings defined in [OpenType Script Tags](https://docs.microsoft.com/en-us/typography/opentype/spec/scripttags).

### Language Tags

"Language tags" in this document refer to the language tag strings defined in [OpenType Language System Tags](https://docs.microsoft.com/en-us/typography/opentype/spec/languagetags).

## Style

### Names

#### Glyph names

- Name all glyphs according to the naming standard used by the Glyphs.app GlyphData.xml database
- Use underscores to separate glyph names in ligature glyph forms
- Name localized glyph forms with the glyph name, a period, the string `locl`, followed by an all caps localized language tag suffix
- In scripts that support upper case forms, please use title case glyph names for upper case glyph forms
- Please do not change glyph names after they have been imported into the upstream source files

#### OpenType class names

- OpenType class naming should use the following format:
  - A_B_C_D
    - A - Context-dependent script system tag (only for Non-Latin scripts)
    - B - Context-dependent language system tag
    - C - Context-dependent feature tag
    - D - Class description string
- When a class is used by several scripts, list all scripts in the name
- When a class is used by several languages, list all languages in the name
- When a class is used in several features, list all feature tags in its name
- Except if listing everything is too cumbersome and counterproductive, then drop that part of name but leave a comment instead, just above the class definition, to explain which scripts/languages/features are concerned

#### Kerning group names

- All names should be lowercase, separated by underscores, except for the string that refers to glyph names. E.g. `Omega` should stay as is if it refers to the upper case glyph name
- Kerning groups should contain the name of the script they pertain to. This avoids name clashes. The format is script_key_glyph_or_description

#### Adobe feature code lookup names

- Adobe feature code lookup names should use the following format:

- A_B_C_D
  - A - Context-dependent Script system tag - only for Non-Latin scripts
  - B - Context-dependent language system tag
  - C - Feature tag
  - D - Lookup description string
- When a lookup is used by several scripts, list all scripts in the name
- When a lookup is used by several languages, list all languages in the name
- When a lookup is used in several features, list all feature tags in its name
- Except if listing everything is too cumbersome and counterproductive, then drop that part of name but leave a comment instead, just above the lookup definition, to explain which scripts/languages/features are concerned

### Adobe feature file source

- feature blocks and lookups should be declared separately
- lookups should have descriptive names and include, where appropriate, the language and feature tag where they are used. Example: `nld_locl_ij_substitution` for a Netherlandish lookup that replaces `i' j'` by `ij`
- Use four space indentation for source contained in `{` and `}` delimiters
- do not include empty lines between the opening `{` delimiter and the first line of contained source
- do not include empty lines between the final line of contained source and the closing `}` delimiter

## Examples

### Glyph name examples

- `amacron`: lower case form has lower case name
- `Amacron`: upper case form has title case name
- `f_f_i`: a `ffi` ligature
- `Ef-cy.loclBGR`: a localized form uses the string `locl` followed by an all caps language tag

### OpenType class name examples

- C: `pnum`
- C_D: `pnum_currencies`
- C_D: `frac_precomposed`
- A_B_C: `cyrl_bgr_locl`
- A_C_D_D: `grek_calt_marks_context`

### Kerning group name examples

- `grek_Omega`
- `thai_phoSamphao`
- `armn_uc_topround_bottomstraight`

### Adobe feature code lookup name examples

- B_C_D_D: `rom_locl_cedilla_substitution`
- A_C_D_D: `grek_ccmp_recompose_dieresistonos`
- A_B_C_D: `cyrl_bgr_locl_alternates`
- C_D: `frac_precomposed`
  
### Adobe feature file examples

```fea
languagesystem DFLT dflt;
languagesystem latn dflt;
languagesystem latn NLD;

@pnum_fig_dflt = [zero one two three four five six seven eight nine];
@pnum_fig_alt = [zero.alt one.alt two.alt three.alt four.alt five.alt six.alt seven.alt eight.alt nine.alt];

lookup pnum_text {
    sub @fig_dflt by @fig_alt;
} pnum_text;

lookup nld_locl_ij_substitution {
    sub i' j' by ij;
    sub I' J' by IJ;
} nld_locl_ij_substitution;

feature pnum {
    lookup pnum_text;
} pnum;

feature locl {
    script latn;
    language NLD;
    lookup nld_locl_ij_substitution;
} locl;
```
