CMD=python -m avocado run --filter-by-tags=-WIP *.py *.sh

check-docker:
	MODULE=docker $(CMD)

check-rpm:
	MODULE=rpm $(CMD)

check-minimal-config-docker:
	MODULE=docker CONFIG=./minimal.yaml $(CMD)

check-minimal-config-rpm:
	MODULE=rpm CONFIG=./minimal.yaml $(CMD)

check-behave-docker:
	cd ../memcached-behave; MODULE=docker behave

check: check-rpm

all: check
