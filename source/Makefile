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
#    NOTE: this builds from a venv install to support
#          pinned dependency versions
# --------------------------------------------------------
FONTMAKE_EXE=fontmake

# --------------------------------------------------------
#  Source file path definitions
# --------------------------------------------------------
UPRIGHT_SOURCE=GoogleSans/GoogleSans.designspace
ITALIC_SOURCE=GoogleSans/GoogleSans-Italic.designspace

# --------------------------------------------------------
#  Build directory and file path definitions
# --------------------------------------------------------
FONT_BUILD_DIR=../build/GoogleSans
EXPERT_STATIC_BUILD_DIR=$(FONT_BUILD_DIR)/static/expert
DEFAULT_STATIC_BUILD_DIR=$(FONT_BUILD_DIR)/static/default
EXPERT_VARIABLE_BUILD_DIR=$(FONT_BUILD_DIR)/variable/expert
DEFAULT_VARIABLE_BUILD_DIR=$(FONT_BUILD_DIR)/variable/default

PARTIAL_INSTANCE_VARIABLE_BUILD_DIR=$(EXPERT_VARIABLE_BUILD_DIR)/partial

STAGING_DIR=GoogleSans/staging

# Static font expert Text opsz build artifacts
#  - these paths are necessary for post compile path
#    edits vs. what comes out of the compiler
STATIC_TEXT_BUILD_PATH_REGULAR=$(EXPERT_STATIC_BUILD_DIR)/GoogleSansText-Regular.ttf
STATIC_TEXT_BUILD_PATH_ITALIC=$(EXPERT_STATIC_BUILD_DIR)/GoogleSansText-Italic.ttf
STATIC_TEXT_BUILD_PATH_BOLD=$(EXPERT_STATIC_BUILD_DIR)/GoogleSansText-Bold.ttf
STATIC_TEXT_BUILD_PATH_BOLDITALIC=$(EXPERT_STATIC_BUILD_DIR)/GoogleSansText-BoldItalic.ttf
STATIC_TEXT_BUILD_PATH_MEDIUM=$(EXPERT_STATIC_BUILD_DIR)/GoogleSansText-Medium.ttf
STATIC_TEXT_BUILD_PATH_MEDIUMITALIC=$(EXPERT_STATIC_BUILD_DIR)/GoogleSansText-MediumItalic.ttf

# Variable font build artifacts

# upright
VARIABLE_BUILD_PATH_UPRIGHT=$(EXPERT_VARIABLE_BUILD_DIR)/GoogleSans-VF.ttf
VARIABLE_BUILD_PATH_UPRIGHT_TARGET=$(EXPERT_VARIABLE_BUILD_DIR)/GoogleSans[opsz,wght].ttf

# italic
VARIABLE_BUILD_PATH_ITALIC=$(EXPERT_VARIABLE_BUILD_DIR)/GoogleSans-Italic-VF.ttf
VARIABLE_BUILD_PATH_ITALIC_TARGET=$(EXPERT_VARIABLE_BUILD_DIR)/GoogleSans-Italic[opsz,wght].ttf

# partial instances ('wght' axis only)
VARIABLE_BUILD_PATH_PARTIAL_UPRIGHT_MAX=$(EXPERT_VARIABLE_BUILD_DIR)/GoogleSans[opsz,wght].ttf.MAX_INSTANCE
VARIABLE_BUILD_PATH_PARTIAL_ITALIC_MAX=$(EXPERT_VARIABLE_BUILD_DIR)/GoogleSans-Italic[opsz,wght].ttf.MAX_INSTANCE
VARIABLE_BUILD_PATH_PARTIAL_UPRIGHT_MIN=$(EXPERT_VARIABLE_BUILD_DIR)/GoogleSans[opsz,wght].ttf.MIN_INSTANCE
VARIABLE_BUILD_PATH_PARTIAL_ITALIC_MIN=$(EXPERT_VARIABLE_BUILD_DIR)/GoogleSans-Italic[opsz,wght].ttf.MIN_INSTANCE

VARIABLE_BUILD_PATH_PARTIAL_UPRIGHT_MAX_TARGET=$(PARTIAL_INSTANCE_VARIABLE_BUILD_DIR)/GoogleSans[wght].ttf
VARIABLE_BUILD_PATH_PARTIAL_ITALIC_MAX_TARGET=$(PARTIAL_INSTANCE_VARIABLE_BUILD_DIR)/GoogleSans-Italic[wght].ttf
VARIABLE_BUILD_PATH_PARTIAL_UPRIGHT_MIN_TARGET=$(PARTIAL_INSTANCE_VARIABLE_BUILD_DIR)/GoogleSansText[wght].ttf
VARIABLE_BUILD_PATH_PARTIAL_ITALIC_MIN_TARGET=$(PARTIAL_INSTANCE_VARIABLE_BUILD_DIR)/GoogleSansText-Italic[wght].ttf

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

gs-static: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -m $(UPRIGHT_SOURCE) --interpolate -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR) --expand-features-to-instances
	$(FONTMAKE_EXE) -m $(ITALIC_SOURCE) --interpolate -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR) --expand-features-to-instances
	@echo "================================"
	@echo " Beginning post-compile edits..."
	@echo "================================"
	# edit Text opsz file paths
	mv $(EXPERT_STATIC_BUILD_DIR)/GoogleSans-TextRegular.ttf $(STATIC_TEXT_BUILD_PATH_REGULAR)
	mv $(EXPERT_STATIC_BUILD_DIR)/GoogleSans-TextItalic.ttf $(STATIC_TEXT_BUILD_PATH_ITALIC)
	mv $(EXPERT_STATIC_BUILD_DIR)/GoogleSans-TextBold.ttf $(STATIC_TEXT_BUILD_PATH_BOLD)
	mv $(EXPERT_STATIC_BUILD_DIR)/GoogleSans-TextBoldItalic.ttf $(STATIC_TEXT_BUILD_PATH_BOLDITALIC)
	mv $(EXPERT_STATIC_BUILD_DIR)/GoogleSans-TextMedium.ttf $(STATIC_TEXT_BUILD_PATH_MEDIUM)
	mv $(EXPERT_STATIC_BUILD_DIR)/GoogleSans-TextMediumItalic.ttf $(STATIC_TEXT_BUILD_PATH_MEDIUMITALIC)
	@echo "================================"
	@echo " Beginning font subsetting..."
	@echo "================================"
	$(PYTHON3_EXE) ../scripts/gs-subset.py
	@echo "================================"
	@echo " Add gasp & prep tables"
	@echo "================================"
	# Expert build targets
	$(PYTHON3_EXE) ../scripts/gftools-fix-nonhinting.py $(EXPERT_STATIC_BUILD_DIR)/*.ttf
	# Default build targets
	$(PYTHON3_EXE) ../scripts/gftools-fix-nonhinting.py $(DEFAULT_STATIC_BUILD_DIR)/*.ttf
	# remove the backups that the script leaves behind
	rm $(EXPERT_STATIC_BUILD_DIR)/*prep-gasp.ttf
	rm $(DEFAULT_STATIC_BUILD_DIR)/*prep-gasp.ttf


gs-vf: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -m $(UPRIGHT_SOURCE) -o variable --output-dir $(EXPERT_VARIABLE_BUILD_DIR)
	$(FONTMAKE_EXE) -m $(ITALIC_SOURCE) -o variable --output-dir $(EXPERT_VARIABLE_BUILD_DIR)
	@echo "================================"
	@echo " Beginning post-compile edits..."
	@echo "================================"
	@echo "================================"
	@echo " MVAR table removal"
	@echo "================================"
	$(PYTHON3_EXE) ../scripts/gftools-fix-unwanted-tables.py --tables MVAR $(EXPERT_VARIABLE_BUILD_DIR)/*.ttf
	mv $(VARIABLE_BUILD_PATH_UPRIGHT) "$(VARIABLE_BUILD_PATH_UPRIGHT_TARGET)"
	mv $(VARIABLE_BUILD_PATH_ITALIC) "$(VARIABLE_BUILD_PATH_ITALIC_TARGET)"
	@echo "================================"
	@echo " Add gasp & prep tables"
	@echo "================================"
	$(PYTHON3_EXE) ../scripts/gftools-fix-nonhinting.py $(EXPERT_VARIABLE_BUILD_DIR)/*.ttf
	# remove the backups that the script leaves behind
	rm $(EXPERT_VARIABLE_BUILD_DIR)/*prep-gasp.ttf
	@echo "================================"
	@echo " Partial instance build targets"
	@echo "================================"
	$(PYTHON3_EXE) ../scripts/gs-partial-instancer.py
	mkdir -p "$(PARTIAL_INSTANCE_VARIABLE_BUILD_DIR)"
	mv "$(VARIABLE_BUILD_PATH_PARTIAL_UPRIGHT_MAX)" "$(VARIABLE_BUILD_PATH_PARTIAL_UPRIGHT_MAX_TARGET)"
	mv "$(VARIABLE_BUILD_PATH_PARTIAL_ITALIC_MAX)" "$(VARIABLE_BUILD_PATH_PARTIAL_ITALIC_MAX_TARGET)"
	mv "$(VARIABLE_BUILD_PATH_PARTIAL_UPRIGHT_MIN)" "$(VARIABLE_BUILD_PATH_PARTIAL_UPRIGHT_MIN_TARGET)"
	mv "$(VARIABLE_BUILD_PATH_PARTIAL_ITALIC_MIN)" "$(VARIABLE_BUILD_PATH_PARTIAL_ITALIC_MIN_TARGET)"
	@echo "================================"
	@echo " Add STAT tables"
	@echo "================================"
	# STAT tables for 2-axis VF build targets
	$(PYTHON3_EXE) ../scripts/gs-stat.py
	# STAT tables for 1-axis (wght) build targets
	$(PYTHON3_EXE) ../scripts/gs-stat-partial.py

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
		$(wildcard $(STAGING_DIR)/*.designspace), \
		python ../scripts/gs-ufo2glyphs.py $(file); \
	)
#
#  Individual static instance build targets
#

# Google Sans (max optical size)
gs-regular: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -u $(UFO_GS_REGULAR) -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR)

gs-italic: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -u $(UFO_GS_ITALIC) -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR)

gs-medium: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -m $(UPRIGHT_SOURCE) -i "Google Sans Medium" -o ufo
	$(FONTMAKE_EXE) -u $(UFO_GS_MEDIUM) -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR)

gs-medium-italic: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -m $(ITALIC_SOURCE) -i "Google Sans Medium Italic" -o ufo
	$(FONTMAKE_EXE) -u $(UFO_GS_MEDIUMITALIC) -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR)

gs-bold: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -u $(UFO_GS_BOLD) -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR)

gs-bold-italic: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -u $(UFO_GS_BOLDITALIC) -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR)

# Google Sans Text (min optical size)
gst-regular: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -u $(UFO_GS_TEXT_REGULAR) -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR)

gst-italic: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -u $(UFO_GS_TEXT_ITALIC) -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR)

gst-medium: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -m $(UPRIGHT_SOURCE) -i "Google Sans Text Medium" -o ufo
	$(FONTMAKE_EXE) -u $(UFO_GS_TEXT_MEDIUM) -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR)

gst-medium-italic: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -m $(ITALIC_SOURCE) -i "Google Sans Text Medium Italic" -o ufo
	$(FONTMAKE_EXE) -u $(UFO_GS_TEXT_MEDIUMITALIC) -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR)

gst-bold: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -u $(UFO_GS_TEXT_BOLD) -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR)

gst-bold-italic: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -u $(UFO_GS_TEXT_BOLDITALIC) -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR)

#
# Individual variable font build targets
#

gs-vf-upright: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -m $(UPRIGHT_SOURCE) -o variable --output-dir $(EXPERT_VARIABLE_BUILD_DIR)

gs-vf-italic: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -m $(ITALIC_SOURCE) -o variable --output-dir $(EXPERT_VARIABLE_BUILD_DIR)

#
# Utilities
#
$(FONT_BUILD_DIR):
	mkdir -p $(FONT_BUILD_DIR)
	mkdir -p $(EXPERT_STATIC_BUILD_DIR)
	mkdir -p $(DEFAULT_STATIC_BUILD_DIR)
	mkdir -p $(EXPERT_VARIABLE_BUILD_DIR)
	mkdir -p $(DEFAULT_VARIABLE_BUILD_DIR)

$(STAGING_DIR):
	mkdir -p $(STAGING_DIR)

.PHONY: gs-static gs-vf \
gs-regular gs-italic gs-medium gs-medium-italic gs-bold gs-bold-italic \
gst-regular gst-italic gst-medium gst-medium-italic gst-bold gst-bold-italic \
gs-vf-upright gs-vf-italic
