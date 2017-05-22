Modularity-testing-framework
============================

Modularity prototype testing
----------------------------

- General Structure
    - **YAML Config file**
        - Each module will need to have yaml config file
        - Config file should cover non generic part - part focused on general module testing
        - It could contain also simple test
        - **how to write config file** `https://pagure.io/modularity-testing-framework/blob/master/f/docs/howtowriteyamlconf.md`

    - **Self generated tests**
        - there is possible to write simple tests directly in yaml config file
        - Bash style testing
        - It has  to have solved dependencies inside each module type
        - Now it just expect to end with *0* return code of command (like: *ls / |grep sbin* directory sbin exists in root dir)
        - It can contain multiple lines
        - It generates python covered bash tests
        - You has to call `generator` binary explicitly, it then create these pythonish tests with bash inside, *Unittest* doesn not allow to have dynamic tests.

    - **Avocado tests**
        - There is wrapper class what helps you to tests modules not focusing on module type
        - It uses avocado-framework
        - This test could be primarily used for more complex testing, not previous one
        - General test for modules: *./base/modulelint.py*
        - Example tests in *memcached* module

    - **Simple bash tests**
        - There is helper what you can use for writing *bash* like tests
        - library is `https://pagure.io/modularity-testing-framework/blob/master/f/moduleframework/bashhelper.py` and it is installed as *moduleframework-cmd* command in */usr/bin*
        - Test has to call setup and cleanup of module explicitly
        - These tests are dependent on return code of commands in test, so in case you have more tests subtest, just count return codes
        - see example test for `https://pagure.io/modularity-testing-framework/blob/master/f/examples/memcached/sanity2.sh`


    - **WIP: Behave tests**
        - You can write tests for you module also in behave style
        - it is first prototype
        - see example in `https://pagure.io/modularity-testing-framework/blob/master/f/examples/memcached-behave`

Running using VAGRANT
---------------------
- install vagrant *dnf -y install vagrant*
- just run *vagrant up*

Dependencies
------------
- base dependencies: **docker python-pip**
- python dependencies: **avocado-framework yaml json behave**

  dnf -y install docker python-pip
  pip install avocado-framework yaml json behave

Enviromental variables
----------------------
- variables allows you to overwrite some values inside *config.yaml*
- *DEBUG* Enable debugging output to test output
- *CONFIG* file with MTF configuration default is *config.yaml*
- *MODULE* which module type to test (in case there is not set *default-module* in config, you **HAVE TO** set it)
    - *=docker* uses section *docker* inside config file and will use docker containerisation
    - *=nspawn* systemd nspawn, it is lightweight virtualization, it does something like **MOCK** but it is not just chroot, but has own systemd etc.
    - *=rpm* testing of local RPM packages directly on HOST (it could be **DESTRUCTIVE**)

- *URL* see example config. It overwrites value *module.docker.container* or *module.rpm.repo* to whatever you want. It has to be proper type what is set in *MODULE*
- *MODULEMDURL* overwrite location of moduleMD file
- *COMPOSEURL* overwrite location of compose repo location
- *PROFILE* overwrite *default* profile to whatever you want to install instead of that
- *MTF_SKIP_DISABLING_SELINUX* In nspawn type on fedora-25 we have to disable selinux, because it does not work well with selinux enabled, this option allows to not do that.
- *MTF_DO_NOT_CLEANUP* Do not cleanup modules between tests, in case there is no interference in your tests you can use it, and it will be **fast**
- *MTF_REMOTE_REPOS* It disables downloading of packages done by koji and creating local repo, it make tests **fast**. (There is issue that composes (repos) are sometimes bad in fedora, unable to use)


Schedule Tests
--------------
- Now it is expected to run this **under root**
- Install modularity-testing-framework from COPR repo like:
    - **dnf copr enable phracek/Modularity-testing-framework**
    - install it by command: **dnf install -y modularity-testing-framework**
    - It installs packages to python site-packages and to /usr/share/moduleframework
- To include tests into your module, add to your Makefile section **test**
- **test** section runs another Makefile in directory **tests**
- Your **Makefile** should contain:
    - **Docker based module testing:** `cd tests; MODULE=docker make all`
    - **Repo based module testing:** `MODULE=nspawn make all `
    - **Host Rpm based module testing:** `MODULE=rpm make all`

- Makefile in tests directory looks like:

    $ cat tests/Makefile
    MODULE_LINT=/usr/share/moduleframework/tools/modulelint.py
    CMD=python -m avocado run --filter-by-tags=-WIP $(MODULE_LINT) *.py

    #
    all: $(CMD)

    - **Makefile in MTF** `https://pagure.io/modularity-testing-framework/blob/master/f/examples/testing-module/Makefile`

- `make check` -  runs tests in your module directory


How to write tests
------------------
- **minimal path creation**
- Install modularity-testing-framework from COPR repo like:
   - *dnf copr enable phracek/Modularity-testing-framework*
   - install it by command: *dnf install -y modularity-testing-framework*
- CREATE your config.yaml (see example `https://pagure.io/modularity-testing-framework/blob/master/f/docs/example-config.yaml`)
- If you have tests in config file call:  */usr/bin/generator* or simply *generator*.
- Call command for running all python tests:  **MODULE=docker avocado run /usr/share/moduleframework/tools/modulelint.py ./*.py**
- **additional tests** - see tests in `https://pagure.io/modularity-testing-framework/blob/master/f/examples/testing-module` directory as an example for you

License
-------
Framework is released under the GPL, version 2 or later, see LICENSE file in project

Development
-----------
- automatically built packages (untested): `https://copr.fedorainfracloud.org/coprs/jscotka/modularity-testing-framework/`

How it works
------------
- Structure of MTF:
  - `https://pagure.io/modularity-testing-framework/blob/master/f/docs/howitworks.png`
- Test types:
  - `https://pagure.io/modularity-testing-framework/blob/master/f/docs/TestTypes.png`
