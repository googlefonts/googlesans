FONT_BUILD_DIR="build/GoogleSans"
MASTER_UFO_DIR="$(FONT_BUILD_DIR)/master_ufo"
INSTANCE_UFO_DIR="$(FONT_BUILD_DIR)/instance_ufo"

all: gs-static gs-vf

clean:
	rm -rf $(MASTER_UFO_DIR)
	rm -rf $(INSTANCE_UFO_DIR)

gs-static gs-vf:
	cd source && $(MAKE) $@

gs-regular gs-medium gs-bold gs-italic gs-medium-italic gs-bold-italic:
	cd source && $(MAKE) $@

gst-regular gst-medium gst-bold gst-italic gst-medium-italic gst-bold-italic:
	cd source && $(MAKE) $@

gs-vf-upright gs-vf-italic:
	cd source && $(MAKE) $@

.PHONY: all \
clean \
gs-static gs-vf \
gs-regular gs-italic gs-medium gs-medium-italic gs-bold gs-bold-italic \
gst-regular gst-italic gst-medium gst-medium-italic gst-bold gst-bold-italic \
gs-vf-upright gs-vf-italic \
build-designspace-upright build-designspace-italic