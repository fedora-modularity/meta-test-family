NAME=moduleframework
INSTALLPATH=/usr/share/$(NAME)
PYTHONSITE=/usr/lib/python2.7/site-packages

all: install check

check:
	make -C examples/testing-module check

travis:
	make -C examples/testing-module travis

.PHONY: clean

clean:
	@python setup.py clean
	git clean -fd
	rm -rf build/html

install: clean
	@python setup.py install

source: clean
	@python setup.py sdist

html:
	make -f Makefile.docs html

man:
	make -f Makefile.docs man

help:
	@echo "Usage: make <target>"
	@echo
	@echo "Available targets are:"
	@echo " help                    show this text"
	@echo " clean                   remove python bytecode and temp files"
	@echo " install                 install program on current system"
	@echo " source                  create source tarball"
	@echo " check                   run examples/testing_module check target in Makefile"
	@echo " html                    create HTML documentation"

