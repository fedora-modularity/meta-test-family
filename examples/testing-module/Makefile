CMD=python -m avocado run --show-job-log --filter-by-tags=-WIP *.py *.sh
export MTF_REMOTE_REPOS=yes

check-docker:
	MODULE=docker $(CMD)

check-rpm:
	MODULE=nspawn $(CMD)

check-minimal-config-docker:
	MODULE=docker CONFIG=./minimal.yaml $(CMD)

check-minimal-config-rpm:
	MODULE=nspawn CONFIG=./minimal.yaml $(CMD)

check-behave-docker:
	cd ../memcached-behave; MODULE=docker behave

check: check-rpm

all: check
