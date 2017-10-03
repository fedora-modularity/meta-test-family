# Source to image example

Contains example how to use `S2I` image testing.

## How to


### Using inherited modules
 - It is possible to test more than just one version of s2i container with inheritance.
 - In `config.yaml`, you can define `parent` set to `docker` and then you can define more docker modules and use them via envvar definition `MODULE=your_docker_module`
 - base module there is `python-2.7` as an example

### Prerare env
There has to be installed some prerequisties like (`source-to-image`, `curl`). Enable docker etc.
 - use: `mtf-env-set`

### Run tests
 - run it via Makefile: `make`
 - run test manually: `mtf simpleTest.py` or for `python-3.5` use `MODULE=docker-python-35 mtf simpleTest.py`
 - or dicrectly via avocado: `avocado run simpleTest.py`

### Run Simple usage check
 - This test is litle bit hackish, but ilustrates how it can be used with minimal config
 - Please use `usage` tests from `simpleTest.py` file
 - run it via Makefile: `make check-usage-minimal`
 - run test manually: `CONFIG=/usr/share/moduleframework/docs/example-config-minimal.yaml URL=docker=centos/python-35-centos7 MODULE=docker mtf usageTest.py`
 - Why there is used minimal config instead of default one? Answer is that it does not contain any setup  or start action, what are not important for this usage testing. It tests original container, what is not expected to provide any service.

### Sample output

```
$ sudo make check-python-3.5
MODULE=docker-python-35 mtf simpleTest.py
JOB ID     : 0516a31a4e1c6dda1d2ed539a86c77bba2c79481
JOB LOG    : /root/avocado/job-results/job-2017-09-29T15.23-0516a31/job.log
 (1/4) simpleTest.py:UsageTest.test_usage: PASS (11.00 s)
 (2/4) simpleTest.py:simpleTests.test_basic: PASS (8.27 s)
 (3/4) simpleTest.py:simpleTests.test_via_curl: PASS (8.37 s)
 (4/4) simpleTest.py:simpleTests.test_another_port: PASS (8.87 s)
RESULTS    : PASS 4 | ERROR 0 | FAIL 0 | SKIP 0 | WARN 0 | INTERRUPT 0 | CANCEL 0
JOB TIME   : 45.71 s
JOB HTML   : /root/avocado/job-results/job-2017-09-29T15.23-0516a31/html/results.html
```

## How it works

 - creation of s2i image is based on `config.yaml` file, it contains installation of tools and using `s2i` command for image creation.
 - it contains `default_module` section set to `docker`, so you don't need to set `MODULE=docker` envvar
 - you can redefine start method of config if you would like to pass another port

