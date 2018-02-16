Linters
=================

MTF provides a set of linters for checking containers and help files

Dockerfile linters
~~~~~~~~~~~~~~~~~~
Dockerfile linters are divided into two python files, like `dockerlint.py`_ and `dockerfile_lint.py`_.

.. _dockerlint.py: https://github.com/fedora-modularity/meta-test-family/blob/master/moduleframework/tests/generic/dockerlint.py
.. _dockerfile_lint.py: https://github.com/fedora-modularity/meta-test-family/blob/master/moduleframework/tests/static/dockerfile_lint.py

`dockerlint.py`_ contains those checks inside built image:

* **test_all_nodocs** checks if documentation files exist in image. There are installed in the ``base image`` or by ``RUN`` commands." . This is only ``WARN`` check.
* **test_installed_docs** checks if packages installed by ``RUN dnf`` command installs also documentation files.
* **test_clean_all** checks if ``dnf/yum clean all`` is present in Dockerfile.

`dockerfile_lint.py`_ contains those checks in Dockerfile file:

* **test_from_is_first_directive** checks if FROM instruction is really first in Dockerfile.
* **test_from_directive_is_valid** checks if FROM instruction has proper format.
* **test_chained_run_dnf_commands** checks if dnf/yum commands are chained or not.
* **test_checked_run_rest_commands** checks if RUN instructions, except dnf/yum, are chained or not.
* **test_helpmd_is_present** checks if help file is present for this container.
* **test_architecture_label_exists** checks if architecture label is present in Dockerfile.
* **test_name_in_env_and_label_exists** checks if name label is present in Dockerfile and NAME is present as ENV variable.
* **test_maintainer_label_exists** checks if maintainer label is present in Dockerfile.
* **test_release_label_exists** checks if release label is present in Dockerfile.
* **test_version_label_exists** checks if version label is present in Dockerfile.
* **test_com_redhat_component_label_exists** checks if com.redhat.component label is present in Dockerfile.
* **test_summary_label_exists** checks if summary label is present in Dockerfile.
* **test_run_or_usage_label_exists** check is run or usage label is present in Dockerfile.

Help file linter
~~~~~~~~~~~~~~~~~
Help file linter checks if help.md file contains important sections. Help file linter is `helpmd_lint.py`_.

.. _helpmd_lint.py: https://github.com/fedora-modularity/meta-test-family/blob/master/moduleframework/tests/static/helpmd_lint.py

Example of such help.md file is:

.. code-block:: makefile

   % MEMCACHED(1) Container Image Pages
   % Petr Hracek
   % February 6, 2017
   # NAME
   # DESCRIPTION
   # USAGE
   # SECURITY IMPLICATIONS


`helpmd_lint.py`_ contains those checks inside help.md file:

* **test_helpmd_image_name** checks if help file contains image name. The correct format is e.g. ``% MEMCACHED(1)``.
* **test_helpmd_maintainer_name** checks if help file contains maintainer name. The correct format is e.g. ``% USER NAME``.
* **test_helpmd_name** checks if help file contains section called ``# NAME``. The section describes name of the container and short description.
* **test_helpmd_description** checks if help file contains section called ``# DESCRIPTION``. This sections describes how to use image, etc.
* **test_helpmd_usage** checks if help file contains section called ``# USAGE``.
* **test_helpmd_environment_variables** checks if help file contains section called ``# ENVIRONMENT VARIABLES``. The check is valid only if ENV variable are present in Dockerfile. There is no heuristic check, like validation all variables.
* **test_helpmd_security_implications** checks if help file contains section called ``# SECURITY IMPLICATIONS``. The check is valid only if container expose a port. There is no heuristic if exposed port is the same in help file.

.. seealso::

   :doc:`index`
       User Guide
   `webchat.freenode.net  <https://webchat.freenode.net/?channels=fedora-modularity>`_
       Questions? Help? Ideas? Stop by the #fedora-modularity chat channel on freenode IRC.

