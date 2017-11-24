test:
	avocado run example1.py
	rm -rf /tmp/dddd1
	REPOS=http://ftp.fi.muni.cz/pub/linux/centos/7/os/x86_64/ avocado run example1.py
	rm -rf /tmp/dddd1

all: test

.PHONY: all