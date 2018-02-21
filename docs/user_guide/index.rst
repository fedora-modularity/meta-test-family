User Guide
==========

1. In a module's root directory create a directory ``tests`` and place there a module configuration file ``config.yaml`` described in detail in section `Configuration file`_. If you would like to use MTF without your own ``config.yaml``.  It is possible. It uses default minimal config. Then you have to set ``URL`` envvar to set `test subject`, otherwise it causes traceback. It is usefull for example for module what does not provide any service (no own ``start/stop/status/etc`` action defined.) or for testing with modulelint.

.. _Configuration file: how_to_write_conf_file.html

2. Optionally write multiline Bash snippet tests directly in the ``tests/config.yaml`` file as described in section `Multiline Bash snippet tests`_.

.. _Multiline Bash snippet tests: how_to_write_conf_file.html#multiline-bash-snippet-tests

3. Check the list of `Environment variables`_.

.. _Environment variables: environment_variables.html

4. Write your tests, for example see `sanity tests`_ and various tests examples in ``/usr/share/moduleframework/examples/testing-module/``. All tests methods are listed in section `API Index`_ and alphabetically in :ref:`genindex` section.

.. _sanity tests: https://github.com/fedora-modularity/meta-test-family/blob/master/examples/template/sanity_template.py
.. _API Index: ../api/index.html

5. In the directory ``tests`` create a ``Makefile`` as below.

   Mind to keep the ``mtf-generator`` line only if there are multiline Bash snippet tests in the ``tests/config.yaml`` file. The ``mtf-generator`` command will convert those multiline Bash snippet tests from the ``tests/config.yaml`` file into Python tests and stores them in the ``tests/generated.py`` file, which will be processed further by avocado.

 .. code-block:: makefile

    MODULE_LINT=/usr/share/moduleframework/tests/generic/*.py
    TESTS=*.py
    CMD=avocado run $(MODULE_LINT) $(TESTS)

    #
    all:
        mtf-generator
        $(CMD)

6. In a module's root directory create a ``Makefile``, which contains a secton **test**. For example:

 .. code-block:: makefile

    .PHONY: build run default

    IMAGE_NAME = debugging-tools
    MODULEMDURL=file://debugging-tools.yaml

    all: run
    default: run

    build:
        docker build --tag=$(IMAGE_NAME) .

    run: build
        docker run -it --name $(IMAGE_NAME) --privileged --ipc=host --net=host --pid=host -e HOST=/host -e NAME=$(IMAGE_NAME) -e IMAGE=$(IMAGE_NAME) -v /run:/run -v /var/log:/var/log -v /etc/machine-id:/etc/machine-id -v /etc/localtime:/etc/localtime -v /:/host $(IMAGE_NAME)

    test: build
        cd tests; MODULE=docker MODULEMD=$(MODULEMDURL) URL="docker=$(IMAGE_NAME)" make all
        cd tests; MODULE=nspawn MODULEMD=$(MODULEMDURL) make all
        cd tests; MODULE=openshift OPENSHIFT_IP="127.0.0.1" OPENSHIFT_USER="developer" OPENSHIFT_PASSWORD="developer" make all

7. `Prepare the environment`_ to run tests in.

.. _Prepare the environment: environment_setup.html

8. Execute tests from the module root directory by running

 .. code-block:: shell

    #run tests from a module root directory
    $ make test

 or from the ``tests`` directory by running

 .. code-block:: shell

    #run Python tests from the tests/ directory
    $ sudo MODULE=docker mtf ./*.py

 or

 .. code-block:: shell

    #run Bash tests from the tests/ directory
    $ sudo MODULE=docker mtf ./*.sh


9. `Clean up the environment`_ after test execution.

.. _Clean up the environment: environment_setup.html#automated-setup

Contents:

.. toctree::
   :maxdepth: 2

   how_to_write_conf_file
   environment_setup
   environment_variables
   scheduling
   mtf_linters
   glossary
   troubleshooting

.. seealso::

   :doc:`../api/index`
       API Index
   `webchat.freenode.net  <https://webchat.freenode.net/?channels=fedora-modularity>`_
       Questions? Help? Ideas? Stop by the #fedora-modularity chat channel on freenode IRC.
