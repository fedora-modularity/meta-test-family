CMD=python -m avocado run --filter-by-tags=-WIP *.py *.sh

check-docker:
	MODULE=docker $(CMD)

check-rpm:
	MODULE=rpm $(CMD)

check: check-rpm

all: check
