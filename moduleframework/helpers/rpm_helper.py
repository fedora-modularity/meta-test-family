#!/usr/bin/python
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
from moduleframework.exceptions import *


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
        self.loadconfig()
        self.yumrepo = os.path.join(
            "/etc", "yum.repos.d", "%s.repo" %
                                   self.moduleName)
        self.info = self.config['module']['rpm']
        self.repos = []
        self.whattoinstallrpm = ""
        self.bootstrappackages = []

    def setModuleDependencies(self):
        if not get_if_remoterepos():
            temprepositories = {}
            if self.getModulemdYamlconfig()["data"].get("dependencies") and self.getModulemdYamlconfig()["data"][
                "dependencies"].get("requires"):
                temprepositories = self.getModulemdYamlconfig()["data"]["dependencies"]["requires"]
            temprepositories_cycle = dict(temprepositories)
            for x in temprepositories_cycle:
                pdc = pdc_data.PDCParser()
                pdc.setLatestPDC(x, temprepositories_cycle[x])
                temprepositories.update(pdc.generateDepModules())
            self.moduledeps = temprepositories
            print_info("Detected module dependencies:", self.moduledeps)
        else:
            self.moduledeps = {"base-runtime": "master"}
            print_info("Remote repos on, set just one repo:", self.moduledeps)

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
        self.setModuleDependencies()
        self.setRepositoriesAndWhatToInstall()
        self.installTestDependencies()
        self.__callSetupFromConfig()
        self.__prepare()
        self.__prepareSetup()

    def __addModuleDependency(self, url, name=None, stream="master"):
        name = name if name else self.moduleName
        if name in self.dependencylist:
            self.dependencylist[name]['urls'].append(url)
        else:
            self.dependencylist[name] = {'urls':[url], 'stream':stream}

    def setRepositoriesAndWhatToInstall(self, repos=None, whattooinstall=None):
        """
        set repositories and packages what to install inside module
        It can override base usage of this framework to general purpose testing

        :param repos: list of repositories
        :param whattooinstall: list of packages to install inside
        :return: None
        """
        if repos is None:
            repos = []
        alldrepos = []
        if repos:
            self.repos = repos
            map(self.__addModuleDependency, repos)
        else:
            if not self.repos:
                for dep in self.moduledeps:
                    latesturl = pdc_data.get_repo_url(dep, self.moduledeps[dep])
                    alldrepos.append(latesturl)
                    self.__addModuleDependency(url=latesturl, name = dep, stream = self.moduledeps[dep])
                if get_url():
                    self.repos = [get_url()] + alldrepos
                    self.__addModuleDependency(get_url())
                elif self.info.get('repo'):
                    self.repos = [self.info.get('repo')] + alldrepos
                    self.__addModuleDependency(self.info.get('repo'))
                elif self.info.get('repos'):
                    self.repos = self.info.get('repos')
                    map(self.__addModuleDependency,self.info.get('repos'))
                else:
                    raise RpmExc("no RPM given in file or via URL")
        if whattooinstall:
            self.whattoinstallrpm = " ".join(set(whattooinstall))
        else:
            if not self.whattoinstallrpm:
                self.bootstrappackages = pdc_data.getBasePackageSet(modulesDict=self.moduledeps,
                                                                    isModule=get_if_module(), isContainer=False)
                self.whattoinstallrpm = " ".join(set(self.getPackageList() + self.bootstrappackages))

    def tearDown(self):
        """
        cleanup enviroment and call cleanup from config

        :return: None
        """
        self.stop()
        self.__callCleanupFromConfig()

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

    def __prepareSetup(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """

        a = self.runHost(
            "%s --disablerepo=* --enablerepo=%s* --allowerasing install %s" %
            (trans_dict["HOSTPACKAGER"], self.moduleName, self.whattoinstallrpm), ignore_status=True,
            verbose=is_not_silent())
        b = self.runHost(
            "%s --disablerepo=* --enablerepo=%s* --allowerasing distro-sync" %
            (trans_dict["HOSTPACKAGER"], self.moduleName), ignore_status=True, verbose=is_not_silent())

        if a.exit_status != 0 and b.exit_status != 0:
            raise RpmExc("ERROR: Unable to install packages %s" % self.whattoinstallrpm,
                         "repositories are: ",
                         self.runHost("cat %s" % self.yumrepo, verbose=is_not_silent()).stdout)

        self.ipaddr = trans_dict["GUESTIPADDR"]

    def status(self, command="/bin/true"):
        """
        Return status of module

        :param command: which command used for do that. it could be defined inside config
        :return: bool
        """
        try:
            if 'status' in self.info and self.info['status']:
                a = self.runHost(self.info['status'], shell=True, ignore_bg_processes=True, verbose=is_not_silent())
            else:
                a = self.runHost("%s" % command, shell=True, ignore_bg_processes=True, verbose=is_not_silent())
            print_debug("command:", a.command, "stdout:", a.stdout, "stderr:", a.stderr)
            return True
        except BaseException:
            return False

    def start(self, command="/bin/true"):
        """
        start the RPM based module (like systemctl start service)

        :param command: Do not use it directly (It is defined in config.yaml)
        :return: None
        """
        if 'start' in self.info and self.info['start']:
            self.runHost(self.info['start'], shell=True, ignore_bg_processes=True, verbose=is_not_silent())
        else:
            self.runHost("%s" % command, shell=True, ignore_bg_processes=True, verbose=is_not_silent())

    def stop(self, command="/bin/true"):
        """
        stop the RPM based module (like systemctl stop service)

        :param command: Do not use it directly (It is defined in config.yaml)
        :return: None
        """
        if 'stop' in self.info and self.info['stop']:
            self.runHost(self.info['stop'], shell=True, ignore_bg_processes=True, verbose=is_not_silent())
        else:
            self.runHost("%s" % command, shell=True, ignore_bg_processes=True, verbose=is_not_silent())

    def run(self, command="ls /", **kwargs):
        """
        Run command inside module, for RPM based it is same as runHost

        :param command: str of command to execute
        :param kwargs: dict from avocado.process.run
        :return: avocado.process.run
        """
        return self.runHost('bash -c "%s"' %
                            sanitize_cmd(command), **kwargs)

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

    def __callSetupFromConfig(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """
        if self.info.get("setup"):
            self.runHost(self.info.get("setup"), shell=True, ignore_bg_processes=True, verbose=is_not_silent())

    def __callCleanupFromConfig(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """
        if self.info.get("cleanup"):
            self.runHost(self.info.get("cleanup"), shell=True, ignore_bg_processes=True, verbose=is_not_silent())
