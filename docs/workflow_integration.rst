Workflow integration
============================

Testsuite of project
----------------------------
- Upstream **testsuite** for project located in `/usr/share/moduleframework/examples/testing-module/`
    - You can use it as an **inspiration** for your tests
    - It contains various types how to schedule tests
    - **CI** It contains info how it is scheduled in internal-ci or in taskotron or how to do
    - Examples of **Manual** running of tests on localhost.
    - Example how to run general **multi-host** tests
    - Every new feature should be covered here - by new Makefile target or by new test run inside every testing module


Taskotron Wokflow
----------------------------
- Production instance: https://taskotron.fedoraproject.org/resultsdb/results?testcases=dist.modularity-testing-framework
    - Trigerred fedmsg via **module-stream-version** string
    - Trigerred by **Module Build system** done message, list of all: https://apps.fedoraproject.org/datagrepper/raw?topic=org.fedoraproject.prod.mbs.module.state.change
    - There is general `runtask.yml` taskotron trigger: https://pagure.io/taskotron/task-modularity-testing-framework
        - There is just one for every module and it contains whole logic where to find tests for module.
        - Not needed to duplicate `runtash.yml` for each component. Scheduler is same (existing Makefile)
        - It run `tools/run-them.sh` script. It contains whole logic where are tests and how to find them.
    - **run-them.sh** script for taskotron
        - Test Subject: rpm repositories (tagged koji builds of packages) via `systemd-nspawn`
        - Located in: `/usr/share/moduleframework/tools/run-them.sh`
        - Scheduled as: `./run-them.sh testmodule testmodule-master-20170407121558 pdc`
        - Example targets: `check-run-them-pdc-testmodule, check-run-them-pdc-baseruntime`
        - Internal logic
            - Contact *PDC* (Product definition center) for info about module like `koji tags, moduleMD file`
            - Try dowload package from `modules` namespace in `dist-git` via `fedpkg clone`
                - checkout to proper version found by PDC (scmurl)
                - Try to find tests there ( if exist `Makefile` in `tests` directory)
            - If None: Try to find module dir in MTF project tests in `/usr/share/moduleframework/examples` directory
            - If None: Run at least general ModuleLinter (`/usr/share/moduleframework/tools/modulelint`) with general minimal config.yaml located in `docs` directory

Internal Jenkins Instance
----------------------------
- Production instance: `hidden`
    - Trigerred via `fedmsg file`
        - Used **tools/run-them.sh** script, for same behaviour as Taskotron
    - **run-them.sh** script for Jenkins based on whole fedmsg
        - Test Subject: Same as *Taskotron Workflow*
        - Located in: Same as *Taskotron Workflow*
        - Scheduled as: `run-them.sh testmodule /usr/share/moduleframework/tools/example_message_module.yaml fedmsg`
        - Example targets: `check-run-them-fedmsg-testmodule`
        - Internal logic
            - Same as *Taskotron Workflow*


Manual testing
----------------------------
- Scheduled on host machine
    - **docker, nspawn** `MODULE` type does not affect Host machine
    - **rpm** `MODULE` type test directly on host machine. It installs things there and may be **very dangerous**
- Intended for test debugging
- **dist-git:** - Create Makefile in top directory, what contains build target and test target dependant on build taret and set proper variables to that test target, template: https://github.com/container-images/container-image-template/
    - Example: https://github.com/container-images/container-image-template/blob/master/Makefile
    - Makefile like: `cd tests; MODULEMDURL=$(MODULEMDURL) MODULE=docker URL="docker=$(IMAGE_NAME)" make all`
    - inside `tests` directory cretates just simple Makefile like https://github.com/container-images/container-image-template/blob/master/tests/Makefile



Docker
~~~~~~~~~~~~~~~~~~~~~~
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
~~~~~~~~~~~~~~~~~~~~~~
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
~~~~~~~~~~~~~~~~~~~~~~
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
~~~~~~~~~~~~~~~~~~~~~~
- Test Subject: any of previous
- Could be used for general multihost testing not directly dependent on modules
- Scheduled as: `cd /usr/share/moduleframework/examples/multios_testing; MTF_DISABLE_MODULE=yes avocado run  *.py`
- Example targets: `check-multihost-testing`
- Internal logic of testing
    - could be same as previous ones that there is one *Host* and one  *Guest* machine what can cooperate togetger
    - Or it could be used for general multihost testing with *N* machines where *N>1* via use backends directly in setUp sections
        - see example of test: https://pagure.io/modularity-testing-framework/blob/master/f/examples/multios_testing/sanityRealMultiHost.py
        - this example creates 3 machines *(using nspawn)* with various fedora versions and gather data.

MTF - Levels of testing
==========================================

Component level testing
----------------------------
- **WIP**
- **Test Subject** - RPM packages build by koji
- See sections Manual testing - *Rpm* or *Multihost*
- MTF could be used for component level testing, it is **not primar purpose** of this project


Module level testing
----------------------------

- **Test Subject** - Module Build (rpm packages produced by MBS and tagged by koji or Docker container created manually or by OSBS or similar service)
- See sections *Docker* *Nspawn* testing
- **This is primar purpose of this framework**
    - tagged rpm packages are not final artifacts (Module Compose should be final artifact) - for now it supply Compose level testing
    - Docker image is final build artifacts

Compose level testing
----------------------------
- **WIP**
- **Test Subject:** Module compose (done by Pungi https://pagure.io/pungi-fedora)
- We are waiting for real module composes, what will be able to provide data about modules (modulemd files, repositories)
- It does not exist yet.
- There should be service for module builds on demand, not just composes for all modules together
- MTF is prepared for *Compose testing* somehow
- How to:
    - remove modulemd-url from config use COMPOSE  env variable or compose-url inside config.yaml.
    - it gets all data from compose info
    - Scheduled as: `MODULE=nspawn COMPOSEURL=https://kojipkgs.stg.fedoraproject.org/compose/branched/jkaluza/latest-Fedora-Modular-26/compose/base-runtime/x86_64/os/ avocado run *.py`

