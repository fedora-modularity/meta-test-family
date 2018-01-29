CMD=mtf
TESTS=$(shell ls *.py *.sh ../../moduleframework/tests/generic/*.py ../../moduleframework/tests/static/*.py)
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
	URL=NOT_VALID_URL MODULE=docker $(CMD) --show-job-log simpleTest.py 2>&1 | grep 'raise CmdError'
	CONFIG=NOT_VALID_CONFIG MODULE=docker $(CMD) --show-job-log simpleTest.py 2>&1 | grep 'raise ConfigExc'

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

check-openshift-memcached:
	sudo oc cluster up
	cd ../openshift-sample; MODULE=openshift DEBUG=yes OPENSHIFT_USER=developer OPENSHIFT_PASSWORD=developer $(CMD) sanity1.py
	sudo oc cluster down

check-minimal-config-rpm-noenvvar: prepare-nspawn
	MTF_REMOTE_REPOS= DOCKERFILE= MODULE=nspawn $(CMD) $(TESTS)

check-mtf-init:
	$(eval TEMPDIR := $(shell mktemp -d))
	cd $(TEMPDIR); mtf-init --name NAME1 --container docker.io/modularitycontainers/memcached
	cd $(TEMPDIR); grep 'class Smoke1' test.py ; grep 'default_module' config.yaml; sudo mtf test.py
	rm -rf "$(TEMPDIR)"

check-mtf-linters:
	cd ../mtf-linters; MODULE=docker mtf-env-set
	cd ../mtf-linters; MODULE=docker $(CMD) -l

check-mtf-list:
	$(CMD) --action=list

check-mtf-options:
	$(eval MYPWD := $(shell pwd))
	$(eval TEMPDIR := $(shell mktemp -d))
	cd $(TEMPDIR); MODULE=docker $(CMD)  --module=nspawn --debug --config=$(MYPWD)/config.yaml $(MYPWD)/simpleTest.py &> log
	cd $(TEMPDIR); grep 'MODULE=docker' log
	rm -rf "$(TEMPDIR)"

check-mtf-pdc-module-info-reader:
	mtf-pdc-module-info-reader -r testmodule-master-20170926102903
	mtf-pdc-module-info-reader -r testmodule-master-20170926102903 --commit | grep 9107dcf53f6201a01b8c8d18493aae0175bcfb19
	mtf-pdc-module-info-reader -r testmodule-master-20170926102903 | grep 'MODULE=nspawn'
	mtf-pdc-module-info-reader -r testmodule-master-20170926102903 | grep 'MODULEMDURL=file:/'
	mtf-pdc-module-info-reader -r testmodule-master-20170926102903 | grep 'URL=https://koj'

check-mtf-metadata:
	make -C ../test_metadata_loader test

check-memcached-metadata-loader: prepare-docker
	make -C ../memcached test


check: check-docker

all: check

.PHONY: all
