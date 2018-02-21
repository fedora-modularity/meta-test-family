Linters
=================

MTF provides a set of linters for checking containers, help files and Dockerfiles.

Dockerfile linters
~~~~~~~~~~~~~~~~~~
Dockerfile linters are divided into two python files: `dockerlint.py`_ and `dockerfile_lint.py`_.

.. _dockerlint.py: https://github.com/fedora-modularity/meta-test-family/blob/master/moduleframework/tests/generic/dockerlint.py
.. _dockerfile_lint.py: https://github.com/fedora-modularity/meta-test-family/blob/master/moduleframework/tests/static/dockerfile_lint.py

`dockerlint.py`_ performs these checks on an existing container image:

* **test_all_nodocs** checks if documentation files shipped by installed RPM packages have been removed. They are usually installed in the ``base image`` and inherited by child layer or installed via the ``RUN`` instruction. This is only ``WARN`` check.
* **test_installed_docs** checks if RPM packages installed by the ``RUN dnf`` command also install documentation files. The ``base image`` is an exception.
* **test_clean_all** checks if ``dnf/yum clean all`` is present in Dockerfile.

`dockerfile_lint.py`_ these checks are performed on a Dockerfile:

* **test_from_is_first_directive** checks if the FROM instruction is really first in the Dockerfile.
* **test_from_directive_is_valid** checks if the FROM instruction has proper format.
* **test_chained_run_dnf_commands** checks if dnf/yum commands are chained or not.
* **test_checked_run_rest_commands** checks if the RUN instructions, except dnf/yum, are chained or not.
* **test_helpmd_is_present** checks if the help file is present for this container.
* **test_architecture_label_exists** checks if the architecture label is present in the Dockerfile.
* **test_name_in_env_and_label_exists** checks if the name label is present in the Dockerfile and NAME is present as ENV variable.
* **test_maintainer_label_exists** checks if the maintainer label is present in the Dockerfile.
* **test_release_label_exists** checks if the release label is present in the Dockerfile.
* **test_version_label_exists** checks if the version label is present in Dockerfile.
* **test_com_redhat_component_label_exists** checks if the com.redhat.component label is present in the Dockerfile.
* **test_summary_label_exists** checks if the summary label is present in the Dockerfile.
* **test_run_or_usage_label_exists** check if the run or usage label is present in the Dockerfile.

Help file linter
~~~~~~~~~~~~~~~~~
Help file linter checks if the help.md file contains important sections. Help file linter is `helpmd_lint.py`_.

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

* **test_helpmd_image_name** checks if the help file contains an image name. The correct format is e.g. ``% MEMCACHED(1)``.
* **test_helpmd_maintainer_name** checks if the help file contains a maintainer name. The correct format is e.g. ``% USER NAME``.
* **test_helpmd_name** checks if the help file contains a section called ``# NAME``. The section describes name of the container and short description.
* **test_helpmd_description** checks if the help file contains a section called ``# DESCRIPTION``. This sections describes how to use image, etc.
* **test_helpmd_usage** checks if the help file contains a section called ``# USAGE``.
* **test_helpmd_environment_variables** checks if the help file contains a section called ``# ENVIRONMENT VARIABLES``. The check is valid only if ENV variable are present in the Dockerfile. There is no heuristic if the variable is the same as specified in the helper file.
* **test_helpmd_security_implications** checks if the help file contains a section called ``# SECURITY IMPLICATIONS``. The check is valid only if container exposes a port. There is no heuristic if the exposed port is the same as specified in the help file.

.. seealso::

   :doc:`index`
       User Guide
   `webchat.freenode.net  <https://webchat.freenode.net/?channels=fedora-modularity>`_
       Questions? Help? Ideas? Stop by the #fedora-modularity chat channel on freenode IRC.

