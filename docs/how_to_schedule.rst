Manual testing
=====================

- Scheduled on host machine
    - **docker, nspawn** `MODULE` type does not affect Host machine
    - **rpm** `MODULE` type test directly on host machine. It installs things there and may be **very dangerous**
- Intended for test debugging

modules dist-git integration
----------------------------

- **dist-git** - Create Makefile in top directory, what contains build target and test target dependant on build taret and set proper variables to that test target, template: https://github.com/container-images/container-image-template/
    - Example: https://github.com/container-images/container-image-template/blob/master/Makefile
    - Makefile like: `cd tests; MODULEMDURL=$(MODULEMDURL) MODULE=docker URL="docker=$(IMAGE_NAME)" make all`
    - inside `tests` directory cretates just simple Makefile like https://github.com/container-images/container-image-template/blob/master/tests/Makefile



Docker
-----------------------
- Test Subject: docker images, https://fedoraproject.org/wiki/Docker
- Scheduled as: `MODULE=docker avocado run  *.py modulelint/*.py`
    - or `MODULE=docker CONFIG=./minimal.yaml avocado run  *.py modulelint/*.py` when you use alternate configuration file
- Example targets: `check-docker, check-minimal-config-docker, check-behave-docker`
- Internal logic of testing
    - pull docker image
    - setup environment
    - start docker image via start section or default one (keep it running)
    - do test
    - cleanup enviroment
    - remove docker container

Nspanw
-----------------------
- Test Subject: rpm repository, inside systemd-nspawn virtualization https://www.freedesktop.org/software/systemd/man/systemd-nspawn.html
- Scheduled as: `MODULE=nspawn avocado run  *.py modulelint/*.py`
    - or `MODULE=nspawn CONFIG=./minimal.yaml avocado run  *.py modulelint/*.py` when you use alternate configuration file
- Example targets: `check-rpm, check-minimal-config-rpm`
- Internal logic of testing
    - install packages to `changeroot` with systemd
    - setup environment and `boot` nspawn machine (to keep it running)
    - start via start section or default one on *guest*
    - do test
    - cleanup enviroment
    - halt system and remove installed chroot dir


Rpm
-----------------------
- **Destructive**  and **WIP**
- Test Subject: rpm repository, bare metal, intended for testing packages directly on machine (without any module)
- Scheduled as: `MODULE=rpm avocado run  *.py modulelint/*.py`
    - or `MODULE=rpm avocado run  *.py modulelint/*.py` when you use alternate configuration file
- Example targets: `None` - cause changes on host
- Internal logic of testing
    - install packages to system
    - start via start section or default one
    - do test
    - cleanup enviroment if any

Multihost
-----------------------
- Test Subject: any of previous
- Could be used for general multihost testing not directly dependent on modules
- Scheduled as: `cd /usr/share/moduleframework/examples/multios_testing; MTF_DISABLE_MODULE=yes avocado run  *.py`
- Example targets: `check-multihost-testing`
- Internal logic of testing
    - could be same as previous ones that there is one *Host* and one  *Guest* machine what can cooperate togetger
    - Or it could be used for general multihost testing with *N* machines where *N>1* via use backends directly in setUp sections
        - see example of test: https://github.com/fedora-modularity/meta-test-family/blob/master/examples/multios_testing/sanityRealMultiHost.py
        - this example creates 3 machines *(using nspawn)* with various fedora versions and gather data.
