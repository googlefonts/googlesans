# --------------------------------------------------------
#  Source file path definitions
# --------------------------------------------------------
UPRIGHT_SOURCE="GoogleSans-Text/GoogleSansText-Beta.glyphs"
ITALIC_SOURCE="GoogleSans-Text/GoogleSansText-Italic-Beta.glyphs"

# --------------------------------------------------------
#  Build directory path definitions
# --------------------------------------------------------
FONT_BUILD_DIR="../build/GoogleSans"
STATIC_BUILD_DIR="$(FONT_BUILD_DIR)/static"
VARIABLE_BUILD_DIR="$(FONT_BUILD_DIR)/variable"

# --------------------------------------------------------
#  UFO intermediates and designspace paths
# --------------------------------------------------------
MASTER_UFO_DIR="$(FONT_BUILD_DIR)/master_ufo"
INSTANCE_UFO_DIR="$(FONT_BUILD_DIR)/instance_ufo"

UPRIGHT_DESIGNSPACE="GoogleSansBeta-GoogleSans.designspace"
ITALIC_DESIGNSPACE="GoogleSansBeta-GoogleSansItalic.designspace"
UPRIGHT_DESIGNSPACE_PATH="$(MASTER_UFO_DIR)/$(UPRIGHT_DESIGNSPACE)"
ITALIC_DESIGNSPACE_PATH="$(MASTER_UFO_DIR)/$(ITALIC_DESIGNSPACE)"

# --------------------------------------------------------
#  Master and instance intermediate UFO file paths
# --------------------------------------------------------
UFO_GS_REGULAR="$(MASTER_UFO_DIR)/GoogleSansBeta-GoogleSansRegular.ufo"
UFO_GS_ITALIC="$(MASTER_UFO_DIR)/GoogleSansBeta-GoogleSansItalic.ufo"
UFO_GS_MEDIUM="$(INSTANCE_UFO_DIR)/GoogleSansBeta-Medium.ufo"
UFO_GS_MEDIUMITALIC="$(INSTANCE_UFO_DIR)/GoogleSansBeta-MediumItalic.ufo"
UFO_GS_BOLD="$(MASTER_UFO_DIR)/GoogleSansBeta-GoogleSansBold.ufo"
UFO_GS_BOLDITALIC="$(MASTER_UFO_DIR)/GoogleSansBeta-GoogleSansBoldItalic.ufo"

UFO_GS_TEXT_REGULAR="$(MASTER_UFO_DIR)/GoogleSansBeta-GoogleSansTextRegular.ufo"
UFO_GS_TEXT_ITALIC="$(MASTER_UFO_DIR)/GoogleSansBeta-GoogleSansTextItalic.ufo"
UFO_GS_TEXT_MEDIUM="$(INSTANCE_UFO_DIR)/GoogleSansBeta-TextMedium.ufo"
UFO_GS_TEXT_MEDIUMITALIC="$(INSTANCE_UFO_DIR)/GoogleSansBeta-TextMediumItalic.ufo"
UFO_GS_TEXT_BOLD="$(MASTER_UFO_DIR)/GoogleSansBeta-GoogleSansTextBold.ufo"
UFO_GS_TEXT_BOLDITALIC="$(MASTER_UFO_DIR)/GoogleSansBeta-GoogleSansTextBoldItalic.ufo"

# --------------------------------------------------------
#  TARGETS
# --------------------------------------------------------

#
# Full font family build targets
#

# TODO: add approach to unhinted and hinted build targets
gs-static:
	fontmake -g $(UPRIGHT_SOURCE) --interpolate -o ttf --output-dir $(STATIC_BUILD_DIR) --master-dir $(MASTER_UFO_DIR) --instance-dir $(INSTANCE_UFO_DIR)
	fontmake -g $(ITALIC_SOURCE) --interpolate -o ttf --output-dir $(STATIC_BUILD_DIR) --master-dir $(MASTER_UFO_DIR) --instance-dir $(INSTANCE_UFO_DIR)
	

gs-vf:
	fontmake -g $(UPRIGHT_SOURCE) -o variable --output-dir $(VARIABLE_BUILD_DIR) --master-dir $(MASTER_UFO_DIR) --instance-dir $(INSTANCE_UFO_DIR)
	fontmake -g $(ITALIC_SOURCE) -o variable --output-dir $(VARIABLE_BUILD_DIR) --master-dir $(MASTER_UFO_DIR) --instance-dir $(INSTANCE_UFO_DIR)


#
#  Individual static instance build targets
#

# Google Sans (max optical size)
gs-regular: build-designspace-upright
	fontmake -u $(UFO_GS_REGULAR) -o ttf --output-dir $(STATIC_BUILD_DIR)

gs-italic: build-designspace-italic
	fontmake -u $(UFO_GS_ITALIC) -o ttf --output-dir $(STATIC_BUILD_DIR)

gs-medium: build-designspace-upright
	fontmake -m $(UPRIGHT_DESIGNSPACE_PATH) -i "Google Sans Beta Medium" -o ufo
	fontmake -u $(UFO_GS_MEDIUM) -o ttf --output-dir $(STATIC_BUILD_DIR)

gs-medium-italic: build-designspace-italic
	fontmake -m $(ITALIC_DESIGNSPACE_PATH) -i "Google Sans Beta Medium Italic" -o ufo
	fontmake -u $(UFO_GS_MEDIUMITALIC) -o ttf --output-dir $(STATIC_BUILD_DIR)

gs-bold: build-designspace-upright
	fontmake -u $(UFO_GS_BOLD) -o ttf --output-dir $(STATIC_BUILD_DIR)

gs-bold-italic: build-designspace-italic
	fontmake -u $(UFO_GS_BOLDITALIC) -o ttf --output-dir $(STATIC_BUILD_DIR)

# Google Sans Text (min optical size)
gst-regular: build-designspace-upright
	fontmake -u $(UFO_GS_TEXT_REGULAR) -o ttf --output-dir $(STATIC_BUILD_DIR)

gst-italic: build-designspace-italic
	fontmake -u $(UFO_GS_TEXT_ITALIC) -o ttf --output-dir $(STATIC_BUILD_DIR)

gst-medium: build-designspace-upright
	fontmake -m $(UPRIGHT_DESIGNSPACE_PATH) -i "Google Sans Beta Text Medium" -o ufo
	fontmake -u $(UFO_GS_TEXT_MEDIUM) -o ttf --output-dir $(STATIC_BUILD_DIR)

gst-medium-italic: build-designspace-italic
	fontmake -m $(ITALIC_DESIGNSPACE_PATH) -i "Google Sans Beta Text Medium Italic" -o ufo
	fontmake -u $(UFO_GS_TEXT_MEDIUMITALIC) -o ttf --output-dir $(STATIC_BUILD_DIR)

gst-bold: build-designspace-upright
	fontmake -u $(UFO_GS_TEXT_BOLD) -o ttf --output-dir $(STATIC_BUILD_DIR)

gst-bold-italic: build-designspace-italic
	fontmake -u $(UFO_GS_TEXT_BOLDITALIC) -o ttf --output-dir $(STATIC_BUILD_DIR)

#
# Individual variable font build targets
#

gs-vf-upright:
	fontmake -g $(UPRIGHT_SOURCE) -o variable --output-dir $(VARIABLE_BUILD_DIR) --master-dir $(MASTER_UFO_DIR) --instance-dir $(INSTANCE_UFO_DIR)

gs-vf-italic:
	fontmake -g $(ITALIC_SOURCE) -o variable --output-dir $(VARIABLE_BUILD_DIR) --master-dir $(MASTER_UFO_DIR) --instance-dir $(INSTANCE_UFO_DIR)

#
#  Design space build targets
#

build-designspace-upright: 
	fontmake -g $(UPRIGHT_SOURCE) -o ufo --master-dir $(MASTER_UFO_DIR) --instance-dir $(INSTANCE_UFO_DIR)


build-designspace-italic: 
	fontmake -g $(ITALIC_SOURCE) -o ufo --master-dir $(MASTER_UFO_DIR) --instance-dir $(INSTANCE_UFO_DIR)


.PHONY: gs-static gs-vf \
gs-regular gs-italic gs-medium gs-medium-italic gs-bold gs-bold-italic \
gst-regular gst-italic gst-medium gst-medium-italic gst-bold gst-bold-italic \
gs-vf-upright gs-vf-italic \
build-designspace-upright build-designspace-italic
