TESTS=simpleTest.py
TESTS_GENERAL=usageTest.py
MINIMAL_CONFIG=/usr/share/moduleframework/docs/example-config-minimal.yaml

prepare:
	mtf-env-set

check: check-python-3.5 check-python-2.7

check-python-2.7: prepare
	# run modulelint explicitly in examples if you want
	# mtf -l
	mtf $(TESTS)

check-python-3.5: prepare
	MODULE=docker-python-35 mtf $(TESTS)

check-usage-minimal:
	CONFIG=$(MINIMAL_CONFIG) URL=docker=centos/python-35-centos7 MODULE=docker mtf $(TESTS_GENERAL)
	CONFIG=$(MINIMAL_CONFIG) URL=docker=centos/python-27-centos7 MODULE=docker mtf $(TESTS_GENERAL)

all: check

.PHONY: all
