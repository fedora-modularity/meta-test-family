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
  * Run tests of all modules in this repo:
   ```
./run-tests
```
  * Run Tests in module directory:
   ```
MODULE=docker aavocado run ./*.py ../base/modulelint.py
```


## Dependencies 
 * base dependencies: python2
 * python dependencies: avocado-framework yaml json
   ```
dnf -y install python2 python2-pip
pip install avocado-framework yaml
```

