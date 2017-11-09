PYTHONSITE=/usr/lib/python2.7/site-packages

all: check

integrationtests: install
	cd examples/general-component/tests; tmet-agregator
	cd examples/general-component/tests; tmet-agregator |grep -o 60
	cd examples/general-component/tests; tmet-filter
	cd examples/general-component/tests; tmet-filter | grep 'sanity/generaltest.py'

unittests:
	py.test tmet/selftests.py

check: install unittests integrationtests

clean:
	pip uninstall .

install: clean
	pip install -U .

source: clean
	@python setup.py sdist

.PHONY: check