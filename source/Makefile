
# --------------------------------------------------------
#  fontmake compiler executable
#    NOTE: this builds from a venv install to support
#          pinned dependency versions
# --------------------------------------------------------
FONTMAKE_EXE=fontmake --verbose WARNING

# --------------------------------------------------------
#  Source file path definitions
# --------------------------------------------------------
UPRIGHT_SOURCE=GoogleSans/GoogleSans.designspace
ITALIC_SOURCE=GoogleSans/GoogleSans-Italic.designspace
STYLESPACE=GoogleSans/GoogleSans.stylespace

# --------------------------------------------------------
#  Build directory and file path definitions
# --------------------------------------------------------
FONT_BUILD_DIR=../build/GoogleSans
FONT_BUILD_TEMP_DIR=../build/tmp
STATIC_BUILD_DIR=$(FONT_BUILD_DIR)/static
VARIABLE_BUILD_DIR=$(FONT_BUILD_DIR)/variable
VARIABLE_BUILD_TEMP_DIR=$(FONT_BUILD_TEMP_DIR)/variable

# Variable font build artifacts

# upright
VARIABLE_BUILD_PATH_UPRIGHT=$(VARIABLE_BUILD_TEMP_DIR)/GoogleSans-VF.ttf
VARIABLE_BUILD_PATH_UPRIGHT_TARGET=$(VARIABLE_BUILD_DIR)/GoogleSans[GRAD,opsz,wght].ttf
STATIC_B_TARGET=$(STATIC_BUILD_DIR)/GoogleSans-Bold.ttf
STATIC_M_TARGET=$(STATIC_BUILD_DIR)/GoogleSans-Medium.ttf
STATIC_R_TARGET=$(STATIC_BUILD_DIR)/GoogleSans-Regular.ttf
STATIC_TB_TARGET=$(STATIC_BUILD_DIR)/GoogleSansText-Bold.ttf
STATIC_TM_TARGET=$(STATIC_BUILD_DIR)/GoogleSansText-Medium.ttf
STATIC_TR_TARGET=$(STATIC_BUILD_DIR)/GoogleSansText-Regular.ttf

# italic
VARIABLE_BUILD_PATH_ITALIC=$(VARIABLE_BUILD_TEMP_DIR)/GoogleSans-Italic-VF.ttf
VARIABLE_BUILD_PATH_ITALIC_TARGET=$(VARIABLE_BUILD_DIR)/GoogleSans-Italic[GRAD,opsz,wght].ttf
STATIC_BI_TARGET=$(STATIC_BUILD_DIR)/GoogleSans-BoldItalic.ttf
STATIC_I_TARGET=$(STATIC_BUILD_DIR)/GoogleSans-Italic.ttf
STATIC_MI_TARGET=$(STATIC_BUILD_DIR)/GoogleSans-MediumItalic.ttf
STATIC_TBI_TARGET=$(STATIC_BUILD_DIR)/GoogleSansText-BoldItalic.ttf
STATIC_TI_TARGET=$(STATIC_BUILD_DIR)/GoogleSansText-Italic.ttf
STATIC_TMI_TARGET=$(STATIC_BUILD_DIR)/GoogleSansText-MediumItalic.ttf


UPRIGHT_SOURCES := \
	$(UPRIGHT_SOURCE) \
	$(wildcard GoogleSans/GoogleSans-*.ufo/*.plist) \
	$(wildcard GoogleSans/GoogleSans-*.ufo/glyphs/*.glif) \
	$(wildcard GoogleSans/GoogleSans-*.ufo/glyphs/contents.plist)

ITALIC_SOURCES := \
	$(ITALIC_SOURCE) \
	$(wildcard GoogleSans/GoogleSansItalic-*.ufo/*.plist) \
	$(wildcard GoogleSans/GoogleSansItalic-*.ufo/glyphs/*.glif) \
	$(wildcard GoogleSans/GoogleSansItalic-*.ufo/glyphs/contents.plist)


gs-vf: gs-vf-upright gs-vf-italic
gs-vf-upright: $(VARIABLE_BUILD_PATH_UPRIGHT_TARGET)
gs-vf-italic: $(VARIABLE_BUILD_PATH_ITALIC_TARGET)
gs-static: $(STATIC_B_TARGET) $(STATIC_M_TARGET) $(STATIC_R_TARGET) $(STATIC_TB_TARGET) $(STATIC_TM_TARGET) $(STATIC_TR_TARGET) $(STATIC_BI_TARGET) $(STATIC_I_TARGET) $(STATIC_MI_TARGET) $(STATIC_TBI_TARGET) $(STATIC_TI_TARGET) $(STATIC_TMI_TARGET)


$(VARIABLE_BUILD_PATH_UPRIGHT): $(UPRIGHT_SOURCES) $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -m $(UPRIGHT_SOURCE) -o variable --output-dir $(VARIABLE_BUILD_TEMP_DIR)

$(VARIABLE_BUILD_PATH_UPRIGHT_TARGET): $(VARIABLE_BUILD_PATH_UPRIGHT)
	python ../scripts/gs-subset.py "$^"
	python ../scripts/gftools-fix-nonhinting.py "$^"
	statmake "$^" --designspace $(UPRIGHT_SOURCE)
	mv "$^" "$@"

$(VARIABLE_BUILD_PATH_ITALIC): $(ITALIC_SOURCES) $(FONT_BUILD_DIR)
	$(FONTMAKE_EXE) -m $(ITALIC_SOURCE) -o variable --output-dir $(VARIABLE_BUILD_TEMP_DIR)

$(VARIABLE_BUILD_PATH_ITALIC_TARGET): $(VARIABLE_BUILD_PATH_ITALIC)
	python ../scripts/gs-subset.py "$^"
	python ../scripts/gftools-fix-nonhinting.py "$^"
	statmake "$^" --designspace $(ITALIC_SOURCE)
	mv "$^" "$@"


$(STATIC_B_TARGET): $(VARIABLE_BUILD_PATH_UPRIGHT_TARGET)
	python ../scripts/gs-cut-instance.py $(VARIABLE_BUILD_PATH_UPRIGHT_TARGET) $(STATIC_B_TARGET) $(UPRIGHT_SOURCE)

$(STATIC_M_TARGET): $(VARIABLE_BUILD_PATH_UPRIGHT_TARGET)
	python ../scripts/gs-cut-instance.py $(VARIABLE_BUILD_PATH_UPRIGHT_TARGET) $(STATIC_M_TARGET) $(UPRIGHT_SOURCE)

$(STATIC_R_TARGET): $(VARIABLE_BUILD_PATH_UPRIGHT_TARGET)
	python ../scripts/gs-cut-instance.py $(VARIABLE_BUILD_PATH_UPRIGHT_TARGET) $(STATIC_R_TARGET) $(UPRIGHT_SOURCE)

$(STATIC_TB_TARGET): $(VARIABLE_BUILD_PATH_UPRIGHT_TARGET)
	python ../scripts/gs-cut-instance.py $(VARIABLE_BUILD_PATH_UPRIGHT_TARGET) $(STATIC_TB_TARGET) $(UPRIGHT_SOURCE)

$(STATIC_TM_TARGET): $(VARIABLE_BUILD_PATH_UPRIGHT_TARGET)
	python ../scripts/gs-cut-instance.py $(VARIABLE_BUILD_PATH_UPRIGHT_TARGET) $(STATIC_TM_TARGET) $(UPRIGHT_SOURCE)

$(STATIC_TR_TARGET): $(VARIABLE_BUILD_PATH_UPRIGHT_TARGET)
	python ../scripts/gs-cut-instance.py $(VARIABLE_BUILD_PATH_UPRIGHT_TARGET) $(STATIC_TR_TARGET) $(UPRIGHT_SOURCE)


$(STATIC_BI_TARGET): $(VARIABLE_BUILD_PATH_ITALIC_TARGET)
	python ../scripts/gs-cut-instance.py $(VARIABLE_BUILD_PATH_ITALIC_TARGET) $(STATIC_BI_TARGET) $(ITALIC_SOURCE)

$(STATIC_I_TARGET): $(VARIABLE_BUILD_PATH_ITALIC_TARGET)
	python ../scripts/gs-cut-instance.py $(VARIABLE_BUILD_PATH_ITALIC_TARGET) $(STATIC_I_TARGET) $(ITALIC_SOURCE)

$(STATIC_MI_TARGET): $(VARIABLE_BUILD_PATH_ITALIC_TARGET)
	python ../scripts/gs-cut-instance.py $(VARIABLE_BUILD_PATH_ITALIC_TARGET) $(STATIC_MI_TARGET) $(ITALIC_SOURCE)

$(STATIC_TBI_TARGET): $(VARIABLE_BUILD_PATH_ITALIC_TARGET)
	python ../scripts/gs-cut-instance.py $(VARIABLE_BUILD_PATH_ITALIC_TARGET) $(STATIC_TBI_TARGET) $(ITALIC_SOURCE)

$(STATIC_TI_TARGET): $(VARIABLE_BUILD_PATH_ITALIC_TARGET)
	python ../scripts/gs-cut-instance.py $(VARIABLE_BUILD_PATH_ITALIC_TARGET) $(STATIC_TI_TARGET) $(ITALIC_SOURCE)

$(STATIC_TMI_TARGET): $(VARIABLE_BUILD_PATH_ITALIC_TARGET)
	python ../scripts/gs-cut-instance.py $(VARIABLE_BUILD_PATH_ITALIC_TARGET) $(STATIC_TMI_TARGET) $(ITALIC_SOURCE)


$(FONT_BUILD_DIR):
	mkdir -p $(FONT_BUILD_DIR)
	mkdir -p $(STATIC_BUILD_DIR)
	mkdir -p $(VARIABLE_BUILD_DIR)
	mkdir -p $(VARIABLE_BUILD_TEMP_DIR)

$(STAGING_DIR):
	mkdir -p $(STAGING_DIR)


# Helper targets 
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


# Settings

# Disable built-in rules to speed up source globbing.
MAKEFLAGS += --no-builtin-rules
.SUFFIXES:

.PHONY: gs-vf gs-vf-upright gs-vf-italic gs-static gs-vf-vendor gs-vf-vendor-glyphs2designspace gs-ufo2glyphs
