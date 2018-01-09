PYTHONSITE=/usr/lib/python2.7/site-packages

all: check

integrationtests: install
	cd examples/general-component/tests; tmet-agregator | tee | grep 64
	cd examples/general-component/tests; tmet-agregator | tee | grep 64
	cd examples/general-component/tests; tmet-filter
	cd examples/general-component/tests; tmet-filter | tee | grep 'sanity/generaltest.py'
	cd examples/general-component/tests; tmet-filter -b generic | tee | grep 'sanity/generaltest.py'
	cd examples/general-component/tests; tmet-filter -b generic | tee | grep meta-test-family.git
	cd examples/general-component/tests; tmet-filter -b generic | tee | grep fedora_specific
	cd examples/general-component/tests; tmet-filter -b generic -t nonsense | tee | grep -v fedora_specific
	cd examples/general-component/tests; tmet-filter -b generic -t nonsense | tee | grep -v meta-test-family.git
	cd examples/general-component/tests; tmet-filter -b generic -t tag1 | tee | grep fedora_specific
	cd examples/general-component/tests; tmet-filter -b generic -t tag1 | tee | grep -v meta-test-family.git
	cd examples/general-component/tests; tmet-filter -b generic -t optional | tee | grep meta-test-family.git
	cd examples/general-component/tests; tmet-filter -b generic -t optional | tee | grep -v fedora_specific
	cd examples/general-component/tests; tmet-filter -b generic | tee | grep downloaded_test.py
	cd examples/general-component/tests; tmet-filter -b generic | tee | grep downloaded_git/tests/sanity1.py

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