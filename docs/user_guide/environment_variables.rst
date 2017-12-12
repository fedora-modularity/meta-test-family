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
- **MTF_DO_NOT_CLEANUP=yes** does not clean up module after tests execution (a machine remains running).
- **MTF_REUSE=yes** uses the same module between tests. It speeds up test execution. It can cause side effects.
- **MTF_REMOTE_REPOS=yes** disables downloading of Koji packages and creating a local repo, and speeds up test execution.
- **MTF_DISABLE_MODULE=yes** disables module handling to use nonmodular test mode (see `multihost tests`_ as an example).
- **DOCKERFILE="<path_to_dockerfile"** overwrites the location of a Dockerfile.
- **HELPMDFILE="<path_to_helpmdfile"** overwrites the location of a HelpMD file, If not set, search for mdfile in same directory where is Dockerfile.
- **OPENSHIFT_LOCAL=yes** enables installing ``origin`` and ``origin-clients`` on local machine
- **OPENSHIFT_IP=openshift_ip_address** uses this IP address for connecting to an OpenShift environment.
- **OPENSHIFT_USER=developer** uses this ``USER`` name for login to an OpenShift environment.
- **OPENSHIFT_PASSWORD=developer** uses this ``PASSWORD`` name for login to an OpenShift environment.
- **MTF_ODCS=[yes|openIDCtoken_string]** enable ODCS for compose creation. Token has to be placed or it tries contact openIDC token via your web browser. **Experimental feature**

.. _multihost tests: https://github.com/fedora-modularity/meta-test-family/tree/devel/examples/multios_testing


.. seealso::

   :doc:`index`
       User Guide
   `webchat.freenode.net  <https://webchat.freenode.net/?channels=fedora-modularity>`_
       Questions? Help? Ideas? Stop by the #fedora-modularity chat channel on freenode IRC.
