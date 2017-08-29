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


class DockerfileSanitize(container_avocado_test.ContainerAvocadoTest):
    """
    :avocado: enable

    """

    dp = dockerlinter.DockerfileLinter(os.path.join(os.getcwd(), ".."))

    def test_docker_from_baseruntime(self):
        self.assertTrue(self.dp.check_baseruntime())

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

    def test_com_red_hat_component_label_exists(self):
        self.assertTrue(self.dp.get_specific_label("com.redhat.component"))

    def test_iok8s_description_exists(self):
        self.assertTrue(self.dp.get_specific_label("io.k8s.description"))

    def test_io_openshift_expose_services_exists(self):
        label_io_openshift = "io.openshift.expose-services"
        exposes = self.dp.get_docker_expose()
        label_list = self.dp.get_docker_labels()
        self.assertTrue(label_list[label_io_openshift])
        for exp in exposes:
            self.assertTrue("%s" % exp in label_list[label_io_openshift])

    def test_io_openshift_tags_exists(self):
        label_list = self.dp.get_docker_labels()
        self.assertTrue("io.openshift.tags" in label_list)


class DockerfileLinterInContainer(container_avocado_test.ContainerAvocadoTest):
    """
    :avocado: enable

    """

    def test_docker_nodocs(self):
        self.start()
        installed_pkgs = self.run("rpm -qa --qf '%{{NAME}}\n'", ignore_status=True).stdout
        # This returns a list of packages defined in config.yaml for testing
        # e.g. ["bash", "rpm", "memcached"] in case of memcached
        pkgs = self.backend.getPackageList()
        list_pkg = [pkg for pkg in installed_pkgs.split('\n') if pkg in pkgs]
        for pkg in list_pkg:
            all_docs = self.run("rpm -qd %s" % pkg).stdout
            for doc in all_docs.strip().split('\n'):
                self.assertNotEqual(0, self.run("test -e %s" % doc, ignore_status=True).exit_status)

    def test_docker_clean_all(self):
        self.start()
        pkg_mgr = "yum"
        # Detect distro in image
        distro = self.run("cat /etc/os-release").stdout
        if 'NAME=Fedora' in distro:
            pkg_mgr = "dnf"
        # Look, whether we have solv files in /var/cache/<pkg_mgr>/*.solv
        # dnf|yum clean all deletes the file *.solv
        ret = self.run("ls /var/cache/%s/*.solv" % pkg_mgr, ignore_status=True)
        self.assertNotEqual(0, ret.exit_status)
        self.assertEqual("", ret.stdout.strip())


class DockerLint(container_avocado_test.ContainerAvocadoTest):
    """
    :avocado: enable
    """

    def testBasic(self):
        self.start()
        self.assertTrue("bin" in self.run("ls /").stdout)

    def testContainerIsRunning(self):
        """
        Function tests whether container is running
        :return:
        """
        self.start()
        self.assertIn(self.backend.jmeno.rsplit("/")[-1], self.runHost("docker ps").stdout)

    def testLabels(self):
        """
        Function tests whether labels are set in modulemd YAML file properly.
        :return:
        """
        llabels = self.getConfigModule().get('labels')
        if llabels is None or len(llabels) == 0:
            print("No labels defined in config to check")
            self.cancel()
        for key in self.getConfigModule()['labels']:
            aaa = self.checkLabel(key, self.getConfigModule()['labels'][key])
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
