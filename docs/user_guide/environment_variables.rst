Environment variables
=====================

Environment variables allow to overwrite some values of a module configuration file ``config.yaml``.

- **AVOCADO_LOG_DEBUG=yes** enables avocado debug output
  - **DEBUG=yes** enables debugging mode to test output
- **CONFIG** defines MTF configuration file. It defaultis to ``config.yaml``
- **MODULE** defines tested module type, if **defailt-module** is not set in ``config.yanl``    

    - **=docker** uses **docker** section of ``config.yaml``
    - **=rpm** uses **rpm** section of ``config.yaml`` and tests RPMs directly on a host
    - **=nspawn** tests RPMs in a virtual environment of lightweight virtualization with systemd-nspawn

- **URL** overwrites value of **module.docker.container** or **module.rpm.repo**. It has to be proper type what is set in **MODULE**
- **MODULEMDURL** overwrites location of a moduleMD file
- **COMPOSEURL** overwrites location of a compose Pungi build
- **MTF_SKIP_DISABLING_SELINUX=yes** does not disable SELinux In nspawn type on Fedora25 SELinux should be diabled, because it does not work well with selinux enabled, this option allows to not do that.
- **MTF_DO_NOT_CLEANUP=yes** does not cleanup modules between tests. It speeds up test execution. Use only if there is no interference between tests
- **MTF_REMOTE_REPOS=yes** disables downloading of Koji packages and creating local repo, and speeds up test execution.
