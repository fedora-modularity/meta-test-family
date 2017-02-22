NAME=moduleframework
INSTALLPATH=/usr/share/$(NAME)
PYTHONSITE=/usr/lib/python2.7/site-packages

check: clean
	./run-tests

.PHONY: clean

clean:
	rm -fv */*.pyc */generated.py

install: clean
	pip install PyYAML avocado-framework
	
	mkdir -p $(INSTALLPATH)/tools
	cp base/moduleframework.py $(INSTALLPATH)/__init__.py
	cp base/modulelint.py $(INSTALLPATH)/tools
	cp base/generator.py $(INSTALLPATH)/tools
	cp base/general_multiplex.yaml $(INSTALLPATH)/tools
	cp base/example-config.yaml $(INSTALLPATH)/tools
	ln -sf $(INSTALLPATH) $(PYTHONSITE)/$(NAME)

all: install check
