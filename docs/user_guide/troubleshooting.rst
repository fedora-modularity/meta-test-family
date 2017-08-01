Troubleshooting
===============

First test takes so long time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is expected behavior, because the first test run downloads all packages from Koji and creates a local
repo. It is workaround because of missing composes for modules (on demand done by pungi). To make tests execute faster use environment variables:

    - **MTF_REMOTE_REPOS=yes** - It heps in case there are repos in koji https://kojipkgs.fedoraproject.org/repos/ (they are there just temporary, deleted after 2 weeks and probably it will not be created in near future anyhow)
    - **MTF_DO_NOT_CLEANUP=yes** to disable cleaup between tests. Use only if there is no interference in between tests.

Unable to debug avocado output errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you see an error: ``Avocado crashed: TestError: Process died before it pushed early test_status.``, add environment variables:

    - **AVOCADO_LOG_DEBUG=yes**
    - **DEBUG=yes**
