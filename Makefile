PREFIX ?= $(HOME)/.local
INSTALL_PATH = $(DESTDIR)$(PREFIX)/share/nautilus-python/extensions
MODULES_PREFIX = nautilus_unicode_
all:

install:   $(patsubst $(MODULES_PREFIX)%.py,install-%,  $(notdir $(wildcard src/$(MODULES_PREFIX)*.py)))
uninstall: $(patsubst $(MODULES_PREFIX)%.py,uninstall-%,$(notdir $(wildcard $(INSTALL_PATH)/$(MODULES_PREFIX)*.py)))

pycache:
	python -m compileall src

clean:
	rm -rf src/__pycache__/ || true

install-%:
	install -dm755 $(INSTALL_PATH)/__pycache__/
	install -m755 src/$(MODULES_PREFIX)$*.py $(INSTALL_PATH)/
	test -f src/__pycache__/$(MODULES_PREFIX)$*.*.pyc && install -m755 src/__pycache__/$(MODULES_PREFIX)$*.*.pyc $(INSTALL_PATH)/__pycache__/ || true

uninstall-%:
	rm $(INSTALL_PATH)/$(MODULES_PREFIX)$*.py || true
	rm $(INSTALL_PATH)/__pycache__/$(MODULES_PREFIX)$*.*.pyc || true
