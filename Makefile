NAME=moduleframework
INSTALLPATH=/usr/share/$(NAME)
PYTHONSITE=/usr/lib/python2.7/site-packages

check:
	./run-tests

.PHONY: clean

clean:
	rm -fv */*.pyc

install: clean
	mkdir -p $(INSTALLPATH)
	
	cp base/moduleframework.py $(INSTALLPATH)/__init__.py
	cp base/modulelint.py $(INSTALLPATH)/
	ln -sf $(INSTALLPATH) $(PYTHONSITE)/$(NAME)

all: install check
