# Modularity prototype testing

## General Structure
 * __YAML Config file__
  * Each module will need to have yaml config file
  * Config file should cover non generic part - part focused on general module testing
  * It cloud contain also simple test 
 * __Avocado tests__
  * General tests using avocado framework
  * There is General test for modules: `./base/modulelint.py`
  * Example test in `memcached` module

## Running using VAGRANT
 * install vagrant `dnf -y install vagrant`
 * just run `vagrant up`

## Schedule Tests
  * Now it is expected to run this __under root__ 
  * ensure you installed new version via `make install`
  * * __Docker base module testing:__
   ```
MODULE=docker avocado run ./*.py ../base/modulelint.py
```
  * __Rpm base module testing:__
   ```
MODULE=rpm avocado run ./*.py ../base/modulelint.py
```

 * __Using Makefile__
  * `make install` - installs packages to python site-packages and to /usr/share/moduleframework
  * `make check` -  run tests

## Dependencies 
 * base dependencies: docker python-pip
 * python dependencies: avocado-framework yaml json
   ```
dnf -y instal docker python-pip
```

## How to write tests
 * __minimal path creation__
  ```
git clone git@gitlab.cee.redhat.com:jscotka/modularity-testing.git
cd modularity-testing
mkdir yourcomponent
cd yourcomponent
# CREATE your config.yaml
```
  * see example https://gitlab.cee.redhat.com/jscotka/modularity-testing/blob/master/base/example-config.yaml
 * __additional tests__ - see https://gitlab.cee.redhat.com/jscotka/modularity-testing/blob/master/memcached/sanity1.py as an example for you
