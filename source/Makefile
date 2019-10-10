gs: gs-static gs-vf

gs-static:
	fontmake -g source/GoogleSans-Text/GoogleSansText-Beta.glyphs --interpolate -o ttf
	fontmake -g source/GoogleSans-Text/GoogleSansText-Italic-Beta.glyphs --interpolate -o ttf
	# TODO: add approach to unhinted and hinted build targets

gs-vf:
	fontmake -g source/GoogleSans-Text/GoogleSansText-Beta.glyphs -o variable
    fontmake -g source/GoogleSans-Text/GoogleSansText-Italic-Beta.glyphs -o variable

.PHONY: gs gs-static gs-vf
