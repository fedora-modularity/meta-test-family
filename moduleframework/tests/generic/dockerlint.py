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


class DockerfileLinterInContainer(container_avocado_test.ContainerAvocadoTest):
    """
    :avocado: enable
    :avocado: tags=sanity,rhel,fedora,docker,docker_lint_inside_test,generic

    """

    def _file_to_check(self, doc_file_list):
        test_failed = False
        for doc in doc_file_list:
            exit_status = self.run("test -e %s" % doc, ignore_status=True).exit_status
            if int(exit_status) == 0:
                self.log.debug("%s doc file exists in container" % doc)
                test_failed = True
        return test_failed

    def test_all_nodocs(self):
        self.start()
        all_docs = self.run("rpm -qad", verbose=False).stdout
        test_failed = self._file_to_check(all_docs.split('\n'))
        msg = "Documentation files exist in container. They are installed in the base image or by RUN commands."
        if test_failed:
            self.log.warn(msg)
        self.assertTrue(True, msg=msg)

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
        docu_pkg = []
        for pkg in list_pkg:
            pkg_doc = self.run("rpm -qd %s" % pkg, verbose=False).stdout
            if self._file_to_check(pkg_doc.split('\n')):
                docu_pkg.append(pkg)
                test_failed = True
        self.assertFalse(test_failed, msg="There is documentation installed for packages: %s" % ','.join(docu_pkg))

    def _check_container_files(self, exts, pkg_mgr):
        found_files = False
        file_list = []
        for ext in exts:
            dir_with_ext = "/var/cache/{pkg_mgr}/**/*.{ext}".format(pkg_mgr=pkg_mgr, ext=ext)
            # Some images does not contain find command and therefore we have to use for or ls.
            ret = self.run('shopt -s globstar && for i in {dir}; do printf "%s\\n" "$i" ; done'.format(
                dir=dir_with_ext),
                ignore_status=True)
            # we did not find any file with an extension.
            # TODO I don't how to detect failure or empty files.
            if ret.stdout.strip() == dir_with_ext:
                continue
            file_list.extend(ret.stdout.split('\n'))
        if self._file_to_check(file_list):
            found_files = True
        return found_files

    def _dnf_clean_all(self):
        """
        Function checks if files with relevant extensions exist in /var/cache/dnf directory
        :return: True if at least one file exists
                 False if no file exists
        """
        exts = ["solv", "solvx", "xml.gz", "rpm"]
        return self._check_container_files(exts, "dnf")

    def _yum_clean_all(self):
        """
        Function checks if files with relevant extensions exist in /var/cache/dnf directory
        :return: True if at least one file exists
                 False if no file exists
        """
        # extensions are taken from https://github.com/rpm-software-management/yum/blob/master/yum/__init__.py#L2854
        exts = ['rpm', 'sqlite', 'sqlite.bz2', 'xml.gz', 'asc', 'mirrorlist.txt', 'cachecookie', 'xml']
        return self._check_container_files(exts, "yum")

    def test_docker_clean_all(self):
        """
        This test checks if `dnf/yum clean all` was called in image

        :return: return True if clean all is called
                 return False if clean all is not called
        """
        self.start()
        # Detect distro in image
        distro = self.run("cat /etc/os-release").stdout
        if 'Fedora' in distro:
            self.assertFalse(self._dnf_clean_all(), msg="`dnf clean all` is not present in Dockerfile.")
        else:
            self.assertFalse(self._yum_clean_all(), msg="`yum clean all` is not present in Dockerfile.")


class DockerLint(container_avocado_test.ContainerAvocadoTest):
    """
    :avocado: enable
    :avocado: tags=sanity,rhel,fedora,docker,docker_labels_inspect_test
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
            print(self.getConfigModule()['labels'][key])
            aaa = self.checkLabel(key, self.getConfigModule()['labels'][key])
            self.assertTrue(aaa, msg="Label %s is not set properly in modulemd YAML file." % key)
