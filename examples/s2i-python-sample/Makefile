TESTS=$(shell ls *.py)

check:
	# run modulelint explicitly in example
	#mtf -l
	mtf $(TESTS)

all: check

.PHONY: all
