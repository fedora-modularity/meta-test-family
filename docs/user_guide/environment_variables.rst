Environment variables
=====================

Environment variables allow to overwrite some values of a module configuration file ``config.yaml``.

- **AVOCADO_LOG_DEBUG=yes** enables avocado debug output.
- **DEBUG=yes** enables debugging mode to test output.
- **CONFIG** defines the module configuration file. It defaults to ``config.yaml``.
- **MODULE** defines tested module type, if **default-module** is not set in ``config.yaml``.

    - **=docker** uses the **docker** section of ``config.yaml``.
    - **=rpm** uses the **rpm** section of ``config.yaml`` and tests RPMs directly on a host.
    - **=nspawn** tests RPMs in a virtual environment of lightweight virtualization with systemd-nspawn.

- **URL** overrides the value of **module.docker.container** or **module.rpm.repo**. The **URL** should correspond to the **MODULE** variable, for example

    - **URL=docker.io/modularitycontainers/haproxy** if **MODULE=docker**
    - **URL=https://phracek.fedorapeople.org/haproxy-module-repo** if **MODULE=nspawn** or **MODULE=rpm**

- **MODULEMDURL** overwrites the location of a moduleMD file.
- **COMPOSEURL** overwrites the location of a compose Pungi build.
- **MTF_SKIP_DISABLING_SELINUX=yes** does not disable SELinux. In nspawn type on Fedora 25 SELinux should be disabled, because it does not work well with SELinux enabled, this option allows to not do that.
- **MTF_DO_NOT_CLEANUP=yes** does not clean up modules between tests. It speeds up test execution. Use only if there is no interference between tests.
- **MTF_REMOTE_REPOS=yes** disables downloading of Koji packages and creating a local repo, and speeds up test execution.

.. seealso::

   :doc:`index`
       User Guide
   `webchat.freenode.net  <https://webchat.freenode.net/?channels=fedora-modularity>`_
       Questions? Help? Ideas? Stop by the #fedora-modularity chat channel on freenode IRC.
