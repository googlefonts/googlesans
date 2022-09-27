from ufoLib2 import Font

# from fontTools.unicodedata import script
# from ufo2ft.featureCompiler import parseLayoutFeatures
# from ufo2ft.util import (
#     classifyGlyphs,
#     makeOfficialGlyphOrder,
#     compileGSUB,
#     makeUnicodeToGlyphNameMapping,
# )

font = Font.open("source/GoogleSans/GoogleSans-opsz18-wght380-GRAD0.ufo")

smallcaps = set(g.name for g in font if g.name is not None and ".sc" in g.name)

combining = set(g.name for g in font if g.name is not None and "comb" in g.name)
print("Combining small caps:")
print("\n".join(sorted(smallcaps & combining)))
print()

# glyph_order = makeOfficialGlyphOrder(font)
# cmap = makeUnicodeToGlyphNameMapping(font, glyph_order)
# feature_file = parseLayoutFeatures(font)
# gsub = compileGSUB(feature_file, glyph_order)
# glyphs_by_script = classifyGlyphs(script, cmap, gsub)
# greek = set(glyphs_by_script["Grek"])
# print("Greek small caps:")
# print("\n".join(sorted(smallcaps & greek)))
# print()

print("Other small caps:")
print(" ".join(sorted(smallcaps - combining)))
