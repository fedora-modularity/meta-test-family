export MTF_REMOTE_REPOS=yes
export DEBUG=yes
export MODULE=docker

prepare-docker:
	 dnf -y install pytest python2-case
	 mtf-env-set

check-nosetest: prepare-docker
	nosetests

check-unittest: prepare-docker
	python -m unittest example_unittest

check-pytest: prepare-docker
	pytest -q example_pytest.py
