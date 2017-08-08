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
    - Triggered fedmsg via **module-stream-version** string
    - Triggered by **Module Build system** done message, list of all: https://apps.fedoraproject.org/datagrepper/raw?topic=org.fedoraproject.prod.mbs.module.state.change
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

Arbitrary Jenkins Instance
----------------------------
- Production instance: `hidden`
    - Triggered via `fedmsg file`
        - Used **tools/run-them.sh** script, for same behaviour as Taskotron
    - **run-them.sh** script for Jenkins based on whole fedmsg
        - Test Subject: Same as *Taskotron Workflow*
        - Located in: Same as *Taskotron Workflow*
        - Scheduled as: `run-them.sh testmodule /usr/share/moduleframework/tools/example_message_module.yaml fedmsg`
        - Example targets: `check-run-them-fedmsg-testmodule`
        - Internal logic
            - Same as *Taskotron Workflow*