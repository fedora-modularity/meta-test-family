PYTHONSITE=/usr/lib/python2.7/site-packages

all: check

integrationtests: install
	cd examples/general-component/; tmet-agregator
	cd examples/general-component/; tmet-agregator |grep -o 50
	cd examples/general-component/; tmet-filter
	cd examples/general-component/; tmet-filter | grep -o 'generaltest.py'

unittests:
	pytest tmet/selftests.py

check: install unittests integrationtests

clean:
	pip uninstall .

install: clean
	pip install -U .

source: clean
	@python setup.py sdist

.PHONY: check