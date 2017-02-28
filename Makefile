NAME=moduleframework
INSTALLPATH=/usr/share/$(NAME)
PYTHONSITE=/usr/lib/python2.7/site-packages

check: clean
	./run-tests all

.PHONY: clean

clean:
	rm -fv */*.pyc */generated.py

install: clean
	
	mkdir -p $(INSTALLPATH)/tools
	cp base/moduleframework.py $(INSTALLPATH)/__init__.py
	cp base/modulelint.py $(INSTALLPATH)/tools
	cp base/generator.py $(INSTALLPATH)/tools
	cp base/general_multiplex.yaml $(INSTALLPATH)/tools
	cp base/example-config.yaml $(INSTALLPATH)/tools
	cp base/bashhelper.py $(INSTALLPATH)/tools
	ln -sf $(INSTALLPATH) $(PYTHONSITE)/$(NAME)
	ln -sf $(INSTALLPATH)/tools/bashhelper.py /usr/bin/moduleframework-cmd

all: install check
