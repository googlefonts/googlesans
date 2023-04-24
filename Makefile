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

FONT_BUILD_DIR=build/GoogleSans
STATIC_BUILD_DIR=$(FONT_BUILD_DIR)/static
VARIABLE_BUILD_DIR=$(FONT_BUILD_DIR)/variable
MASTER_UFO_DIR=$(FONT_BUILD_DIR)/master_ufo
INSTANCE_UFO_DIR=$(FONT_BUILD_DIR)/instance_ufo
VENV_DIR=.venv

all: gs-static gs-compatible-masters  # gs-vf is built by gs-static

# ------------------------------
# Clean
# ------------------------------

# clean performs post-build cleanup tasks
clean:
	rm -rf "$(MASTER_UFO_DIR)"
	rm -rf "$(INSTANCE_UFO_DIR)"
	rm -rf "$(VENV_DIR)"

# clean-builds removes the font build dir and all font artifact contents
clean-builds:
	rm -rf "$(FONT_BUILD_DIR)"

# clean intermediate UFO masters and instances
clean-ufo:
	rm -rf "$(MASTER_UFO_DIR)"
	rm -rf "$(INSTANCE_UFO_DIR)"

# ------------------------------
# Compile
# ------------------------------

gs-static gs-vf gs-vf-vendor gs-compatible-masters gs-compatible-masters-upright gs-compatible-masters-italic:
	cd source && $(MAKE) $@

gs-regular gs-medium gs-bold gs-italic gs-medium-italic gs-bold-italic:
	cd source && $(MAKE) $@

gst-regular gst-medium gst-bold gst-italic gst-medium-italic gst-bold-italic:
	cd source && $(MAKE) $@

gs-vf-upright gs-vf-italic:
	cd source && $(MAKE) $@

gs-ufo2glyphs:
	cd source && $(MAKE) $@

# ------------------------------
# Build dependency management
# ------------------------------
# setup creates a Python 3 virtual environment directory
setup:
	mkdir -p "$(VENV_DIR)"
	python3 -m venv "$(VENV_DIR)"
	"$(VENV_DIR)/bin/pip" install --upgrade pip wheel setuptools
	"$(VENV_DIR)/bin/pip" install --no-deps -r requirements-dev.txt
	@echo "\n\nDependency versions installed in your venv are:\n"
	@$(MAKE) list-deps
	@echo "\n\nBuild fonts with 'make' or make targets for select font builds (see BUILD.md docs)."
	@echo "Remove the virtual environment directory with 'make clean'."

# sync-deps syncs updated build dependencies in an existing virtual environment
# installing and uninstalling packages as (re)defined in the requirements.txt file
sync-deps:
	"$(VENV_DIR)/bin/pip" install -r requirements.txt

# list-deps displays venv installed dependencies
list-deps:
	@"$(VENV_DIR)/bin/pip" list

# [MAINTAINER ONLY TARGET]
# update-deps updates the requirements.txt file with new releases of Python build dependencies
# Note: the `pip-compile` tool is from the https://github.com/jazzband/pip-tools package
update-deps:
	pip-compile -U

# ------------------------------
# Testing
# ------------------------------

test-fb: test-fb-static test-fb-vf

test-fb-static:
	@echo "========================================================="
	@echo " fontbakery v`fontbakery --version` static font checks"
	@echo "========================================================="
	fontbakery check-profile --auto-jobs -C --loglevel WARN qa/check-googlesans.py $(STATIC_BUILD_DIR)/*.ttf
	fontbakery check-profile --auto-jobs -C --loglevel WARN qa/check-fea.py $(STATIC_BUILD_DIR)/*.ttf
	fontbakery check-profile --auto-jobs -C --loglevel WARN qa/check-charset.py $(STATIC_BUILD_DIR)/*.ttf

test-fb-vf:
	@echo "========================================================="
	@echo " fontbakery v`fontbakery --version` variable font checks"
	@echo "========================================================="
	fontbakery check-profile --auto-jobs -C --loglevel WARN qa/check-googlesans.py $(VARIABLE_BUILD_DIR)/*.ttf
	fontbakery check-profile --auto-jobs -C --loglevel WARN qa/check-fea.py $(VARIABLE_BUILD_DIR)/*.ttf
	fontbakery check-profile --auto-jobs -C --loglevel WARN qa/check-charset.py $(VARIABLE_BUILD_DIR)/*.ttf

update-glyphset-defs:
	python3 scripts/gs-update-glyphset-qa-files.py

# ------------------------------
# Python source formatting
# ------------------------------
black:
	black --line-length 90 scripts/*.py qa/*.py

# --------------------------------------
# Glyphs source formatting/normalization
# --------------------------------------
glyphs-norm:
	python3 scripts/gs-glyphs-norm.py source/GoogleSans/*.glyphs


# -------------------------------------
# Release targets
# -------------------------------------

# METADATA.pb file gen for Fonts API configuration
metadata:
	cd metadata && python metadata-builder.py

.PHONY: all \
black \
clean clean-builds clean-ufo\
gs-static gs-vf \
gs-regular gs-italic gs-medium gs-medium-italic gs-bold gs-bold-italic \
gst-regular gst-italic gst-medium gst-medium-italic gst-bold gst-bold-italic \
gs-vf-upright gs-vf-italic \
setup update-deps sync-deps list-deps \
test-fb test-fb-static-expert test-fb-vf-expert \
metadata

# Disable built-in rules to speed up source globbing.
MAKEFLAGS += --no-builtin-rules
.SUFFIXES:
