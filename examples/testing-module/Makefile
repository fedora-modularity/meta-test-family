CMD=avocado run --filter-by-tags=-WIP
TESTS=$(shell ls *.py *.sh modulelint/*.py)
export MTF_REMOTE_REPOS=yes
export DEBUG=yes
export DOCKERFILE=./Dockerfile

check-docker:
	MODULE=docker CONFIG=./fullconfig.yaml $(CMD) $(TESTS)
	@true

check-minimal-config-docker:
	MODULE=docker $(CMD) $(TESTS)
	@true


check-rpm:
	MODULE=nspawn CONFIG=./fullconfig.yaml $(CMD) $(TESTS)
	@true

check-minimal-config-rpm:
	MODULE=nspawn $(CMD) $(TESTS)
	@true

check-behave-docker:
	cd ../memcached-behave; MODULE=docker behave
	@true

check-multihost-testing:
	cd ../multios_testing; MTF_DISABLE_MODULE=yes $(CMD) *.py
	@true

check-run-them-pdc-baseruntime:
	../../tools/run-them.sh base-runtime base-runtime-f26-20170504201340 pdc
	@true

check-run-them-pdc-testmodule:
	../../tools/run-them.sh testmodule testmodule-master-20170413142055 pdc
	@true

check-run-them-fedmsg-testmodule:
	../../tools/run-them.sh testmodule ../../tools/example_message_module.yaml fedmsg
	@true

check-exceptions:
	MODULEMDURL=XXX  MODULE=nspawn $(CMD) --show-job-log simpleTest.py  | grep 'raise ConfigExc' >/dev/null
	@true



check: check-docker check-minimal-config-rpm check-run-them-pdc-testmodule

all: check

.PHONY: all
