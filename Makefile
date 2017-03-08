NAME=moduleframework
INSTALLPATH=/usr/share/$(NAME)
PYTHONSITE=/usr/lib/python2.7/site-packages

check: clean
	./run-tests

.PHONY: clean

clean:
	@python setup.py clean
	rm -f MANIFEST
	rm -rf build/html
	rm -fv */generated.py
	find . -\( -name "*.pyc" -o -name '*.pyo' -o -name "*~" -\) -delete

install: clean
	@python setup.py install

source: clean
	@python setup.py sdist

all: install check
