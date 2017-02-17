
INSTALLPATH=/usr/lib/python2.7/site-packages/moduleframework

check:
	./run-tests

.PHONY: clean

clean:
	rm -fv */*.pyc

install: clean
	mkdir -p $(INSTALLPATH)/tests
	cp base/moduleframework.py $(INSTALLPATH)/__init__.py
	cp base/modulelint.py $(INSTALLPATH)/tests/__init__.py

all: install check
