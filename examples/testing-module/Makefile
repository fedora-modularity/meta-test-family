CMD=avocado run
TESTS=$(shell ls *.py *.sh ../../moduleframework/tools/*.py)
SIMPLE=simpleTest.py
export MTF_REMOTE_REPOS=yes
export DEBUG=yes
export DOCKERFILE=./Dockerfile

prepare-nspawn:
	MODULE=nspawn mtf-env-set

prepare-docker:
	MODULE=docker mtf-env-set

check-docker: prepare-docker
	MODULE=docker CONFIG=./fullconfig.yaml $(CMD) $(TESTS)

check-minimal-config-docker: prepare-docker
	MODULE=docker $(CMD) $(TESTS)

check-rpm: prepare-nspawn
	MODULE=nspawn CONFIG=./fullconfig.yaml $(CMD) $(TESTS)

check-minimal-config-rpm: prepare-nspawn
	MODULE=nspawn $(CMD) $(TESTS)

check-behave-docker: prepare-docker
	cd ../memcached-behave; MODULE=docker behave

check-multihost-testing:
	cd ../multios_testing; MODULE=nspawn mtf-env-set
	cd ../multios_testing; MTF_DISABLE_MODULE=yes $(CMD) *.py

check-run-them-pdc-testmodule: prepare-nspawn
	../../tools/run-them.sh testmodule testmodule-master-20170413142055 pdc

check-run-them-pdc-testmodule-taskotron: prepare-nspawn
	MTF_REMOTE_REPOS= DOCKERFILE= /usr/share/moduleframework/tools/run-them.sh testmodule testmodule-master-20170926102903 pdc

check-run-them-fedmsg-testmodule: prepare-nspawn
	../../tools/run-them.sh testmodule ../../tools/example_message_module.yaml fedmsg

check-exceptions: prepare-docker
	URL=NOT_VALID_URL MODULE=docker $(CMD) --show-job-log simpleTest.py | grep 'raise CmdError'
	CONFIG=NOT_VALID_CONFIG MODULE=docker $(CMD) --show-job-log simpleTest.py | grep 'raise ConfigExc'

check-pure-rpm: prepare-nspawn
	CONFIG=config-pure-rpm.yaml MODULE=nspawn $(CMD) $(SIMPLE)

check-real-rpm-destructive:
	CONFIG=config-pure-rpm.yaml MODULE=rpm $(CMD) $(SIMPLE)

check-pure-docker: prepare-docker
	CONFIG=config-pure-docker.yaml MODULE=docker $(CMD) $(SIMPLE)

check-default-config:
	cd ..; MODULE=docker URL=fedora mtf-env-set
	cd ..; MODULE=docker URL=fedora $(CMD) testing-module/$(SIMPLE)

check-inheritance: prepare-docker
	CONFIG=config-inheritance-docker.yaml MODULE=dockerinherited URL=fedora $(CMD) $(SIMPLE)

check-docker-scl-multi-travis:
	cd ../rhscl_maria; MODULE=docker $(CMD) *.py

check-docker-scl-multi:
	cd ../rhscl_maria; MODULE=docker mtf-env-set
	cd ../rhscl_maria; MODULE=docker $(CMD) *.py


travis:
	MODULE=docker $(CMD) $(TESTS)

check-test-mtf-bin-modulelint: prepare-docker
	MODULE=docker mtf -l

check-memcached-both: prepare-docker prepare-nspawn
	cd ../memcached; MODULE=docker $(CMD) sanity1.py
	cd ../memcached; MODULE=nspawn $(CMD) sanity1.py



check: check-docker

all: check

.PHONY: all
