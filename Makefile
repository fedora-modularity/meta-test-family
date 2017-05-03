NAME=moduleframework
INSTALLPATH=/usr/share/$(NAME)
PYTHONSITE=/usr/lib/python2.7/site-packages

all: install check

check: clean
	./run-tests

.PHONY: clean

clean:
	@python setup.py clean
	rm -f MANIFEST
	rm -rf build/html
	rm -fv */generated.py
	find . -\( -name 'generated.py' -o -name "*.pyc" -o -name '*.pyo' -o -name "*~" -\) -delete

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
	@echo " test                    run tests/run_tests.py"
	@echo " html                    create HTML documentation"
