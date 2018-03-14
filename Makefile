NAME=moduleframework
INSTALLPATH=/usr/share/$(NAME)
PYTHONSITE=/usr/lib/python2.7/site-packages

all: install_pip check

check:
	make -C examples/testing-module check

check-linter:
	@# don't use $(shell ) -- it messes out output
	cd examples/linter/tools && PYTHONPATH=${PWD} MODULE=docker ${PWD}/${NAME}/mtf_scheduler.py -l
	cd examples/linter/rhscl-postgresql && PYTHONPATH=${PWD} MODULE=docker ${PWD}/${NAME}/mtf_scheduler.py -l
	cd examples/linter/rhscl-nginx && PYTHONPATH=${PWD} MODULE=docker ${PWD}/${NAME}/mtf_scheduler.py -l
	cd examples/linter/f26-etcd && PYTHONPATH=${PWD} MODULE=docker ${PWD}/${NAME}/mtf_scheduler.py -l
	cd examples/linter/f26-flannel && PYTHONPATH=${PWD} MODULE=docker ${PWD}/${NAME}/mtf_scheduler.py -l

travis:
	make -C examples/testing-module travis
	cd examples/linter/tools && PYTHONPATH=${PWD} MODULE=docker mtf -l

check-mtf-default-config-loader:
	mtf -l && false || true
	mtf -l --url fedora && false || true
	mtf -l --url fedora --module docker


.PHONY: clean

clean_pip:
	pip uninstall .
	rm -rf build/* dist/*


install_pip: clean_pip
	pip install -U .

clean:
	@python setup.py clean
	rm -rf build/* dist/*

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

