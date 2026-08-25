export UV_PYTHON=$(shell cat .github/workflows/python-version.txt)
UV_RUN=uv run --quiet --with-requirements requirements.txt

SOURCES=$(shell python3 scripts/read-config.py --sources)
FAMILY=$(shell python3 scripts/read-config.py --family)

FONT_BUILD_DIR=fonts
FONT_NAME_UPRIGHT=GoogleSans[GRAD,opsz,wght].ttf
FONT_NAME_ITALIC=GoogleSans-Italic[GRAD,opsz,wght].ttf

INTERMEDIATE_VARIABLE_DIR=$(FONT_BUILD_DIR)/.intermediate
VARIABLE_UPRIGHT_INTERMEDIATE=$(INTERMEDIATE_VARIABLE_DIR)/$(FONT_NAME_UPRIGHT)
VARIABLE_ITALIC_INTERMEDIATE=$(INTERMEDIATE_VARIABLE_DIR)/$(FONT_NAME_ITALIC)

VARIABLE_BUILD_DIR=$(FONT_BUILD_DIR)/variable
VARIABLE_UPRIGHT_TARGET=$(VARIABLE_BUILD_DIR)/$(FONT_NAME_UPRIGHT)
VARIABLE_ITALIC_TARGET=$(VARIABLE_BUILD_DIR)/$(FONT_NAME_ITALIC)

STATIC_BUILD_DIR=$(FONT_BUILD_DIR)/static
STATIC_UPRIGHTS_TARGETS = $(addprefix $(STATIC_BUILD_DIR)/,GoogleSansText-Regular.ttf GoogleSansText-Bold.ttf GoogleSansText-Medium.ttf GoogleSans-Regular.ttf GoogleSans-Bold.ttf GoogleSans-Medium.ttf)
STATIC_ITALICS_TARGETS = $(addprefix $(STATIC_BUILD_DIR)/,GoogleSans-BoldItalic.ttf GoogleSans-Italic.ttf GoogleSansText-MediumItalic.ttf GoogleSansText-BoldItalic.ttf GoogleSansText-Italic.ttf GoogleSans-MediumItalic.ttf)

ANDROID_BUILD_DIR=$(FONT_BUILD_DIR)/android
VARIABLE_ANDROID_UPRIGHT_TARGET=$(ANDROID_BUILD_DIR)/variable/$(FONT_NAME_UPRIGHT)
VARIABLE_ANDROID_UPRIGHT_CHARACTERS=android/characters-roman-v4.txt
VARIABLE_ANDROID_ITALIC_TARGET=$(ANDROID_BUILD_DIR)/variable/$(FONT_NAME_ITALIC)
VARIABLE_ANDROID_ITALIC_CHARACTERS=android/characters-italic-v4.txt
STATIC_ANDROID_UPRIGHT_TARGETS = $(addprefix $(ANDROID_BUILD_DIR)/static/,GoogleSansText-Regular.ttf GoogleSansText-Bold.ttf GoogleSansText-Medium.ttf GoogleSans-Regular.ttf GoogleSans-Bold.ttf GoogleSans-Medium.ttf)
STATIC_ANDROID_ITALIC_TARGETS = $(addprefix $(ANDROID_BUILD_DIR)/static/,GoogleSans-BoldItalic.ttf GoogleSans-Italic.ttf GoogleSansText-MediumItalic.ttf GoogleSansText-BoldItalic.ttf GoogleSansText-Italic.ttf GoogleSans-MediumItalic.ttf)

FIGMA_BUILD_DIR=$(FONT_BUILD_DIR)/figma

export FONTTOOLS_GPOS_COMPACT_MODE = 5

help:
	@echo "Build targets for Google Sans"
	@echo
	@echo "  make build:  Builds the variable fonts and places them in the fonts/ directory"
	@echo "  make test:   Tests the fonts with Fontspector"

#################
# Build targets #
#################

build: build.stamp

build.stamp: requirements.txt sources/config.yaml $(SOURCES)
	@rm -rf $(FONT_BUILD_DIR)/*
	$(UV_RUN) gftools builder sources/config.yaml
	@mkdir -p $(VARIABLE_BUILD_DIR)
	$(UV_RUN) --script scripts/patch-figma-fvar.py \
		$(VARIABLE_UPRIGHT_INTERMEDIATE) \
		--output $(VARIABLE_UPRIGHT_TARGET)
	$(UV_RUN) --script scripts/patch-figma-fvar.py \
		$(VARIABLE_ITALIC_INTERMEDIATE) \
		--output $(VARIABLE_ITALIC_TARGET)
	@touch build.stamp

static: static-upright static-italic
static-upright: $(STATIC_UPRIGHTS_TARGETS)
static-italic: $(STATIC_ITALICS_TARGETS)

$(STATIC_UPRIGHTS_TARGETS): build
	@mkdir -p $(STATIC_BUILD_DIR)
	$(UV_RUN) scripts/internal/cut-instances.py \
		$(VARIABLE_UPRIGHT_INTERMEDIATE) \
		sources/GoogleSans.designspace \
		$@
	$(UV_RUN) scripts/gs-subset.py $@
	$(UV_RUN) python -m fontTools.otlLib.optimize --gpos-compression-level 5 $@

$(STATIC_ITALICS_TARGETS): build
	@mkdir -p $(STATIC_BUILD_DIR)
	$(UV_RUN) scripts/internal/cut-instances.py \
		$(VARIABLE_ITALIC_INTERMEDIATE) \
		sources/GoogleSans-Italic.designspace \
		$@
	$(UV_RUN) scripts/gs-subset.py $@
	$(UV_RUN) python -m fontTools.otlLib.optimize --gpos-compression-level 5 $@

android: android-vf android-static
android-vf: android-vf-upright android-vf-italic
android-vf-upright: $(VARIABLE_ANDROID_UPRIGHT_TARGET)
android-vf-italic: $(VARIABLE_ANDROID_ITALIC_TARGET)

$(VARIABLE_ANDROID_UPRIGHT_TARGET): build $(VARIABLE_ANDROID_UPRIGHT_CHARACTERS)
	@mkdir -p $(ANDROID_BUILD_DIR)/variable
	$(UV_RUN) android/build-android-vfs.py \
		$(VARIABLE_UPRIGHT_TARGET) \
		$(VARIABLE_ANDROID_UPRIGHT_CHARACTERS) \
		$(VARIABLE_ANDROID_UPRIGHT_TARGET)

$(VARIABLE_ANDROID_ITALIC_TARGET): build $(VARIABLE_ANDROID_ITALIC_CHARACTERS)
	@mkdir -p $(ANDROID_BUILD_DIR)/variable
	$(UV_RUN) android/build-android-vfs.py \
		$(VARIABLE_ITALIC_TARGET) \
		$(VARIABLE_ANDROID_ITALIC_CHARACTERS) \
		$(VARIABLE_ANDROID_ITALIC_TARGET)

android-static: android-static-upright android-static-italic
android-static-upright: $(STATIC_ANDROID_UPRIGHT_TARGETS)
android-static-italic: $(STATIC_ANDROID_ITALIC_TARGETS)

$(STATIC_ANDROID_UPRIGHT_TARGETS): $(VARIABLE_ANDROID_UPRIGHT_TARGET)
	@mkdir -p $(ANDROID_BUILD_DIR)/static
	$(UV_RUN) scripts/internal/cut-instances.py \
		$(VARIABLE_ANDROID_UPRIGHT_TARGET) \
		sources/GoogleSans.designspace \
		$@
	$(UV_RUN) scripts/gs-subset.py $@
	$(UV_RUN) python -m fontTools.otlLib.optimize --gpos-compression-level 5 $@

$(STATIC_ANDROID_ITALIC_TARGETS): $(VARIABLE_ANDROID_ITALIC_TARGET)
	@mkdir -p $(ANDROID_BUILD_DIR)/static
	$(UV_RUN) scripts/internal/cut-instances.py \
		$(VARIABLE_ANDROID_ITALIC_TARGET) \
		sources/GoogleSans-Italic.designspace \
		$@
	$(UV_RUN) scripts/gs-subset.py $@
	$(UV_RUN) python -m fontTools.otlLib.optimize --gpos-compression-level 5 $@

figma: build
	@mkdir -p $(FIGMA_BUILD_DIR)
	$(UV_RUN) gftools-rename-font $(VARIABLE_UPRIGHT_TARGET) \
		--suffix " Variable" \
		--out $(FIGMA_BUILD_DIR)/GoogleSansVariable[GRAD,opsz,wght].ttf
	$(UV_RUN) gftools-rename-font $(VARIABLE_ITALIC_TARGET) \
		--suffix " Variable" \
		--out $(FIGMA_BUILD_DIR)/GoogleSansVariable-Italic[GRAD,opsz,wght].ttf

all: build static android figma

################
# Test targets #
################

test: test-static test-vf

test-static:
	@echo "==================================================="
	@echo " `fontspector -V` static font checks"
	@echo "==================================================="
	fontspector --loglevel warn --succinct --full-lists \
		--profile qa/check-googlesans.toml \
		--plugin qa/check-charset.py,qa/check-fea.py,qa/check-googlesans.py \
		$(STATIC_BUILD_DIR)/*.ttf

test-vf:
	@echo "==================================================="
	@echo " `fontspector -V` variable font checks"
	@echo "==================================================="
	fontspector --loglevel warn --succinct --full-lists \
		--profile qa/check-googlesans.toml \
		--plugin qa/check-charset.py,qa/check-fea.py,qa/check-googlesans.py \
		$(VARIABLE_BUILD_DIR)/*.ttf

test-figma:
	@echo "==================================================="
	@echo " `fontspector -V` Figma font checks"
	@echo "==================================================="
	fontspector --loglevel warn --succinct --full-lists \
		--profile qa/check-googlesans.toml \
		--plugin qa/check-charset.py,qa/check-fea.py,qa/check-googlesans.py \
		$(FONT_BUILD_DIR)/figma/*.ttf

test-android:
	@echo "==================================================="
	@echo " `fontspector -V` Android font checks"
	@echo "==================================================="
	fontspector --loglevel warn --succinct --full-lists \
		--profile qa/check-googlesans.toml \
		--plugin qa/check-charset.py,qa/check-fea.py,qa/check-googlesans.py \
		$(FONT_BUILD_DIR)/android/*/*.ttf

#################################
# Working with external vendors #
#################################

STAGING_DIR=sources/staging

vendor-build: vendor-glyphs2designspace
	$(foreach \
		file, \
		$(wildcard $(STAGING_DIR)/*.designspace), \
		$(UV_RUN) fontmake -m $(file) -o variable --output-dir $(STAGING_DIR); \
	)
	@echo "Note: vendor fonts are built with fontmake, not gftools, and so may have some differences as a result"

vendor-glyphs2designspace: $(wildcard sources/*.glyphs)
	$(UV_RUN) scripts/gs-glyphs2ufo.py sources/*.glyphs --target-dir $(STAGING_DIR)

# Export Google Sans as Glyphs files
ufo2glyphs: $(wildcard GoogleSans/*.designspace)
	$(foreach \
		file, \
		$(wildcard GoogleSans/*.designspace), \
		$(UV_RUN) scripts/gs-ufo2glyphs.py $(file); \
	)

#################
# Misc. targets #
#################

update-glyphset-expectations:
	$(UV_RUN) scripts/gs-update-glyphset-qa-files.py

update-shaping-expectations:
	$(UV_RUN) bash -c "cd qa && bash update_all_shaping.sh"

autobase: build
	cargo binstall autobase-cli --no-confirm || cargo install --locked autobase-cli
	autobase --min-max --config source/GoogleSans/autobase.toml --words 1000000 build/GoogleSans/variable/GoogleSans*.ttf

metadata:
	cd metadata && python metadata-builder.py

.PHONY: help \
test test-static test-vf test-android test-figma \
update-glyphset-expectations update-shaping-expectations

# Disable built-in rules to speed up source globbing.
MAKEFLAGS += --no-builtin-rules
.SUFFIXES:
