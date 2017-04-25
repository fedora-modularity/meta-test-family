# Modularity prototype testing

## General Structure
 * __YAML Config file__
     * Each module will need to have yaml config file
     * Config file should cover non generic part - part focused on general module testing
     * It could contain also simple test
     * __how to write config file__ https://pagure.io/modularity-testing-framework/blob/master/f/docs/howtowriteyamlconf.md

 * __Self generated tests__
     * there is possible to write simple tests directly in yaml config file
     * Bash style testing
     * It has  to have solved dependencies inside each module type
     * Now it just expect to end with `0` return code of command (like: `ls / |grep sbin` directory sbin exists in root dir)
     * It can contain multiple lines
     * It generates python covered bash tests

 * __Avocado tests__
     * There is wrapper class what helps you to tests modules not focusing on module type
     * It uses avocado-framework
     * This test could be primarily used for more complex testing, not previous one
     * General test for modules: `./base/modulelint.py`
     * Example tests in `memcached` module

 * __Simple bash tests__
     * There is helper what you can use for writing `bash` like tests
     * library is https://pagure.io/modularity-testing-framework/blob/master/f/moduleframework/bashhelper.py and it is installed as `moduleframework-cmd` command in `/usr/bin`
     * Test has to call setup and cleanup of module explicitly
     * These tests are dependent on return code of commands in test, so in case you have more tests subtest, just count return codes
     * see example test for https://pagure.io/modularity-testing-framework/blob/master/f/examples/memcached/sanity2.sh


 * __WIP: Behave tests__
     * You can write tests for you module also in behave style
     * it is first prototype
     * see example in https://pagure.io/modularity-testing-framework/blob/master/f/examples/memcached-behave

## Running using VAGRANT
 * install vagrant `dnf -y install vagrant`
 * just run `vagrant up`

## Dependencies
 * base dependencies: ```docker python-pip```
 * python dependencies: avocado-framework yaml json

```bash
dnf -y install docker python-pip
```

## Schedule Tests
* Now it is expected to run this __under root__
 * Install modularity-testing-framework from COPR repo like:
    * ```dnf copr enable phracek/Modularity-testing-framework```
    * install it by command: ```dnf install -y modularity-testing-framework```
    * It installs packages to python site-packages and to /usr/share/moduleframework
* To include tests into your module, add to your Makefile section __check__
  * __check__ section runs script __run_tests.sh__ which
* Your __run_tests.sh__ should contain:
    * __Docker based module testing:__ ```MODULE=docker avocado run /usr/share/moduleframework/tools/modulelint.py ./*.py```
    * __Rpm based module testing:__ ```MODULE=rpm avocado run /usr/share/moduleframework/tools/modulelint.py ./*.py```
    * You can skip disabling SELinux by setting environment variable `MTF_SKIP_DISABLING_SELINUX`:
        * `MTF_SKIP_DISABLING_SELINUX=true avocado run ...`
    * `make check` -  runs tests in your module directory

## How to write tests
 * __minimal path creation__
  * Install modularity-testing-framework from COPR repo like:
    * ```dnf copr enable phracek/Modularity-testing-framework```
    * install it by command: ```dnf install -y modularity-testing-framework```
  * CREATE your config.yaml (see example https://pagure.io/modularity-testing-framework/blob/master/f/docs/example-config.yaml)
  * If you have tests in config file call:  `/usr/bin/generator` or simply `generator`.
  * Call command for running all python tests:  `MODULE=docker avocado run /usr/share/moduleframework/tools/modulelint.py ./*.py`
 * __additional tests__ - see tests in https://pagure.io/modularity-testing-framework/blob/master/f/examples/testing-module directory as an example for you

## License
 Framework is released under the GPL, version 2 or later, see LICENSE file in project

## Development
 * automatically built packages (untested): https://copr.fedorainfracloud.org/coprs/jscotka/modularity-testing-framework/
 * aa
