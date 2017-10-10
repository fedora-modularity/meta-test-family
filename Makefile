NAME=moduleframework
INSTALLPATH=/usr/share/$(NAME)
PYTHONSITE=/usr/lib/python2.7/site-packages

all: install check

check:
	make -C examples/testing-module check

check-linter:
	@# don't use $(shell ) -- it messes out output
	cd examples/linter/tools && PYTHONPATH=${PWD} MODULE=docker ${PWD}/tools/mtf -l
	cd examples/linter/rhscl-postgresql && PYTHONPATH=${PWD} MODULE=docker ${PWD}/tools/mtf -l
	cd examples/linter/rhscl-nginx && PYTHONPATH=${PWD} MODULE=docker ${PWD}/tools/mtf -l
	cd examples/linter/f26-etcd && PYTHONPATH=${PWD} MODULE=docker ${PWD}/tools/mtf -l
	cd examples/linter/f26-flannel && PYTHONPATH=${PWD} MODULE=docker ${PWD}/tools/mtf -l

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

