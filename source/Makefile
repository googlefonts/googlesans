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

PYTHON3_EXE=../$(VENV_DIR)/bin/python3

# --------------------------------------------------------
#  fontmake compiler executable
#    NOTE: this builds from a venv install to support
#          pinned dependency versions
# --------------------------------------------------------
FONTMAKE_EXE=../$(VENV_DIR)/bin/fontmake

# --------------------------------------------------------
#  Source file path definitions
# --------------------------------------------------------
UPRIGHT_SOURCE=GoogleSans/GoogleSans.glyphs
ITALIC_SOURCE=GoogleSans/GoogleSans-Italic.glyphs

# --------------------------------------------------------
#  Build directory and file path definitions
# --------------------------------------------------------
FONT_BUILD_DIR=../build/GoogleSans
EXPERT_STATIC_BUILD_DIR=$(FONT_BUILD_DIR)/static/expert
DEFAULT_STATIC_BUILD_DIR=$(FONT_BUILD_DIR)/static/default
EXPERT_VARIABLE_BUILD_DIR=$(FONT_BUILD_DIR)/variable/expert
DEFAULT_VARIABLE_BUILD_DIR=$(FONT_BUILD_DIR)/variable/default

# Variable font paths
VARIABLE_BUILD_PATH_UPRIGHT=$(EXPERT_VARIABLE_BUILD_DIR)/GoogleSans-VF.ttf
VARIABLE_BUILD_PATH_UPRIGHT_TARGET=$(EXPERT_VARIABLE_BUILD_DIR)/GoogleSans[opsz,wght].ttf
VARIABLE_BUILD_PATH_ITALIC=$(EXPERT_VARIABLE_BUILD_DIR)/GoogleSans-Italic-VF.ttf
VARIABLE_BUILD_PATH_ITALIC_TARGET=$(EXPERT_VARIABLE_BUILD_DIR)/GoogleSans-Italic[opsz,wght].ttf

# --------------------------------------------------------
#  UFO intermediates and designspace paths
# --------------------------------------------------------
MASTER_UFO_DIR=$(FONT_BUILD_DIR)/master_ufo
INSTANCE_UFO_DIR=$(FONT_BUILD_DIR)/instance_ufo

UPRIGHT_DESIGNSPACE=GoogleSans.designspace
ITALIC_DESIGNSPACE=GoogleSans-Italic.designspace
UPRIGHT_DESIGNSPACE_PATH=$(MASTER_UFO_DIR)/$(UPRIGHT_DESIGNSPACE)
ITALIC_DESIGNSPACE_PATH=$(MASTER_UFO_DIR)/$(ITALIC_DESIGNSPACE)

# --------------------------------------------------------
#  Master and instance intermediate UFO file paths
# --------------------------------------------------------
UFO_GS_REGULAR=$(MASTER_UFO_DIR)/GoogleSans-Regular.ufo
UFO_GS_ITALIC=$(MASTER_UFO_DIR)/GoogleSans-Italic.ufo
UFO_GS_MEDIUM=$(INSTANCE_UFO_DIR)/GoogleSans-Medium.ufo
UFO_GS_MEDIUMITALIC=$(INSTANCE_UFO_DIR)/GoogleSans-MediumItalic.ufo
UFO_GS_BOLD=$(MASTER_UFO_DIR)/GoogleSans-Bold.ufo
UFO_GS_BOLDITALIC=$(MASTER_UFO_DIR)/GoogleSans-BoldItalic.ufo

UFO_GS_TEXT_REGULAR=$(MASTER_UFO_DIR)/GoogleSans-TextRegular.ufo
UFO_GS_TEXT_ITALIC=$(MASTER_UFO_DIR)/GoogleSans-TextItalic.ufo
UFO_GS_TEXT_MEDIUM=$(INSTANCE_UFO_DIR)/GoogleSans-TextMedium.ufo
UFO_GS_TEXT_MEDIUMITALIC=$(INSTANCE_UFO_DIR)/GoogleSans-TextMediumItalic.ufo
UFO_GS_TEXT_BOLD=$(MASTER_UFO_DIR)/GoogleSans-TextBold.ufo
UFO_GS_TEXT_BOLDITALIC=$(MASTER_UFO_DIR)/GoogleSans-TextBoldItalic.ufo

# --------------------------------------------------------
#  TARGETS
# --------------------------------------------------------

#
# Full font family build targets
#

gs-static: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -g $(UPRIGHT_SOURCE) --interpolate -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR) --master-dir $(MASTER_UFO_DIR) --instance-dir $(INSTANCE_UFO_DIR)
	$(FONTMAKE_EXE) -g $(ITALIC_SOURCE) --interpolate -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR) --master-dir $(MASTER_UFO_DIR) --instance-dir $(INSTANCE_UFO_DIR)
	@echo "================================"
	@echo " Beginning post-compile fixes..."
	@echo "================================"
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
	$(FONTMAKE_EXE) -g $(UPRIGHT_SOURCE) -o variable --output-dir $(EXPERT_VARIABLE_BUILD_DIR) --master-dir $(MASTER_UFO_DIR) --instance-dir $(INSTANCE_UFO_DIR)
	$(FONTMAKE_EXE) -g $(ITALIC_SOURCE) -o variable --output-dir $(EXPERT_VARIABLE_BUILD_DIR) --master-dir $(MASTER_UFO_DIR) --instance-dir $(INSTANCE_UFO_DIR)
	@echo "================================"
	@echo " Beginning post-compile fixes..."
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

#
#  Individual static instance build targets
#

# Google Sans (max optical size)
gs-regular: $(FONT_BUILD_DIR) build-designspace-upright
	$(FONTMAKE_EXE) -u $(UFO_GS_REGULAR) -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR)

gs-italic: $(FONT_BUILD_DIR) build-designspace-italic
	$(FONTMAKE_EXE) -u $(UFO_GS_ITALIC) -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR)

gs-medium: $(FONT_BUILD_DIR) build-designspace-upright
	$(FONTMAKE_EXE) -m $(UPRIGHT_DESIGNSPACE_PATH) -i "Google Sans Medium" -o ufo
	$(FONTMAKE_EXE) -u $(UFO_GS_MEDIUM) -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR)

gs-medium-italic: $(FONT_BUILD_DIR) build-designspace-italic
	$(FONTMAKE_EXE) -m $(ITALIC_DESIGNSPACE_PATH) -i "Google Sans Medium Italic" -o ufo
	$(FONTMAKE_EXE) -u $(UFO_GS_MEDIUMITALIC) -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR)

gs-bold: $(FONT_BUILD_DIR) build-designspace-upright
	$(FONTMAKE_EXE) -u $(UFO_GS_BOLD) -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR)

gs-bold-italic: $(FONT_BUILD_DIR) build-designspace-italic
	$(FONTMAKE_EXE) -u $(UFO_GS_BOLDITALIC) -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR)

# Google Sans Text (min optical size)
gst-regular: $(FONT_BUILD_DIR) build-designspace-upright
	$(FONTMAKE_EXE) -u $(UFO_GS_TEXT_REGULAR) -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR)

gst-italic: $(FONT_BUILD_DIR) build-designspace-italic
	$(FONTMAKE_EXE) -u $(UFO_GS_TEXT_ITALIC) -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR)

gst-medium: $(FONT_BUILD_DIR) build-designspace-upright
	$(FONTMAKE_EXE) -m $(UPRIGHT_DESIGNSPACE_PATH) -i "Google Sans Text Medium" -o ufo
	$(FONTMAKE_EXE) -u $(UFO_GS_TEXT_MEDIUM) -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR)

gst-medium-italic: $(FONT_BUILD_DIR) build-designspace-italic
	$(FONTMAKE_EXE) -m $(ITALIC_DESIGNSPACE_PATH) -i "Google Sans Text Medium Italic" -o ufo
	$(FONTMAKE_EXE) -u $(UFO_GS_TEXT_MEDIUMITALIC) -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR)

gst-bold: $(FONT_BUILD_DIR) build-designspace-upright
	$(FONTMAKE_EXE) -u $(UFO_GS_TEXT_BOLD) -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR)

gst-bold-italic: $(FONT_BUILD_DIR) build-designspace-italic
	$(FONTMAKE_EXE) -u $(UFO_GS_TEXT_BOLDITALIC) -o ttf --output-dir $(EXPERT_STATIC_BUILD_DIR)

#
# Individual variable font build targets
#

gs-vf-upright: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -g $(UPRIGHT_SOURCE) -o variable --output-dir $(EXPERT_VARIABLE_BUILD_DIR) --master-dir $(MASTER_UFO_DIR) --instance-dir $(INSTANCE_UFO_DIR)

gs-vf-italic: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -g $(ITALIC_SOURCE) -o variable --output-dir $(EXPERT_VARIABLE_BUILD_DIR) --master-dir $(MASTER_UFO_DIR) --instance-dir $(INSTANCE_UFO_DIR)

#
#  Design space build targets
#

build-designspace-upright: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -g $(UPRIGHT_SOURCE) -o ufo --master-dir $(MASTER_UFO_DIR) --instance-dir $(INSTANCE_UFO_DIR)


build-designspace-italic: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -g $(ITALIC_SOURCE) -o ufo --master-dir $(MASTER_UFO_DIR) --instance-dir $(INSTANCE_UFO_DIR)


#
# Utilities
#
$(FONT_BUILD_DIR):
	mkdir -p $(FONT_BUILD_DIR)
	mkdir -p $(EXPERT_STATIC_BUILD_DIR)
	mkdir -p $(DEFAULT_STATIC_BUILD_DIR)
	mkdir -p $(EXPERT_VARIABLE_BUILD_DIR)
	mkdir -p $(DEFAULT_VARIABLE_BUILD_DIR)

.PHONY: gs-static gs-vf \
gs-regular gs-italic gs-medium gs-medium-italic gs-bold gs-bold-italic \
gst-regular gst-italic gst-medium gst-medium-italic gst-bold gst-bold-italic \
gs-vf-upright gs-vf-italic \
build-designspace-upright build-designspace-italic
