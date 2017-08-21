CMD=avocado run --filter-by-tags=-WIP
TESTS=$(shell ls *.py *.sh ../../tools/modulelint/*.py)
export MTF_REMOTE_REPOS=yes
export DEBUG=yes
export DOCKERFILE=./Dockerfile

prepare-nspawn:
	MODULE=nspawn mtf-env-set

prepare-docker:
	MODULE=docker mtf-env-set

check-docker: prepare-docker
	MODULE=docker CONFIG=./fullconfig.yaml $(CMD) $(TESTS)
	@true

check-minimal-config-docker: prepare-docker
	MODULE=docker $(CMD) $(TESTS)
	@true


check-rpm: prepare-nspawn
	MODULE=nspawn CONFIG=./fullconfig.yaml $(CMD) $(TESTS)
	@true

check-minimal-config-rpm: prepare-nspawn
	MODULE=nspawn $(CMD) $(TESTS)
	@true

check-behave-docker: prepare-docker
	cd ../memcached-behave; MODULE=docker behave
	@true

check-multihost-testing: prepare-nspawn
	cd ../multios_testing; MTF_DISABLE_MODULE=yes $(CMD) *.py
	@true

check-run-them-pdc-baseruntime: prepare-nspawn
	../../tools/run-them.sh base-runtime base-runtime-f26-20170504201340 pdc
	@true

check-run-them-pdc-testmodule: prepare-nspawn
	../../tools/run-them.sh testmodule testmodule-master-20170413142055 pdc
	@true

check-run-them-fedmsg-testmodule: prepare-nspawn
	../../tools/run-them.sh testmodule ../../tools/example_message_module.yaml fedmsg
	@true

check-exceptions: prepare-nspawn
	MODULEMDURL=XXX  MODULE=nspawn $(CMD) simpleTest.py  | grep 'raise ConfigExc' >/dev/null
	@true

travis:
	MODULE=docker $(CMD) $(TESTS)

check: check-docker

all: check

.PHONY: all
