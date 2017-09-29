TESTS=simpleTest.py
TESTS_GENERAL=usageTest.py
MINIMAL_CONFIG=/usr/share/moduleframework/docs/example-config-minimal.yaml

check: check-2.7

check-2.7:
	# run modulelint explicitly in example
	mtf -l
	mtf $(TESTS)

check-python-3.5:
	MODULE=docker-python-35 mtf $(TESTS)

check-usage:
	CONFIG=$(MINIMAL_CONFIG) URL=docker=centos/python-35-centos7 MODULE=docker mtf $(TESTS_GENERAL)
	CONFIG=$(MINIMAL_CONFIG) URL=docker=centos/python-27-centos7 MODULE=docker mtf $(TESTS_GENERAL)

all: check

.PHONY: all
