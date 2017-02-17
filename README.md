# Modularity prototype testing

## General Structure
 * __YAML Config file__
  * Each module will need to have yaml config file
  * Config file should cover non generic part - part focused on general module testing
  * It cloud contain also simple test 
 * __Avocado tests__
  * General tests using avocado framework
  * There is General test for modules: `./base/modulelint.py` (in progress)
  * Example test in `memcached` module
 * __Schedule Tests__
  * Now it is expected to run this __under root__ 
  * Run tests of all modules in this repo:
   ```
make check
```
  * Run Tests in module directory, ensure you installed new version via `make install`:
   ```
MODULE=docker avocado run ./*.py ../base/modulelint.py
```
 * __Using Makefile__
  * `make intall` - installs packages to python site-packages and to /usr/share/moduleframework
  * `make check` -  run tests

## Dependencies 
 * base dependencies: python2
 * python dependencies: avocado-framework yaml json
   ```
dnf -y install python2 python2-pip
pip install avocado-framework yaml json
```

