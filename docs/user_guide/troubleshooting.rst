Troubleshooting
===============

First test takes so long time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is expected behavior, because the first test run downloads all packages from Koji and creates a local
repo. It is workaround because of missing composes for modules (on demand done by pungi). To make tests execute faster use environment variables:

    - **MTF_DO_NOT_CLEANUP=yes** does not clean up module after tests execution (a machine remains running).
    - **MTF_REUSE=yes** uses the same module between tests. It speeds up test execution. It can cause side effects.
    - **MTF_REMOTE_REPOS=yes** disables downloading of Koji packages and creating a local repo, and speeds up test execution.

Unable to debug avocado output errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you see an error: ``Avocado crashed: TestError: Process died before it pushed early test_status.``, add environment variables:

    - **AVOCADO_LOG_DEBUG=yes**
    - **DEBUG=yes**
