TESTS=$(shell ls *.py)

check:
	# run modulelint explicitly in example
	#mtf -l
	mtf $(TESTS)

check-python-3.5:
	MODULE=docker-python-35 mtf $(TESTS)

all: check

.PHONY: all
