PYTHONSITE=/usr/lib/python2.7/site-packages

all: check

check: install
	cd example-component/tests/; tmet-agregator
	cd example-component/tests/; tmet-agregator |grep -o 50
	cd example-component/tests/; tmet-filter
	cd example-component/tests/; tmet-filter | grep -o 'file://general/generaltest.py'

.PHONY: check

clean:
	pip uninstall .

install: clean
	pip install -U .

source: clean
	@python setup.py sdist
