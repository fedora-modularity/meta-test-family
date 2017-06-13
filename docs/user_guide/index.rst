User Guide
==========

1. In a module's root directory create a directory ``tests`` and place there a module configuration file ``config.yaml`` described in detail in section `Configuration file`_.

.. _Configuration file: how_to_write_conf_file

2. Optionally write multi like Bash snippet tests directly in ``tests/config.yaml`` file as described in section `Multi like Bash snippet tests`_.

.. _Multi like Bash snippet tests: how_to_write_conf_file#multi-like-bash-snippet-tests

3. Check the list of `Environment variables`_.

.. _Environment variables: environment_variables.

4. Write your tests, for example see `sanity tests`_ and various tests examples in ``/usr/share/moduleframework/examples/testing-module/``. All tests methods are listed in section :ref:`genindex`.
  
.. _sanity tests: https://pagure.io/modularity-testing-framework/blob/master/f/examples/template/sanity_template.py

5. In a directory ``tests`` create a ``Makefile`` as below. Line ``generator`` is optional and needed only if you have multi like Bash snippet tests.

 .. code-block:: makefile

    MODULE_LINT=/usr/share/moduleframework/tools/modulelint.py
    CMD=python -m avocado run $(MODULE_LINT) *.py
    
    #
    all:
        generator
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
        cd tests; MODULE=rpm MODULEMD=$(MODULEMDURL) URL="docker=$(IMAGE_NAME)" make all

7. Execute tests from the module root directory by running

 .. code-block:: shell

    #run tests from a module root directory
    $ make test

 or from ``tests`` directory by running

 .. code-block:: shell
 
    #run Python tests from tests/ directory
    $ sudo MODULE=docker avocado run ./*.py

 or

 .. code-block:: shell

    #run Bash tests from tests/ directory
    $ sudo MODULE=docker avocado run ./*.sh


Contents:

.. toctree::
   :maxdepth: 2

   how_to_write_conf_file
   environment_variables
   #bash_tests
   #python_tests
   scheduling
   #general-reference
   #glossary
   troubleshooting

.. seealso::

   `webchat.freenode.net  <https://webchat.freenode.net/?channels=fedora-modularity>`_
       Questions? Help? Ideas? Stop by the #fedora-modularity on freenode IRC chat channel

