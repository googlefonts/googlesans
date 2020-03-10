FONT_BUILD_DIR=build/GoogleSans
MASTER_UFO_DIR=$(FONT_BUILD_DIR)/master_ufo
INSTANCE_UFO_DIR=$(FONT_BUILD_DIR)/instance_ufo
VENV_DIR=.venv

all: gs-static gs-vf

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

# ------------------------------
# Compile
# ------------------------------

gs-static gs-vf:
	cd source && $(MAKE) $@

gs-regular gs-medium gs-bold gs-italic gs-medium-italic gs-bold-italic:
	cd source && $(MAKE) $@

gst-regular gst-medium gst-bold gst-italic gst-medium-italic gst-bold-italic:
	cd source && $(MAKE) $@

gs-vf-upright gs-vf-italic:
	cd source && $(MAKE) $@

# ------------------------------
# Build dependency management
# ------------------------------
# setup creates a Python 3 virtual environment directory
setup:
	mkdir -p "$(VENV_DIR)"
	python3 -m venv "$(VENV_DIR)"
	"$(VENV_DIR)/bin/pip" install --upgrade pip
	"$(VENV_DIR)/bin/pip" install -r requirements.txt
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


test-fb: test-fb-static test-fb-vf

test-fb-static:
	@echo "========================================================="
	@echo " fontbakery v`fontbakery --version` static font checks"
	@echo "========================================================="
	fontbakery check-profile -C --loglevel WARN qa/check-googlesans.py build/GoogleSans/static/*.ttf

test-fb-vf:
	@echo "========================================================="
	@echo " fontbakery v`fontbakery --version` variable font checks"
	@echo "========================================================="
	fontbakery check-profile -C --loglevel WARN qa/check-googlesans.py build/GoogleSans/variable/*.ttf


.PHONY: all \
clean \
gs-static gs-vf \
gs-regular gs-italic gs-medium gs-medium-italic gs-bold gs-bold-italic \
gst-regular gst-italic gst-medium gst-medium-italic gst-bold gst-bold-italic \
gs-vf-upright gs-vf-italic \
setup update-deps sync-deps list-deps \
test-fb test-fb-static test-fb-vf