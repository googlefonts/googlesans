# Copyright 2020 Google Sans Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
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
FONTMAKE_EXE_NO_COMPACTION=fontmake --verbose WARNING

# --------------------------------------------------------
#  Source file path definitions
# --------------------------------------------------------
SOURCE=GoogleSans/GoogleSans.designspace

# --------------------------------------------------------
#  Build directory and file path definitions
# --------------------------------------------------------
FONT_BUILD_DIR=../build/GoogleSans
STATIC_BUILD_DIR=$(FONT_BUILD_DIR)/static
INTERMEDIATE_VARIABLE_DIR=$(FONT_BUILD_DIR)/.intermediate
VARIABLE_BUILD_DIR=$(FONT_BUILD_DIR)/variable
INTERPOLATABLE_BUILD_DIR=$(FONT_BUILD_DIR)/interpolatable

STAGING_DIR=GoogleSans/staging

# Artifact paths
STATIC_UPRIGHTS_TARGETS = $(addprefix $(STATIC_BUILD_DIR)/,GoogleSansText-Regular.ttf GoogleSansText-Bold.ttf GoogleSansText-Medium.ttf GoogleSans-Regular.ttf GoogleSans-Bold.ttf GoogleSans-Medium.ttf)
STATIC_ITALICS_TARGETS = $(addprefix $(STATIC_BUILD_DIR)/,GoogleSans-BoldItalic.ttf GoogleSans-Italic.ttf GoogleSansText-MediumItalic.ttf GoogleSansText-BoldItalic.ttf GoogleSansText-Italic.ttf GoogleSans-MediumItalic.ttf)

INTERPOLATABLE_UPRIGHTS_TARGET = $(INTERPOLATABLE_BUILD_DIR)/GoogleSans.designspace
INTERPOLATABLE_ITALICS_TARGET = $(INTERPOLATABLE_BUILD_DIR)/GoogleSans-Italic.designspace

VARIABLE_UPRIGHT_INTERMEDIATE = $(INTERMEDIATE_VARIABLE_DIR)/GoogleSans[GRAD,opsz,wght].ttf
VARIABLE_ITALIC_INTERMEDIATE = $(INTERMEDIATE_VARIABLE_DIR)/GoogleSans-Italic[GRAD,opsz,wght].ttf
VARIABLE_UPRIGHT_TARGET = $(VARIABLE_BUILD_DIR)/GoogleSans[GRAD,opsz,wght].ttf
VARIABLE_ITALIC_TARGET = $(VARIABLE_BUILD_DIR)/GoogleSans-Italic[GRAD,opsz,wght].ttf

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

gs-vf: gs-vf-upright gs-vf-italic
gs-vf-upright: $(VARIABLE_UPRIGHT_TARGET)
gs-vf-italic: $(VARIABLE_ITALIC_TARGET)

$(VARIABLE_UPRIGHT_INTERMEDIATE): $(FONT_BUILD_DIR) $(UPRIGHT_ALL_SOURCES)
	$(FONTMAKE_EXE) -m $(SOURCE) --variable-fonts "GoogleSans-VF" -o variable --output-path $@
	$(PYTHON3_EXE) ../scripts/gs-subset.py $@
	$(PYTHON3_EXE) ../scripts/internal/set-overlap-bits.py $@
	$(PYTHON3_EXE) ../scripts/set-unicoderange.py $@
	$(PYTHON3_EXE) ../scripts/gftools-fix-unwanted-tables.py $@
	$(PYTHON3_EXE) ../scripts/gftools-fix-nonhinting.py $@
	font-v write --sha1 $@

$(VARIABLE_UPRIGHT_TARGET): $(VARIABLE_UPRIGHT_INTERMEDIATE)
	$(PYTHON3_EXE) ../scripts/patch-figma-fvar.py $(VARIABLE_UPRIGHT_INTERMEDIATE) --output $@

$(VARIABLE_ITALIC_INTERMEDIATE): $(FONT_BUILD_DIR) $(ITALIC_ALL_SOURCES)
	$(FONTMAKE_EXE) -m $(SOURCE) --variable-fonts "GoogleSans-Italic-VF" -o variable --output-path $@
	$(PYTHON3_EXE) ../scripts/gs-subset.py $@
	$(PYTHON3_EXE) ../scripts/internal/set-overlap-bits.py $@
	$(PYTHON3_EXE) ../scripts/set-unicoderange.py $@
	$(PYTHON3_EXE) ../scripts/gftools-fix-unwanted-tables.py $@
	$(PYTHON3_EXE) ../scripts/gftools-fix-nonhinting.py $@
	font-v write --sha1 $@

$(VARIABLE_ITALIC_TARGET): $(VARIABLE_ITALIC_INTERMEDIATE)
	$(PYTHON3_EXE) ../scripts/patch-figma-fvar.py $(VARIABLE_ITALIC_INTERMEDIATE) --output $@


gs-static: gs-static-upright gs-static-italic
gs-static-upright: $(STATIC_UPRIGHTS_TARGETS)
gs-static-italic: $(STATIC_ITALICS_TARGETS)

$(STATIC_UPRIGHTS_TARGETS): $(VARIABLE_UPRIGHT_INTERMEDIATE)
	$(PYTHON3_EXE) ../scripts/internal/cut-instances.py $< $(SOURCE) $@
	$(PYTHON3_EXE) ../scripts/gs-subset.py $@
	$(PYTHON3_EXE) -m fontTools.otlLib.optimize --gpos-compression-level 5 $@
	font-v write --sha1 $@

$(STATIC_ITALICS_TARGETS): $(VARIABLE_ITALIC_INTERMEDIATE)
	$(PYTHON3_EXE) ../scripts/internal/cut-instances.py $< $(SOURCE) $@
	$(PYTHON3_EXE) ../scripts/gs-subset.py $@
	$(PYTHON3_EXE) -m fontTools.otlLib.optimize --gpos-compression-level 5 $@
	font-v write --sha1 $@


gs-compatible-masters: gs-compatible-masters-upright gs-compatible-masters-italic
gs-compatible-masters-upright: $(INTERPOLATABLE_UPRIGHTS_TARGET)
gs-compatible-masters-italic: $(INTERPOLATABLE_ITALICS_TARGET)

$(INTERPOLATABLE_UPRIGHTS_TARGET): $(FONT_BUILD_DIR) $(UPRIGHT_ALL_SOURCES)
	$(FONTMAKE_EXE_NO_COMPACTION) --no-production-names -m $(SOURCE) --variable-fonts "GoogleSans-VF" -o ttf-interpolatable --output-dir $(INTERPOLATABLE_BUILD_DIR)

$(INTERPOLATABLE_ITALICS_TARGET): $(FONT_BUILD_DIR) $(ITALIC_ALL_SOURCES)
	$(FONTMAKE_EXE_NO_COMPACTION) --no-production-names -m $(SOURCE) --variable-fonts "GoogleSans-Italic-VF" -o ttf-interpolatable --output-dir $(INTERPOLATABLE_BUILD_DIR)


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
	$(FONTMAKE_EXE) -m $(SOURCE) -i "Google Sans Medium" -o ufo
	$(FONTMAKE_EXE) -u $(UFO_GS_MEDIUM) -o ttf --output-dir $(STATIC_BUILD_DIR)

gs-medium-italic: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -m $(SOURCE) -i "Google Sans Medium Italic" -o ufo
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
	$(FONTMAKE_EXE) -m $(SOURCE) -i "Google Sans Text Medium" -o ufo
	$(FONTMAKE_EXE) -u $(UFO_GS_TEXT_MEDIUM) -o ttf --output-dir $(STATIC_BUILD_DIR)

gst-medium-italic: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -m $(SOURCE) -i "Google Sans Text Medium Italic" -o ufo
	$(FONTMAKE_EXE) -u $(UFO_GS_TEXT_MEDIUMITALIC) -o ttf --output-dir $(STATIC_BUILD_DIR)

gst-bold: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -u $(UFO_GS_TEXT_BOLD) -o ttf --output-dir $(STATIC_BUILD_DIR)

gst-bold-italic: $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -u $(UFO_GS_TEXT_BOLDITALIC) -o ttf --output-dir $(STATIC_BUILD_DIR)


#
# Utilities
#
$(FONT_BUILD_DIR):
	mkdir -p $(STATIC_BUILD_DIR) $(INTERMEDIATE_VARIABLE_DIR) $(VARIABLE_BUILD_DIR) $(INTERPOLATABLE_BUILD_DIR)

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
