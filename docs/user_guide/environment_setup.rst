Enviroment setup
=================

To test a particular component (docker, rpm or nspawn) the test environment should be configured accordingly, e.g. certain dependencies should be installed or some services should be started. There is an option to do it manually or by using MTF scripts.

Manual Setup
~~~~~~~~~~~~~

**Docker**

 - Install Docker if not installed
 - Add insecure registry to config if not added for your testing images
 - (Re)Start docker service

**Nspawn**

 - Install systemd-nspawn
 - Disable selinux if enabled. It is an issue in selinux-policy

**Rpm**

 - No any configuration needed

**OpenShift**

 - Install OpenShift if not installed and if environment variable ``OPENSHIFT_LOCAL`` is specified.
 - if ``OPENSHIFT_LOCAL`` variable is specified, then it starts an OpenShift by command ``oc cluster up`` or stops it by command ``oc cluster down``.

Automated Setup
~~~~~~~~~~~~~~~

The environment configuration scripts should be executed in the same directory where the tests are, otherwise the environment variable **CONFIG** should be set.

  - to setup environment run ``MODULE=docker mtf-env-set``
  - to execute tests run ``MODULE=docker mtf your.test.py``
  - to cleanup environment ``MODULE=docker mtf-env-clean``

Test Creation
~~~~~~~~~~~~~~~

There is a script called mtf-init which generates easy template of test for module docker as example.

  -  to create template for module docker ``mtf-init --name your_name --container path_to_your_container``

