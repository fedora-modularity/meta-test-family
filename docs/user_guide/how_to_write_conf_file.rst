Configuration file
==================

To test a module create its configuration file ``config.yaml`` similar to an `example configuration file`_ described further. If the tested module doesn't represent any service, the `minimal configuration file`_ structure can be used.

.. _example configuration file: https://github.com/fedora-modularity/meta-test-family/blob/master/examples/memcached/config.yaml
.. _minimal configuration file: https://github.com/fedora-modularity/meta-test-family/blob/master/docs/example-config-minimal.yaml

An example of ``config.yaml`` header:

.. code-block:: yaml

    document: modularity-testing
    version: 1

An example of module general description:

.. code-block:: yaml

    name: memcached
    modulemd-url: http://raw.githubusercontent.com/container-images/memcached/master/memcached.yaml
    compose-url: https://kojipkgs.fedoraproject.org/compose/latest-Fedora-Modular-26/compose/Server/x86_64/os/Packages/m/memcached-1.4.36-1.module_b2e063be.x86_64.rpm
    service:
        port: 11211
    packages:
        rpms:
            - memcached
            - perl-Carp
    testdependencies:
        rpms:
            - nc

* **name** defines module name
* **modulemd-url** contains a link to a moduleMD file
* **compose-url** links to a final compose Pungi build. **repo** or **repos** can be used instead, see further
* **service** stores a port if a module has any
* **packages** defines a module type (at the moment only `rpms` type is supported)
* **testdependencies** covers dependencies to be installed and used in tests

An example of module types specification:

.. code-block:: yaml

    default_module: docker
    module:
        docker:
            setup: "docker run -it -e CACHE_SIZE=128 -p 11211:11211"
            cleanup:"echo Cleanup magic"
            labels:
                description: "memcached is a high-performance, distributed memory"
                io.k8s.description: "memcached is a high-performance, distributed memory"
            source: https://github.com/container-images/memcached.git
            container: docker.io/phracek/memcached
        rpm:
            setup: /usr/bin/memcached -p 11211
            cleanup: echo Cleanup magic
            start: systemctl start memcached
            stop: systemctl stop memcached
            status: systemctl status memcached
            repo:
                - http://download.englab.brq.redhat.com/pub/fedora/releases/25/Everything/x86_64/os/
                - https://phracek.fedorapeople.org/memcached-module-repo/

* **default_module**, if specified, sets the default tested module type
* **setup** runs setup commands on a host machine, not in container, and prepares the environemt for tests, for example changes selinux policy or hostname
* **cleanup**: similar to setup but done after test finished
* **start** defines how to start module service if there is any
* **stop**  defines how to stop module service if there is any
* **status** defines how to check the status of module service if there is any
* **labels** contains docker labels to check if there is any
* **container** contains a link to a container (docker.io or local tar.gz file)
* **repo** is used when **compose-url** is not set and contains a repo to be used for rpm module type testing

Multiline Bash snippet tests
-----------------------------
A ``config.yaml`` file may contain multiline Bash snippet tests directly. Every Bash command has to finish with 0 return code otherwise it returns fail:

.. code-block:: yaml

    test:
        processrunning:
            - 'ls  /proc/*/exe -alh | grep memcached'
    testhost:
        selfcheck:
            - 'echo errr | nc localhost 11211'
            - 'echo set AAA 0 4 2 | nc localhost 11211'
            - 'echo get AAA | nc localhost 11211'
        selcheckError:
            - 'echo errr | nc localhost 11211 |grep ERROR'

* **test** defines a section of multiline bash snippet tests
* **processrunning**  contains commands to run as tests and displayed as avocado output
* **testhost** is optional and similar to **test**. The difference is that it runs commands on host machine so that there could be more dependencies than there are just in a module.

.. seealso::

   :doc:`index`
       User Guide
   `webchat.freenode.net  <https://webchat.freenode.net/?channels=fedora-modularity>`_
       Questions? Help? Ideas? Stop by the #fedora-modularity chat channel on freenode IRC.
