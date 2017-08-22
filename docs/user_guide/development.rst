Development & Continous integration
===============

See CONTRIBUTING.md for more info
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 * https://github.com/fedora-modularity/meta-test-family/blob/devel/CONTRIBUTING.md

Run tests by yourself locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In source code git, use directory **examples/testing-module** and run affected targets in Makefile.


Continous integration
~~~~~~~~~~~~~~~~~~~~~
On each PR there is scheduled continous integration. It should improve code quality and each PR has to pass these tests.
 * **lanscapeCI** - https://landscape.io/github/fedora-modularity/meta-test-family
 * **travis-CI** - https://travis-ci.org/fedora-modularity/meta-test-family - It doesn't cover all targets in testing-module,
just docker module with minimal config, to be fast, and also on travis there is no systemd -> no nspawn support.
