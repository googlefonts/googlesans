# Copyright 2020 Google Sans Authors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# --------------------------------------------------------
#  Python 3 virtual environment directory
#    NOTE: This must match the path defined in the root
#          level Makefile
# --------------------------------------------------------
VENV_DIR=.venv

PYTHON3_EXE=python3

# --------------------------------------------------------
#  fontmake compiler executable
# --------------------------------------------------------
FONTMAKE_EXE=FONTTOOLS_GPOS_COMPACT_MODE=5 fontmake --verbose WARNING

# --------------------------------------------------------
#  Source file path definitions
# --------------------------------------------------------
UPRIGHT_SOURCE=GoogleSans/GoogleSans.designspace
ITALIC_SOURCE=GoogleSans/GoogleSans-Italic.designspace

# --------------------------------------------------------
#  Build directory and file path definitions
# --------------------------------------------------------
FONT_BUILD_DIR=../build/GoogleSans
STATIC_BUILD_DIR=$(FONT_BUILD_DIR)/static
VARIABLE_BUILD_DIR=$(FONT_BUILD_DIR)/variable
INTERPOLATABLE_BUILD_DIR=$(FONT_BUILD_DIR)/interpolatable

STAGING_DIR=GoogleSans/staging

# Static font artifact paths
STATIC_TEXT_BUILD_PATH_REGULAR=$(STATIC_BUILD_DIR)/GoogleSansText-Regular.ttf
STATIC_TEXT_BUILD_PATH_ITALIC=$(STATIC_BUILD_DIR)/GoogleSansText-Italic.ttf
STATIC_TEXT_BUILD_PATH_BOLD=$(STATIC_BUILD_DIR)/GoogleSansText-Bold.ttf
STATIC_TEXT_BUILD_PATH_BOLDITALIC=$(STATIC_BUILD_DIR)/GoogleSansText-BoldItalic.ttf
STATIC_TEXT_BUILD_PATH_MEDIUM=$(STATIC_BUILD_DIR)/GoogleSansText-Medium.ttf
STATIC_TEXT_BUILD_PATH_MEDIUMITALIC=$(STATIC_BUILD_DIR)/GoogleSansText-MediumItalic.ttf

STATIC_DISPLAY_BUILD_PATH_REGULAR=$(STATIC_BUILD_DIR)/GoogleSans-Regular.ttf
STATIC_DISPLAY_BUILD_PATH_ITALIC=$(STATIC_BUILD_DIR)/GoogleSans-Italic.ttf
STATIC_DISPLAY_BUILD_PATH_BOLD=$(STATIC_BUILD_DIR)/GoogleSans-Bold.ttf
STATIC_DISPLAY_BUILD_PATH_BOLDITALIC=$(STATIC_BUILD_DIR)/GoogleSans-BoldItalic.ttf
STATIC_DISPLAY_BUILD_PATH_MEDIUM=$(STATIC_BUILD_DIR)/GoogleSans-Medium.ttf
STATIC_DISPLAY_BUILD_PATH_MEDIUMITALIC=$(STATIC_BUILD_DIR)/GoogleSans-MediumItalic.ttf

STATIC_UPRIGHT_BUILD_PATHS = $(STATIC_TEXT_BUILD_PATH_REGULAR) $(STATIC_TEXT_BUILD_PATH_MEDIUM) $(STATIC_TEXT_BUILD_PATH_BOLD) $(STATIC_DISPLAY_BUILD_PATH_REGULAR) $(STATIC_DISPLAY_BUILD_PATH_MEDIUM) $(STATIC_DISPLAY_BUILD_PATH_BOLD)
STATIC_ITALIC_BUILD_PATHS = $(STATIC_TEXT_BUILD_PATH_ITALIC) $(STATIC_TEXT_BUILD_PATH_MEDIUMITALIC) $(STATIC_TEXT_BUILD_PATH_BOLDITALIC) $(STATIC_DISPLAY_BUILD_PATH_ITALIC) $(STATIC_DISPLAY_BUILD_PATH_MEDIUMITALIC) $(STATIC_DISPLAY_BUILD_PATH_BOLDITALIC)

# Variable font artifact paths

# Roman
VARIABLE_BUILD_PATH_UPRIGHT=$(VARIABLE_BUILD_DIR)/GoogleSans-VF.ttf
VARIABLE_BUILD_PATH_UPRIGHT_TARGET=$(VARIABLE_BUILD_DIR)/GoogleSans[GRAD,opsz,wght].ttf

# Italic
VARIABLE_BUILD_PATH_ITALIC=$(VARIABLE_BUILD_DIR)/GoogleSans-Italic-VF.ttf
VARIABLE_BUILD_PATH_ITALIC_TARGET=$(VARIABLE_BUILD_DIR)/GoogleSans-Italic[GRAD,opsz,wght].ttf

# --------------------------------------------------------
#  UFO intermediates and designspace paths
# --------------------------------------------------------
INSTANCE_UFO_DIR=$(FONT_BUILD_DIR)/instance_ufo

# --------------------------------------------------------
#  Master and instance intermediate UFO file paths
# --------------------------------------------------------
UFO_GS_REGULAR=GoogleSans/GoogleSans-Regular.ufo
UFO_GS_ITALIC=GoogleSans/GoogleSans-Italic.ufo
UFO_GS_MEDIUM=$(INSTANCE_UFO_DIR)/GoogleSans-Medium.ufo
UFO_GS_MEDIUMITALIC=$(INSTANCE_UFO_DIR)/GoogleSans-MediumItalic.ufo
UFO_GS_BOLD=GoogleSans/GoogleSans-Bold.ufo
UFO_GS_BOLDITALIC=GoogleSans/GoogleSans-BoldItalic.ufo

UFO_GS_TEXT_REGULAR=GoogleSans/GoogleSans-TextRegular.ufo
UFO_GS_TEXT_ITALIC=GoogleSans/GoogleSans-TextItalic.ufo
UFO_GS_TEXT_MEDIUM=$(INSTANCE_UFO_DIR)/GoogleSans-TextMedium.ufo
UFO_GS_TEXT_MEDIUMITALIC=$(INSTANCE_UFO_DIR)/GoogleSans-TextMediumItalic.ufo
UFO_GS_TEXT_BOLD=GoogleSans/GoogleSans-TextBold.ufo
UFO_GS_TEXT_BOLDITALIC=GoogleSans/GoogleSans-TextBoldItalic.ufo

# --------------------------------------------------------
#  TARGETS
# --------------------------------------------------------

#
# Full font family build targets
#

gs-static: gs-static-upright gs-static-italic

gs-static-upright: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -m $(UPRIGHT_SOURCE) --interpolate -o ttf --output-dir $(STATIC_BUILD_DIR) --expand-features-to-instances
	$(PYTHON3_EXE) ../scripts/gs-subset.py $(STATIC_UPRIGHT_BUILD_PATHS)
	$(PYTHON3_EXE) ../scripts/set-unicoderange.py $(STATIC_UPRIGHT_BUILD_PATHS)
	$(PYTHON3_EXE) ../scripts/gftools-fix-nonhinting.py $(STATIC_UPRIGHT_BUILD_PATHS)
	font-v write --sha1 $(STATIC_UPRIGHT_BUILD_PATHS)

gs-static-italic: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -m $(ITALIC_SOURCE) --interpolate -o ttf --output-dir $(STATIC_BUILD_DIR) --expand-features-to-instances
	$(PYTHON3_EXE) ../scripts/gs-subset.py $(STATIC_ITALIC_BUILD_PATHS)
	$(PYTHON3_EXE) ../scripts/set-unicoderange.py $(STATIC_ITALIC_BUILD_PATHS)
	$(PYTHON3_EXE) ../scripts/gftools-fix-nonhinting.py $(STATIC_ITALIC_BUILD_PATHS)
	font-v write --sha1 $(STATIC_ITALIC_BUILD_PATHS)

gs-vf: gs-vf-upright gs-vf-italic

VARIABLE_BUILD_PATH_UPRIGHT_TARGET: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -m $(UPRIGHT_SOURCE) -o variable --output-dir $(VARIABLE_BUILD_DIR)
	$(PYTHON3_EXE) ../scripts/gs-subset.py $(VARIABLE_BUILD_PATH_UPRIGHT)
	$(PYTHON3_EXE) ../scripts/internal/set-overlap-bits.py $(VARIABLE_BUILD_PATH_UPRIGHT)
	$(PYTHON3_EXE) ../scripts/set-unicoderange.py $(VARIABLE_BUILD_PATH_UPRIGHT)
	$(PYTHON3_EXE) ../scripts/gftools-fix-unwanted-tables.py --tables MVAR $(VARIABLE_BUILD_PATH_UPRIGHT)
	$(PYTHON3_EXE) ../scripts/gftools-fix-nonhinting.py $(VARIABLE_BUILD_PATH_UPRIGHT)
	$(PYTHON3_EXE) ../scripts/gs-stat.py $(VARIABLE_BUILD_PATH_UPRIGHT)
	font-v write --sha1 $(VARIABLE_BUILD_PATH_UPRIGHT)
	mv $(VARIABLE_BUILD_PATH_UPRIGHT) "$(VARIABLE_BUILD_PATH_UPRIGHT_TARGET)"

VARIABLE_BUILD_PATH_ITALIC_TARGET: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -m $(ITALIC_SOURCE) -o variable --output-dir $(VARIABLE_BUILD_DIR)
	$(PYTHON3_EXE) ../scripts/gs-subset.py $(VARIABLE_BUILD_PATH_ITALIC)
	$(PYTHON3_EXE) ../scripts/internal/set-overlap-bits.py $(VARIABLE_BUILD_PATH_ITALIC)
	$(PYTHON3_EXE) ../scripts/set-unicoderange.py $(VARIABLE_BUILD_PATH_ITALIC)
	$(PYTHON3_EXE) ../scripts/gftools-fix-unwanted-tables.py --tables MVAR $(VARIABLE_BUILD_PATH_ITALIC)
	$(PYTHON3_EXE) ../scripts/gftools-fix-nonhinting.py $(VARIABLE_BUILD_PATH_ITALIC)
	$(PYTHON3_EXE) ../scripts/gs-stat.py $(VARIABLE_BUILD_PATH_ITALIC)
	font-v write --sha1 $(VARIABLE_BUILD_PATH_ITALIC)
	mv $(VARIABLE_BUILD_PATH_ITALIC) "$(VARIABLE_BUILD_PATH_ITALIC_TARGET)"

gs-compatible-masters: gs-compatible-masters-upright gs-compatible-masters-italic

gs-compatible-masters-upright: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) --no-production-names -m $(UPRIGHT_SOURCE) -o ttf-interpolatable --output-dir $(INTERPOLATABLE_BUILD_DIR)

gs-compatible-masters-italic: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) --no-production-names -m $(ITALIC_SOURCE) -o ttf-interpolatable --output-dir $(INTERPOLATABLE_BUILD_DIR)

gs-vf-vendor: gs-vf-vendor-glyphs2designspace
	$(foreach \
		file, \
		$(wildcard $(STAGING_DIR)/*.designspace), \
		fontmake -m $(file) -o variable --output-dir $(STAGING_DIR); \
	)

gs-vf-vendor-glyphs2designspace: $(STAGING_DIR) $(wildcard GoogleSans/*.glyphs)
	python ../scripts/gs-glyphs2ufo.py GoogleSans/*.glyphs --target-dir GoogleSans/staging

gs-ufo2glyphs: $(wildcard GoogleSans/*.designspace)
	$(foreach \
		file, \
		$(wildcard GoogleSans/*.designspace), \
		python ../scripts/gs-ufo2glyphs.py $(file); \
	)

#
#  Individual static instance build targets
#

# Google Sans (max optical size)
gs-regular: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -u $(UFO_GS_REGULAR) -o ttf --output-dir $(STATIC_BUILD_DIR)

gs-italic: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -u $(UFO_GS_ITALIC) -o ttf --output-dir $(STATIC_BUILD_DIR)

gs-medium: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -m $(UPRIGHT_SOURCE) -i "Google Sans Medium" -o ufo
	$(FONTMAKE_EXE) -u $(UFO_GS_MEDIUM) -o ttf --output-dir $(STATIC_BUILD_DIR)

gs-medium-italic: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -m $(ITALIC_SOURCE) -i "Google Sans Medium Italic" -o ufo
	$(FONTMAKE_EXE) -u $(UFO_GS_MEDIUMITALIC) -o ttf --output-dir $(STATIC_BUILD_DIR)

gs-bold: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -u $(UFO_GS_BOLD) -o ttf --output-dir $(STATIC_BUILD_DIR)

gs-bold-italic: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -u $(UFO_GS_BOLDITALIC) -o ttf --output-dir $(STATIC_BUILD_DIR)

# Google Sans Text (min optical size)
gst-regular: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -u $(UFO_GS_TEXT_REGULAR) -o ttf --output-dir $(STATIC_BUILD_DIR)

gst-italic: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -u $(UFO_GS_TEXT_ITALIC) -o ttf --output-dir $(STATIC_BUILD_DIR)

gst-medium: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -m $(UPRIGHT_SOURCE) -i "Google Sans Text Medium" -o ufo
	$(FONTMAKE_EXE) -u $(UFO_GS_TEXT_MEDIUM) -o ttf --output-dir $(STATIC_BUILD_DIR)

gst-medium-italic: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -m $(ITALIC_SOURCE) -i "Google Sans Text Medium Italic" -o ufo
	$(FONTMAKE_EXE) -u $(UFO_GS_TEXT_MEDIUMITALIC) -o ttf --output-dir $(STATIC_BUILD_DIR)

gst-bold: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -u $(UFO_GS_TEXT_BOLD) -o ttf --output-dir $(STATIC_BUILD_DIR)

gst-bold-italic: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -u $(UFO_GS_TEXT_BOLDITALIC) -o ttf --output-dir $(STATIC_BUILD_DIR)

#
# Individual variable font build targets
#

gs-vf-upright: VARIABLE_BUILD_PATH_UPRIGHT_TARGET

gs-vf-italic: VARIABLE_BUILD_PATH_ITALIC_TARGET

#
# Utilities
#
$(FONT_BUILD_DIR):
	mkdir -p $(FONT_BUILD_DIR)
	mkdir -p $(STATIC_BUILD_DIR)
	mkdir -p $(VARIABLE_BUILD_DIR)
	mkdir -p $(INTERPOLATABLE_BUILD_DIR)

$(STAGING_DIR):
	mkdir -p $(STAGING_DIR)

.PHONY: gs-static gs-vf \
gs-regular gs-italic gs-medium gs-medium-italic gs-bold gs-bold-italic \
gst-regular gst-italic gst-medium gst-medium-italic gst-bold gst-bold-italic \
gs-vf-upright gs-vf-italic gs-ufo2glyphs gs-compatible-masters \
gs-compatible-masters-upright gs-compatible-masters-italic

# Disable built-in rules to speed up source globbing.
MAKEFLAGS += --no-builtin-rules
.SUFFIXES:
