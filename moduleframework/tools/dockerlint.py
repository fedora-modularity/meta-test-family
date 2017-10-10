# -*- coding: utf-8 -*-
#
# Meta test family (MTF) is a tool to test components of a modular Fedora:
# https://docs.pagure.org/modularity/
# Copyright (C) 2017 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# he Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Authors: Jan Scotka <jscotka@redhat.com>
#
from __future__ import print_function

import os
from moduleframework import module_framework
from moduleframework import dockerlinter
from moduleframework.avocado_testers import container_avocado_test


class DockerInstructionsTests(module_framework.AvocadoTest):
    """
    :avocado: enable
    :avocado: tags=sanity

    """

    dp = None

    def setUp(self):
        # it is not intended just for docker, but just docker packages are
        # actually properly signed
        self.dp = dockerlinter.DockerfileLinter()
        if self.dp.dockerfile is None:
            dir_name = os.getcwd()
            self.log.info("Dockerfile was not found in %s directory." % dir_name)
            self.skip()

    def test_from_is_first_directive(self):
        self.assertTrue(self.dp.check_from_is_first())

    def test_from_directive_is_valid(self):
        self.assertTrue(self.dp.check_from_directive_is_valid())

    def test_chained_run_dnf_commands(self):
        self.assertTrue(self.dp.check_chained_run_dnf_commands())

    def test_chained_run_rest_commands(self):
        self.assertTrue(self.dp.check_chained_run_rest_commands())

    def test_helpmd_is_present(self):
        self.assert_to_warn(self.assertTrue, self.dp.check_helpmd_is_present())


class DockerLabelsTests(module_framework.AvocadoTest):
    """
    :avocado: enable
    :avocado: sanity

    """

    dp = None

    def setUp(self):
        # it is not intended just for docker, but just docker packages are
        # actually properly signed
        self.dp = dockerlinter.DockerfileLinter()
        if self.dp.dockerfile is None:
            dir_name = os.getcwd()
            self.log.info("Dockerfile was not found in %s directory." % dir_name)
            self.skip()

    def _test_for_env_and_label(self, docker_env, docker_label, env=True):
        label_found = True
        if env:
            label = self.dp.get_docker_specific_env(docker_env)
        else:
            label = self.dp.get_specific_label(docker_env)
        if not label:
            label_found = self.dp.get_specific_label(docker_label)
        return label_found

    def test_architecture_in_env_and_label_exists(self):
        self.assertTrue(self.dp.get_specific_label("architecture"))

    def test_name_in_env_and_label_exists(self):
        self.assertTrue(self.dp.get_docker_specific_env("NAME="))
        self.assertTrue(self.dp.get_specific_label("name"))

    def test_maintainer_label_exists(self):
        self.assertTrue(self.dp.get_specific_label("maintainer"))

    def test_release_label_exists(self):
        self.assertTrue(self.dp.get_specific_label("release"))

    def test_version_label_exists(self):
        self.assertTrue(self.dp.get_specific_label("version"))

    def test_com_redhat_component_label_exists(self):
        self.assertTrue(self.dp.get_specific_label("com.redhat.component"))

    def test_summary_label_exists(self):
        self.assertTrue(self.dp.get_specific_label("summary"))

    def test_run_or_usage_label_exists(self):
        self.assertTrue(self._test_for_env_and_label("run", "usage", env=False))


class DockerfileLinterInContainer(container_avocado_test.ContainerAvocadoTest):
    """
    :avocado: enable

    """

    def _file_to_check(self, doc_file_list):
        test_failed = False
        for doc in doc_file_list.split('\n'):
            exit_status = self.run("test -e %s" % doc, ignore_status=True).exit_status
            if int(exit_status) == 0:
                self.log.debug("%s doc file exists in container" % doc)
                test_failed = True
        return test_failed

    def test_all_nodocs(self):
        self.start()
        all_docs = self.run("rpm -qad", verbose=False).stdout
        test_failed = self._file_to_check(all_docs)
        if test_failed:
            self.log.warn("Documentation files exist in container. They are installed by Platform or by RUN commands.")
        self.assertTrue(True)

    def test_installed_docs(self):
        """
        This test checks whether no docs are installed by RUN dnf command
        :return: FAILED in case we found some docs
                 PASS in case there is no doc file found
        """
        self.start()
        # Double brackets has to by used because of trans_dict.
        # 'EXCEPTION MTF: ', 'Command is formatted by using trans_dict.
        # If you want to use brackets { } in your code, please use {{ }}.
        installed_pkgs = self.run("rpm -qa --qf '%{{NAME}}\n'", verbose=False).stdout
        defined_pkgs = self.backend.getPackageList()
        list_pkg = set(installed_pkgs).intersection(set(defined_pkgs))
        test_failed = False
        for pkg in list_pkg:
            pkg_doc = self.run("rpm -qd %s" % pkg, verbose=False).stdout
            if self._file_to_check(pkg_doc):
                test_failed = True
        self.assertFalse(test_failed)

    def test_docker_clean_all(self):
        """
        This test checks if size of /var/cache/<pkg_manager> is bigger then
        150000 taken by command du -hsb /var/cache/<pkg_manager>

        :return: return True if size is less then 150000
                 return False is size is bigger then 150000
        """
        self.start()
        pkg_mgr = "yum"
        # Detect distro in image
        distro = self.run("cat /etc/os-release").stdout

        if 'NAME=Fedora' in distro:
            pkg_mgr = "dnf"
        # Look, whether we have solv files in /var/cache/<pkg_mgr>/*.solv
        # dnf|yum clean all deletes the file *.solv
        ret = self.run("du -shb /var/cache/%s/" % pkg_mgr, ignore_status=True)
        (size, directory) = ret.stdout.strip().split()
        if int(size) < 10000:
            correct_size = True
        else:
            correct_size = False
        self.assertTrue(correct_size)


class DockerLint(container_avocado_test.ContainerAvocadoTest):
    """
    :avocado: enable
    """

    def testLabels(self):
        """
        Function tests whether labels are set in modulemd YAML file properly.
        :return:
        """
        llabels = self.getConfigModule().get('labels')
        if llabels is None or len(llabels) == 0:
            self.log.info("No labels defined in config to check")
            self.cancel()
        for key in self.getConfigModule()['labels']:
            aaa = self.checkLabel(key, self.getConfigModule()['labels'][key])
            self.assertTrue(aaa)
