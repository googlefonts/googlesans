# --------------------------------------------------------
#  Source file path definitions
# --------------------------------------------------------
UPRIGHT_SOURCE="GoogleSans-Text/GoogleSansText-Beta.glyphs"
ITALIC_SOURCE="GoogleSans-Text/GoogleSansText-Italic-Beta.glyphs"

# --------------------------------------------------------
#  Build directory path definitions
# --------------------------------------------------------
BUILD_DIR="../build/GoogleSans"
STATIC_BUILD_DIR="$(BUILD_DIR)/static"
VARIABLE_BUILD_DIR="$(BUILD_DIR)/variable"

# --------------------------------------------------------
#  TARGETS
# --------------------------------------------------------

gs: gs-static gs-vf

gs-static:
	fontmake -g "$(UPRIGHT_SOURCE)" --interpolate -o ttf --output-dir "$(STATIC_BUILD_DIR)" --master-dir {tmp} --instance-dir {tmp}
	fontmake -g "$(ITALIC_SOURCE)" --interpolate -o ttf --output-dir "$(STATIC_BUILD_DIR)" --master-dir {tmp} --instance-dir {tmp}
	# TODO: add approach to unhinted and hinted build targets

gs-vf:
	fontmake -g "$(UPRIGHT_SOURCE)" -o variable --output-dir "$(VARIABLE_BUILD_DIR)" --master-dir {tmp} --instance-dir {tmp}
	fontmake -g "$(ITALIC_SOURCE)" -o variable --output-dir "$(VARIABLE_BUILD_DIR)" --master-dir {tmp} --instance-dir {tmp}

.PHONY: gs gs-static gs-vf
