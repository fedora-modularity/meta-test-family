Installation
============

There are two ways to install and use MTF: to set up it locally or alternatively on a virtual machine via the Vagrant tool.

.. contents:: Topics

.. _using_vagrant:
Vagrant
---------------------

`Vagrant`_ is a tool to aid developers in quickly deploying development environments. There is a `Vagrantfile`_ in the `modularity-testing-framework`_ git repository on Pagure that can automatically deploy a virtual machine on your host with a MTF environment configured.

.. _Vagrant: https://docs.vagrantup.com/
.. _Vagrantfile: https://pagure.io/modularity-testing-framework/blob/master/f/Vagrantfile
.. _modularity-testing-framework: https://pagure.io/modularity-testing-framework

The MTF tool has made available for use of two providers: ``libvirt`` (for Linux host only) and ``virtualbox`` (for MAC OS, Windows and Linux hosts), where ``libvirt`` is a default one. See more about Vagrant providers `here`_.

.. _here: https://www.vagrantup.com/docs/providers/basic_usage.html#default-provider

This document assumes that you are running a recent version of Fedora although these steps should be roughly the same on other distributions, just be aware that package managers and names can differ if you are not using Fedora as your host. Consult `Vagrant installation documentation`_ to set up Vagrant for a different platform and adjuest the steps of this document accordingly.

.. _Vagrant installation documentation: https://www.vagrantup.com/docs/installation/

.. note::
   Before you start using Vagrant-libvirt, please make sure your libvirt and qemu installation is working correctly and you are able to create qemu or kvm type virtual machines with virsh or virt-manager.

Prerequisites for Vagrant
~~~~~~~~~~~~~~~~~~~~~~~~~

1. Install Vagrant. Ensure that ``vagrant-libvirt`` is among pulled dependencies.

.. code-block:: bash

    # install Vagrant
    $ sudo dnf -y install vagrant

2. Start ``libvirtd`` service

.. code-block:: bash

    # start libvirtd service
    $ sudo systemctl start libvirtd

Creating the Vagrant environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After preparing the libvirt prerequisites using the instructions above:

1. You are now prepared to check out the MTF code into your preferred location.

.. code-block:: bash

   # cd to your prefered location
   $ cd $HOME/  # Season to taste.
   $ git clone https://pagure.io/modularity-testing-framework.git

2. Next, cd into the ``modularity-testing-framework`` directory.

.. code-block:: bash

   # cd in modularity-testing-framework
   $ cd modularity-testing-framework

3. The MTF tool provides a configuration Vagrantfile that you can use to configure the Vagrant environment as given or open the Vagrantfile in your favorite editor and modify it to better fit your development preferences. This step is entirely optional as the default Vagrantfile should  work for most users.

.. code-block:: bash

   # vim Vagrantfile
   $ vim Vagrantfile

4. If you’ve happy with the Vagrantfile, you can begin provisioning your Vagrant environment. Finish by running ``vagrant reload`` to reboot machine after provisioning and apply the latest kernel updates.

.. code-block:: bash

      # Provision the Vagrant environment:
      $ sudo vagrant up --provider=libvirt # or just `sudo vagrant up` as libvirt is a default one
      # The above will run for a while while it provisions your development environment.
      $ sudo vagrant reload  # Reboot the machine at the end to apply kernel updates, etc.

5. Once you have followed the steps above, you should have a running deployed MTF development machine. ssh into your Vagrant environment::

.. code-block:: bash

      # ssh into the Vagrant environment
      $ sudo vagrant ssh

.. _local_requirements:

Local installation
------------------

Requirements
~~~~~~~~~~~~

MTF installer pulls its latest dependencies: ``python-devel``, ``python-setuptools`` and ``python-netifcaes``, ``docker``, `avocado`_, ``yaml`` and ``json``.

MTF supports Gherkin-based testing in Python. To write tests in a natural language style, backed up by Python code, install BBD tool `behave`_ . Execute the following command to install behave with pip:

.. _avocado: https://avocado-framework.github.io/
.. _behave: http://pythonhosted.org/behave/

.. code-block:: bash

    # install behave
    $ sudo pip install behave

.. _installing_mtg:
Installing MTF
~~~~~~~~~~~~~
Install MTF rpm from `Fedora Copr repo`_.

.. _Fedora Copr repo: https://copr.fedorainfracloud.org/coprs/phracek/Modularity-testing-framework/

.. code-block:: bash

    # add modularity-testing-framework yum repo
    $ sudo dnf copr enable phracek/Modularity-testing-framework
    $ sudo dnf install -y modularity-testing-framework

MTF scripts, examples and documentation will be installed into ``/usr/share/moduleframework``

.. _getting_mtf:
Source code
-----------

You may also wish to follow the `Pagure MTF repo`_ if you have a Pagure account. This stores the source code and the issue tracker for sharing bugs and feature ideas. The repository should be forked into your personal Pagure account where all work will be done. Any changes should be submitted through the pull request process.

.. _Pagure MTF repo: https://pagure.io/modularity-testing-framework

.. seealso::

   :doc:`user_guide/index`
       User Guide
   `webchat.freenode.net  <https://webchat.freenode.net/?channels=fedora-modularity>`_
       Questions? Help? Ideas? Stop by the #fedora-modularity on freenode IRC chat channel
