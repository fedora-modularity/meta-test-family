# -*- coding: utf-8 -*-
#
# This Modularity Testing Framework helps you to write tests for modules
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
# Authors: Petr Hracek <phracek@redhat.com>
#

from moduleframework import pdc_data
from moduleframework.common import *

class RpmHelper(CommonFunctions):
    """
    Class for testing "modules" on local machine (host) directly. It could be used for scheduling tests for
    system packages

    :avocado: disable
    """

    def __init__(self):
        """
        Set basic variables for RPM based testing, based on modules.rpm section of config.yaml
        """
        super(RpmHelper, self).__init__()
        baserepodir=os.path.join("/etc", "yum.repos.d")
        # allow to fake environment in ubuntu (for Travis)
        if not os.path.exists(baserepodir):
            baserepodir="/var/tmp"
        self.yumrepo = os.path.join(baserepodir, "%s.repo" % self.moduleName)
        self.whattoinstallrpm = []
        self.bootstrappackages = []
        self.repos = []

    def getURL(self):
        """
        Return semicolon separated string of repositories what will be used, could be simialr to URL param,
         it contains also dependent repositories from PDC

        :return: str
        """
        return ";".join(self.repos)

    def setUp(self):
        """
        It is called by child class and it is same methof as Avocado/Unittest has. It prepares environment
        for RPM based testing
        * installing dependencies from config
        * setup environment from config

        :return: None
        """
        self.setRepositoriesAndWhatToInstall()
        self._callSetupFromConfig()
        self.__prepare()

    def __addModuleDependency(self, url, name=None, stream="master"):
        name = name if name else self.moduleName
        if name in self.dependencylist:
            self.dependencylist[name]['urls'].append(url)
        else:
            self.dependencylist[name] = {'urls':[url], 'stream':stream}

    def setRepositoriesAndWhatToInstall(self, repos=[], whattooinstall=None):
        """
        set repositories and packages what to install inside module
        It can override base usage of this framework to general purpose testing

        :param repos: list of repositories
        :param whattooinstall: list of packages to install inside
        :return: None
        """
        if repos:
            self.repos = repos
        else:
            self.repos += get_compose_url() or self.get_url()
            # add also all dependent modules repositories if it is module
            # TODO: removed this dependency search
            if not get_compose_url() and self.is_it_module:
                depend_repos = [get_compose_url_modular_release()]
                self.repos += depend_repos
        self.repos = list(set(self.repos))
        if whattooinstall:
            self.whattoinstallrpm = list(set(whattooinstall))
        else:
            self.bootstrappackages = pdc_data.getBasePackageSet(modulesDict=None,
                                                                isModule=self.is_it_module, isContainer=False)
            self.whattoinstallrpm = list(set(self.getPackageList() + self.bootstrappackages))

    def __prepare(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """
        counter = 0
        f = open(self.yumrepo, 'w')
        for repo in self.repos:
            counter = counter + 1
            add = """[%s%d]
name=%s%d
baseurl=%s
enabled=1
gpgcheck=0

""" % (self.moduleName, counter, self.moduleName, counter, repo)
            f.write(add)
        f.close()
        self.install_packages()
        self.ipaddr = trans_dict["GUESTIPADDR"]

    def copyTo(self, src, dest):
        """
        Copy file from one location (host) to another one to (module)

        :param src: str
        :param dest: str
        :return: None
        """
        self.runHost("cp -r %s %s" % (src, dest), verbose=is_not_silent())

    def copyFrom(self, src, dest):
        """
        Copy file from one location (module) to another one to (host)

        :param src: str
        :param dest: str
        :return: None
        """
        self.runHost("cp -r %s %s" % (src, dest), verbose=is_not_silent())

