# Upstream Test Metedata PoC
This project defines file strucuture and tooling to work with general test metadata.


## User Stories
* __US1:__ Schedule/__Filter__ testsets based on some filters because you have limited resources(eg. not have enought time, just tests what does not need network, because you are offine)
 * I want to select some cases based on tags
 * I want to select some cases based on relevancy
* __US2:__ Find/__Agregate__ uncovered parts in testsuite to write new tests, or report status of testsuite to managers
 * I want to see acual coverage for component
 * I want to see uncovered parts
* __US3:__ General format allows us more, Describing tests inside source code is `programming lang` specific and harder to handle
 * I want cover simple usecases in as simplest way as possible
 * I want to  be able to write complex structure as well
 * I want to have it human readable
 * I want to see some examples

### What we covers
* __Test case filtering__, based on relevancy and tags
* __Test coverage__ document and analysis.
* __Example__  [component](example-component/tests)
* __Tooling__ to work with this example, to show abilities
* __Modular__ various tools can define own items for each test and parse it how you want.

## How it works
* Tree structure of metadata splitted to two types
* can use one metadata file, or split metadata file to each test or use combination of both solution.
* Two type of `metadata.yaml`
 * __general__ - fully descriptive file for writing general info about component and testing and whatever you want - [metadata.yaml](example-component/tests/metadata.yaml)
 * __test__ - basic metadata for test, it has same value as any test in `tests` element [metadata.yaml](example-component/tests/sanity/metadata.yaml)


## Installation
```
sudo make install
```

## Self-Check
```
sudo make check
```

## Usage
 * Two tools: `tmet-filter` and `tmet-agregator`
 * Swithc to example directory `example-component/tests/` and try them
 
#### Example output of commands

```
$ tmet-agregator
50%
```

```
$ tmet-agregator -a md
# Coverage for: tests

## Description
Not given


## Tests
* general
  * by: generaltest.py
  * description: some general test doing
* networking/use_tcp (MISSING coverage)
  * description: desc of not covered, missing source
* networking/use_udp (MISSING coverage)
  * description: desc of not covered, missing source
* options/extend_test
  * by: https://github.com/fedora-modularity/meta-test-family.git
  * description: some general test doing verbose test
* options/fedora_test
  * by: fedora_specifictest.py
  * description: some general test doing verbose test
* options/new_option (MISSING coverage)
  * description: desc of not covered, missing source
* sanity
  * by: generaltest.py
  * description: some general test doing
* sanity/SSSSSS (MISSING coverage)
  * description: some general test doing

## Overall Coverage: 50%
```

```
$ tmet-filter 
file://general/generaltest.py file://networking/use_tcp/ file://networking/use_udp/ https://github.com/fedora-modularity/meta-test-family.git file://options/fedora_test/fedora_specifictest.py file://options/new_option/ file://sanity/generaltest.py file://sanity/SSSSSS/
```

```
$ tmet-filter --help
usage: tmet-filter [-h] [-r RELEVANCY] [-t TAGS]

Filter and print tests

optional arguments:
  -h, --help    show this help message and exit
  -r RELEVANCY  apply relevancy filtering, expect environment specification
  -t TAGS       apply tags filtering, expect tags in DNF form
```
