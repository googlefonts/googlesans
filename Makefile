all: gs

gs gs-static gs-vf:
	cd source && $(MAKE) $@

.PHONY: all gs gs-static gs-vf