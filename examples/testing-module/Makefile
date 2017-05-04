CMD=python -m avocado run --filter-by-tags=-WIP
TESTS=$(shell ls *.py *.sh)
export MTF_REMOTE_REPOS=yes
export MTF_DO_NOT_CLEANUP=yes

check-docker:
	MODULE=docker $(CMD) $(TESTS)
	@true

check-rpm:
	MODULE=nspawn $(CMD) $(TESTS)
	@true

check-minimal-config-docker:
	MODULE=docker CONFIG=./minimal.yaml $(CMD) $(TESTS)
	@true

check-minimal-config-rpm:
	MODULE=nspawn CONFIG=./minimal.yaml $(CMD) $(TESTS)
	@true

check-behave-docker:
	cd ../memcached-behave; MODULE=docker behave
	@true

check-multihost-testing:
	cd ../multios_testing; DEBUG=yes MTF_DISABLE_MODULE=yes $(CMD) *.py
	@true

check-run-them-pdc-baseruntime:
	../../tools/run-them.sh base-runtime base-runtime-master-20170502071613 pdc
	@true

check-run-them-pdc-testmodule:
	../../tools/run-them.sh testmodule testmodule-f26-20170502202658 pdc
	@true

check-run-them-fedmsg-testmodule:
	../../tools/run-them.sh testmodule ../../tools/example_message_module.yaml fedmsg
	@true



check: check-rpm check-docker check-minimal-config-rpm

all: check

.PHONY: all
