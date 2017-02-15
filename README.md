# Modularity prototype testing

## General Structure
 * ** YAML Config file **
  * Each module will need to have yaml config file
  * Config file should cover non generic part - part focused on general module testing
  * It cloud contain also simple test 
 * ** Avocado tests **
  * General tests using avocado framework
 * ** Scheduler **
  * `MODULE=docker avocado run *.py`

Each Module contains own 
nd then there will be just general tests, 

## Dependencies 
 * base dependencies: python2
 * python dependencies: avocado-framework yaml
```bash
dnf -y install python2 python2-pip
pip install avocado-framework yaml
```

