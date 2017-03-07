NAME=moduleframework
INSTALLPATH=/usr/share/$(NAME)
PYTHONSITE=/usr/lib/python2.7/site-packages

check: clean
	./run-tests

.PHONY: clean

clean:
	rm -fv */*.pyc */generated.py

install: clean
	mkdir -p $(INSTALLPATH)
	mkdir -p $(PYTHONSITE)/$(NAME)
	cp base/moduleframework.py $(INSTALLPATH)
	ln -sf $(INSTALLPATH)/moduleframework.py $(PYTHONSITE)/$(NAME)/__init__.py
	
	mkdir -p $(INSTALLPATH)/tools
	cp base/modulelint.py $(INSTALLPATH)/tools
	cp base/generator.py $(INSTALLPATH)/tools
	cp base/general_multiplex.yaml $(INSTALLPATH)/tools
	cp base/bashhelper.py $(INSTALLPATH)/tools
	ln -sf $(INSTALLPATH)/tools/bashhelper.py /usr/bin/moduleframework-cmd
	
	mkdir -p $(INSTALLPATH)/docs
	cp docs/example-config.yaml $(INSTALLPATH)/docs
	cp docs/howtowriteyamlconf.md $(INSTALLPATH)/docs

all: install check
