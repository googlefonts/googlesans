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
#  Intermediate source file directory path definitions
# --------------------------------------------------------
INSTANCE_UFO_DIR="instance_ufo"
MASTER_UFO_DIR="master_ufo"

# --------------------------------------------------------
#  TARGETS
# --------------------------------------------------------

gs: gs-static gs-vf

gs-static:
	fontmake -g "$(UPRIGHT_SOURCE)" --interpolate -o ttf --output-dir "$(STATIC_BUILD_DIR)"
	fontmake -g "$(ITALIC_SOURCE)" --interpolate -o ttf --output-dir "$(STATIC_BUILD_DIR)"
	@rm -rf $(INSTANCE_UFO_DIR)
	@rm -rf $(MASTER_UFO_DIR)
	# TODO: add approach to unhinted and hinted build targets

gs-vf:
	fontmake -g "$(UPRIGHT_SOURCE)" -o variable --output-dir "$(VARIABLE_BUILD_DIR)"
	fontmake -g "$(ITALIC_SOURCE)" -o variable --output-dir "$(VARIABLE_BUILD_DIR)"
	@rm -rf $(INSTANCE_UFO_DIR)
	@rm -rf $(MASTER_UFO_DIR)

.PHONY: gs gs-static gs-vf
