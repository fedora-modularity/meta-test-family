Enviroment setup
===============
After install of MTF, enviroment for MTF is not fully ready. each module has some dependencies&services what has to
be enabled. There is possible to do it manually, or use prepared script what will take care about that.

Manual Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Docker
------
 - Install Docker if not installed
 - Add insecure registry to config if not added for your testing images
 - (Re)Start docker service

Nspawn
------
 - Install systemd-nspawn
 - Disable selinux if enabled. It is an issue in selinux-policy

Rpm
----
 - Nothing special here for now

Automated Setup
---------------
 - use **mtf-env-** commands like an code, for mtf-env commans you have to be in same directory where are tests to be
 able to read config.yaml file or you can use env variable ``CONFIG=`` to use other config location.
.. code-block:: bash
    MODULE=docker mtf-env-set
    MODULE=docker avocado run your.test.py
    MODULE=docker mtf-env-clean

