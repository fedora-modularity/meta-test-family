PYTHONSITE=/usr/lib/python2.7/site-packages

all: check

integrationtests: install
	cd examples/general-component/tests; tmet-agregator | tee | grep 64
	cd examples/general-component/tests; tmet-agregator | tee | grep 64
	cd examples/general-component/tests; tmet-filter
	cd examples/general-component/tests; tmet-filter | grep 'sanity/generaltest.py'
	cd examples/general-component/tests; tmet-filter -b generic | grep 'sanity/generaltest.py'
	cd examples/general-component/tests; tmet-filter -b generic | grep meta-test-family.git
	cd examples/general-component/tests; tmet-filter -b generic | grep fedora_specific
	cd examples/general-component/tests; tmet-filter -b generic -t nonsense | grep -v fedora_specific
	cd examples/general-component/tests; tmet-filter -b generic -t nonsense | grep -v meta-test-family.git
	cd examples/general-component/tests; tmet-filter -b generic -t tag1 | grep fedora_specific
	cd examples/general-component/tests; tmet-filter -b generic -t tag1 | grep -v meta-test-family.git
	cd examples/general-component/tests; tmet-filter -b generic -t optional | grep meta-test-family.git
	cd examples/general-component/tests; tmet-filter -b generic -t optional | grep -v fedora_specific
	cd examples/general-component/tests; tmet-filter -b generic | grep downloaded_test.py
	cd examples/general-component/tests; tmet-filter -b generic | grep downloaded_git/tests/sanity1.py

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