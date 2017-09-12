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

from moduleframework import module_framework
from moduleframework import dockerlinter
from moduleframework.avocado_testers import container_avocado_test


class DockerFileLinter(module_framework.AvocadoTest):
    """
    :avocado: enable

    """

    dp = None

    def setUp(self):
        # it is not intended just for docker, but just docker packages are
        # actually properly signed
        self.dp = dockerlinter.DockerfileLinter()
        if self.dp.dockerfile is None:
            self.skip()

    def test_architecture_in_env_and_label_exists(self):
        self.assertTrue(self.dp.get_docker_specific_env("ARCH="))
        self.assertTrue(self.dp.get_specific_label("architecture"))

    def test_name_in_env_and_label_exists(self):
        self.assertTrue(self.dp.get_docker_specific_env("NAME="))
        self.assertTrue(self.dp.get_specific_label("name"))

    def test_release_label_exists(self):
        self.assertTrue(self.dp.get_specific_label("release"))

    def test_version_label_exists(self):
        self.assertTrue(self.dp.get_specific_label("version"))

    def test_com_redhat_component_label_exists(self):
        self.assertTrue(self.dp.get_specific_label("com.redhat.component"))

    def test_summary_label_exists(self):
        self.assertTrue(self.dp.get_specific_label("summary"))

    def test_run_or_usage_label_exists(self):
        label_found = True
        run = self.dp.get_specific_label("run")
        if not run:
            label_found = self.dp.get_specific_label("usage")
        self.assertTrue(label_found)


class DockerfileLinterInContainer(container_avocado_test.ContainerAvocadoTest):
    """
    :avocado: enable

    """

    def test_docker_nodocs(self):
        self.start()
        installed_pkgs = self.run("rpm -qa --qf '%{{NAME}}\n'", verbose=False).stdout
        # This returns a list of packages defined in config.yaml for testing
        # e.g. ["bash", "rpm", "memcached"] in case of memcached
        defined_pkgs = self.backend.getPackageList()
        list_pkg = set(installed_pkgs).intersection(set(defined_pkgs))
        for pkg in list_pkg:
            all_docs = self.run("rpm -qd %s" % pkg, verbose=False).stdout
            for doc in all_docs.strip().split('\n'):
                self.assertNotEqual(0, self.run("test -e %s" % doc, ignore_status=True).exit_status)

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
        if int(size) < 150000:
            correct_size = True
        else:
            correct_size = False
        self.assertTrue(correct_size)


class DockerLint(container_avocado_test.ContainerAvocadoTest):
    """
    :avocado: enable
    """

    def test_basic(self):
        self.start()
        self.assertTrue("bin" in self.run("ls /").stdout)

    def test_container_is_running(self):
        """
        Function tests whether container is running
        :return:
        """
        self.start()
        self.assertIn(self.backend.jmeno.rsplit("/")[-1], self.runHost("docker ps").stdout)

    def test_labels(self):
        """
        Function tests whether labels are set in modulemd YAML file properly.
        :return:
        """
        llabels = self.getConfigModule().get('labels')
        if llabels is None or len(llabels) == 0:
            print("No labels defined in config to check")
            self.cancel()
        for key in self.getConfigModule()['labels']:
            aaa = self.checklabel(key, self.getConfigModule()['labels'][key])
            print(">>>>>> ", aaa, key)
            self.assertTrue(aaa)


class ModuleLintSigning(module_framework.AvocadoTest):
    """
    :avocado: disable
    :avocado: tags=WIP
    """

    def setUp(self):
        # it is not intended just for docker, but just docker packages are
        # actually properly signed
        if self.moduleType != "docker":
            self.skip("Docker specific test")
        super(self.__class__, self).setUp()

    def test(self):
        RHKEY = "fd431d51"
        FEDKEY = "73bde98381b46521"
        KEY = FEDKEY
        self.start()
        allpackages = self.run(
            r'rpm -qa --qf="%{{name}}-%{{version}}-%{{release}} %{{SIGPGP:pgpsig}}\n"').stdout
        for package in [x.strip() for x in allpackages.split('\n')]:
            pinfo = package.split(', ')
            if len(pinfo) == 3:
                self.assertIn(KEY, pinfo[2])


class ModuleLintPackagesCheck(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    def test(self):
        self.start()
        allpackages = [
            x.strip()
            for x in self.run(r'rpm -qa --qf="%{{name}}\n"').stdout.split('\n')]
        for pkg in self.backend.getPackageList():
            self.assertIn(pkg, allpackages)
