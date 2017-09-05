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

check-run-them-pdc-baseruntime: prepare-nspawn
	../../tools/run-them.sh base-runtime base-runtime-f26-20170504201340 pdc

check-run-them-pdc-testmodule: prepare-nspawn
	../../tools/run-them.sh testmodule testmodule-master-20170413142055 pdc

check-run-them-fedmsg-testmodule: prepare-nspawn
	../../tools/run-them.sh testmodule ../../tools/example_message_module.yaml fedmsg

check-exceptions: prepare-nspawn
	MODULEMDURL=NOT_VALID_URL MODULE=docker $(CMD) --show-job-log simpleTest.py |& grep 'raise ConfigExc'

check-pure-rpm: prepare-nspawn
	CONFIG=config-pure-rpm.yaml MODULE=nspawn $(CMD) $(SIMPLE)

check-pure-docker: prepare-docker
	CONFIG=config-pure-docker.yaml MODULE=docker $(CMD) $(SIMPLE)

travis:
	MODULE=docker $(CMD) $(TESTS)

check: check-docker

all: check

.PHONY: all
