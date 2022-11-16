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

PYTHON3 ?= python3

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
	. "$(VENV_DIR)/bin/activate" && cd source && $(MAKE) $@

gs-regular gs-medium gs-bold gs-italic gs-medium-italic gs-bold-italic:
	. "$(VENV_DIR)/bin/activate" && cd source && $(MAKE) $@

gst-regular gst-medium gst-bold gst-italic gst-medium-italic gst-bold-italic:
	. "$(VENV_DIR)/bin/activate" && cd source && $(MAKE) $@

gs-vf-upright gs-vf-italic:
	. "$(VENV_DIR)/bin/activate" && cd source && $(MAKE) $@

gs-ufo2glyphs:
	. "$(VENV_DIR)/bin/activate" && cd source && $(MAKE) $@

# ------------------------------
# Build dependency management
# ------------------------------
# setup creates a Python 3 virtual environment directory
setup:
	mkdir -p "$(VENV_DIR)"
	$(PYTHON3) -m venv "$(VENV_DIR)"
	@$(MAKE) sync-deps
	@$(MAKE) list-deps

	@echo "\n\nBuild fonts with 'make' or make targets for select font builds (see BUILD.md docs)."
	@echo "Remove the virtual environment directory with 'make clean'."

# sync-deps syncs updated build dependencies in an existing virtual environment
# installing and uninstalling packages as (re)defined in the requirements.txt file
sync-deps:
	"$(VENV_DIR)/bin/pip" install --quiet --upgrade pip wheel setuptools
	"$(VENV_DIR)/bin/pip" install --quiet -r requirements-dev.txt

# list-deps displays venv installed dependencies
list-deps:
	@echo "\n\nDependency versions installed in your general purpose venv are:\n"
	@"$(VENV_DIR)/bin/pip" list


# [MAINTAINER ONLY TARGET]
# update-deps updates the requirements.txt file with new releases of Python build dependencies
# Note: the `pip-compile` tool is from the https://github.com/jazzband/pip-tools package
update-deps:
	@"$(VENV_DIR)/bin/pip" install --upgrade pip-tools
	@"$(VENV_DIR)/bin/pip-compile" -U requirements-dev.txt -o requirements.txt

# ------------------------------
# Testing
# ------------------------------

test-fb: test-fb-static test-fb-vf

test-fb-static:
	@echo "========================================================="
	@echo " fontbakery v`"$(VENV_DIR)/bin/fontbakery" --version` static font checks"
	@echo "========================================================="
	"$(VENV_DIR)/bin/fontbakery" check-profile --auto-jobs --order "*check" -C --loglevel WARN qa/check-googlesans.py $(STATIC_BUILD_DIR)/*.ttf
	"$(VENV_DIR)/bin/fontbakery" check-profile --auto-jobs --order "*check" -C --loglevel WARN qa/check-fea.py $(STATIC_BUILD_DIR)/*.ttf
	"$(VENV_DIR)/bin/fontbakery" check-profile --auto-jobs --order "*check" -C --loglevel WARN qa/check-charset.py $(STATIC_BUILD_DIR)/*.ttf

test-fb-vf:
	@echo "========================================================="
	@echo " fontbakery v`"$(VENV_DIR)/bin/fontbakery" --version` variable font checks"
	@echo "========================================================="
	"$(VENV_DIR)/bin/fontbakery" check-profile --auto-jobs --order "*check" -C --loglevel WARN qa/check-googlesans.py $(VARIABLE_BUILD_DIR)/*.ttf
	"$(VENV_DIR)/bin/fontbakery" check-profile --auto-jobs --order "*check" -C --loglevel WARN qa/check-fea.py $(VARIABLE_BUILD_DIR)/*.ttf
	"$(VENV_DIR)/bin/fontbakery" check-profile --auto-jobs --order "*check" -C --loglevel WARN qa/check-charset.py $(VARIABLE_BUILD_DIR)/*.ttf

update-glyphset-defs:
	"$(VENV_DIR)/bin/python" scripts/gs-update-glyphset-qa-files.py

# ------------------------------
# Python source formatting
# ------------------------------
black:
	"$(VENV_DIR)/bin/black" --line-length 90 scripts/*.py qa/*.py

# --------------------------------------
# Glyphs source formatting/normalization
# --------------------------------------
glyphs-norm:
	"$(VENV_DIR)/bin/python" scripts/gs-glyphs-norm.py source/GoogleSans/*.glyphs


# -------------------------------------
# Release targets
# -------------------------------------

# METADATA.pb file gen for Fonts API configuration
metadata:
	cd metadata && "$(VENV_DIR)/bin/python" metadata-builder.py

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
