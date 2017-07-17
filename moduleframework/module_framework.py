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
# Authors: Jan Scotka <jscotka@redhat.com>
#

"""
main module provides helpers for various module types and AVOCADO(unittest) classes
what you should use for your tests (inherited)
"""

import re
import shutil
import yaml
import json
import urllib
import glob
from avocado import Test
from avocado.core import exceptions
from avocado.utils import service
from avocado.utils import process
from compose_info import ComposeParser
import pdc_data
from common import *
from timeoutlib import Retry
import time
import warnings
PROFILE = None


def skipTestIf(value, text="Test not intended for this module profile"):
    """
    function what solves troubles that it is not possible to call SKIP inside code
    You can use avocado decorators, it is preferred way.

    :param value: Boolean what is used for decision in case of True
    :param text: Error text what to raise
    :return: None
    """
    if value:
        raise ModuleFrameworkException(
            "DEPRECATED, don't use this skip, use self.cancel() inside test function, or self.skip() in setUp()")


class CommonFunctions(object):
    """
    Basic class doing configuration reading and allow do commands on host machine
    """
    config = None
    modulemdConf = None

    def __init__(self, *args, **kwargs):
        self.config = None
        self.modulemdConf = None
        self.moduleName = None
        self.source = None
        self.arch = None
        self.dependencylist = {}
        self.moduledeps = None
        # general use case is to have forwarded services to host (so thats why it is same)
        self.ipaddr = trans_dict["HOSTIPADDR"]
        trans_dict["GUESTARCH"] = self.getArch()

    def getArch(self):
        """
        get system architecture string

        :return: str
        """
        out = self.runHost(command='uname -m', verbose=False).stdout.strip()
        return out

    def runHost(self, command="ls /", **kwargs):
        """
        Run commands on host

        :param command: command to exectute
        :param kwargs: (avocado process.run) params like: shell, ignore_status, verbose
        :return: avocado.process.run
        """
        try:
            formattedcommand = command.format(**trans_dict)
        except KeyError:
            raise ModuleFrameworkException(
                "Command is formatted by using trans_dict, if you want to use brackets { } in your code please use {{ "
                "or }}, possible values in trans_dict are:",
                trans_dict)
        return process.run("%s" % formattedcommand, **kwargs)

    def PackagesInstalled(self,packagelist, func="runHost"):
        """
        Check if package list is already installed on Host

        :param packagelist: list
        :return: bool
        """
        return True
        #rpmout = getattr(self, func)("rpm -q %s" % " ".join(packagelist), ignore_status=True, verbose=is_not_silent())
        #return bool(rpmout.exit_status)


    def installTestDependencies(self, packages=None):
        """
        Which packages install to host system to satisfy environment

        :param packages: List of packages, if not set, it will install rpms from config.yaml
        :return: None
        """
        if not packages:
            typo = 'testdependecies' in self.config
            if typo:
                warnings.warn("'testdependecies' is a typo, please fix",
                              DeprecationWarning)

            # try section without typo first
            packages = self.config.get('testdependencies', {}).get('rpms')
            if packages:
                if typo:
                    warnings.warn("preferring section without typo")
            else:
                # fall back to mistyped test dependency section
                packages = self.config.get('testdependecies', {}).get('rpms')

        if packages and not self.PackagesInstalled(packages):
            self.runHost(
                "{HOSTPACKAGER} install " +
                " ".join(packages),
                ignore_status=True, verbose=is_not_silent())

    def loadconfig(self):
        """
        Load configuration from config.yaml file (it is better to call this explicitly, than in
        __init__ method for our purposes)

        :return: None
        """
        try:
            self.config = get_config()
            self.moduleName = sanitize_text(self.config['name'])
            self.source = self.config.get('source') if self.config.get(
                'source') else self.config['module']['rpm'].get('source')
        except ValueError:
            pass

    def getPackageList(self, profile=None):
        """
        Return list of packages what has to be installed inside module

        :param profile: get list for intended profile instead of default method for searching
        :return: list of packages (rpms)
        """
        out = []
        if not profile:
            if 'packages' in self.config:
                packages_rpm = self.config['packages'].get('rpms') if self.config[
                    'packages'].get('rpms') else []
                packages_profiles = []
                for x in self.config['packages'].get('profiles') if self.config[
                    'packages'].get('profiles') else []:
                    packages_profiles = packages_profiles + \
                                        self.getModulemdYamlconfig()['data']['profiles'][x]['rpms']
                out += packages_rpm + packages_profiles

            elif self.getModulemdYamlconfig()['data'].get('profiles') and self.getModulemdYamlconfig()['data'][
                'profiles'].get(get_profile()):
                out += self.getModulemdYamlconfig()['data']['profiles'][get_profile()]['rpms']
            else:
                # fallback solution when it is not known what to install
                out.append("bash")
        else:
            out += self.getModulemdYamlconfig()['data']['profiles'][profile]['rpms']
        print_info("PCKGs to install inside module:", out)
        return out

    def getModuleDependencies(self):
        return self.dependencylist

    def getModulemdYamlconfig(self, urllink=None):
        """
        Return moduleMD file yaml object.
        It can be used also for loading another yaml file via url parameter

        :param urllink: load this url instead of default one defined in config, or redefined by vaiable CONFIG
        :return: dict
        """
        try:
            if urllink:
                ymlfile = urllib.urlopen(urllink)
                cconfig = yaml.load(ymlfile)
                link = cconfig
            elif not get_if_module():
                trans_dict["GUESTPACKAGER"] = "yum -y"
                link = {"data": {}}
            else:
                if self.config is None:
                    self.loadconfig()
                if not self.modulemdConf:
                    modulemd = get_modulemd()
                    if modulemd:
                        ymlfile = urllib.urlopen(modulemd)
                        self.modulemdConf = yaml.load(ymlfile)
                link = self.modulemdConf
            return link
        except IOError as e:
            raise ConfigExc("Cannot load file")

    def getIPaddr(self):
        """
        Return ip addr string of guest machine
        In many cases it should be same as host machine and port should be forwarded to host

        :return: str
        """
        return self.ipaddr




class ContainerHelper(CommonFunctions):
    """
    Basic Helper class for Docker container module type

    :avocado: disable
    """

    def __init__(self):
        """
        set basic object variables
        """
        super(ContainerHelper, self).__init__()
        self.loadconfig()
        self.info = self.config['module']['docker']
        self.tarbased = None
        self.jmeno = None
        self.docker_id = None
        self.icontainer = get_url(
        ) if get_url() else self.info['container']
        if ".tar" in self.icontainer:
            self.jmeno = "testcontainer"
            self.tarbased = True
        if "docker=" in self.icontainer:
            self.jmeno = self.icontainer[7:]
            self.tarbased = False
        elif "docker.io" in self.info['container']:
            # Trusted source
            self.tarbased = False
            self.jmeno = self.icontainer
        else:
            # untrusted source
            self.tarbased = False
            self.jmeno = self.icontainer

    def getURL(self):
        """
        It returns actual URL link string to container, It is same as URL

        :return: str
        """
        return self.icontainer

    def getDockerInstanceName(self):
        """
        Return docker instance name what will be used inside docker as docker image name
        :return: str
        """
        return self.jmeno

    def setUp(self):
        """
        It is called by child class and it is same methof as Avocado/Unittest has. It prepares environment
        for docker testing
        * start docker if not
        * pull docker image
        * setup environment from config
        * run and store identification

        :return: None
        """
        self.installTestDependencies()
        self.__callSetupFromConfig()
        self.__prepare()
        self.__prepareContainer()
        self.__pullContainer()

    def tearDown(self):
        """
        Cleanup environment and call also cleanup from config

        :return: None
        """
        self.stop()
        self.__callCleanupFromConfig()

    def __prepare(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """
        if not os.path.isfile('/usr/bin/docker-current'):
            self.runHost("{HOSTPACKAGER} install docker", verbose=is_not_silent())

    def __prepareContainer(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """
        if self.tarbased is False and self.jmeno == self.icontainer and "docker.io" not in self.info[
            'container']:
            registry = re.search("([^/]*)", self.icontainer).groups()[0]
            if registry not in open('/etc/sysconfig/docker', 'rw').read():
                with open("/etc/sysconfig/docker", "a") as myfile:
                    myfile.write(
                        "INSECURE_REGISTRY='--insecure-registry $REGISTRY %s'" %
                        registry)
        service_manager = service.ServiceManager()
        service_manager.start('docker')

    def __pullContainer(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """
        if self.tarbased:
            self.runHost(
                "docker import %s %s" %
                (self.icontainer, self.jmeno), verbose=is_not_silent())
        elif "docker=" in self.icontainer:
            pass
        else:
            self.runHost("docker pull %s" % self.jmeno, verbose=is_not_silent())

        self.containerInfo = json.loads(
            self.runHost(
                "docker inspect %s" %
                self.jmeno, verbose=is_not_silent()).stdout)[0]["Config"]

    def start(self, args="-it -d", command="/bin/bash"):
        """
        start the docker container

        :param args: Do not use it directly (It is defined in config.yaml)
        :param command: Do not use it directly (It is defined in config.yaml)
        :return: None
        """
        if not self.status():
            if 'start' in self.info and self.info['start']:
                self.docker_id = self.runHost(
                    "%s -d %s" %
                    (self.info['start'], self.jmeno), shell=True, ignore_bg_processes=True,
                    verbose=is_not_silent()).stdout
            else:
                self.docker_id = self.runHost(
                    "docker run %s %s %s" %
                    (args, self.jmeno, command), shell=True, ignore_bg_processes=True, verbose=is_not_silent()).stdout
            self.docker_id = self.docker_id.strip()
            if self.getPackageList() and not self.PackagesInstalled(self.getPackageList(),"run"):
                a = self.run(
                    "%s install %s" %
                    (trans_dict["GUESTPACKAGER"], " ".join(
                        self.getPackageList())),
                    ignore_status=True, verbose=False)
                if a.exit_status == 0:
                    print_info("Packages installed via {GUESTPACKAGER}", a.stdout)
                else:
                    print_info(
                        "Nothing installed via {GUESTPACKAGER}), but package list is not empty",
                        self.getPackageList())
        if self.status() is False:
            raise ContainerExc(
                "Container %s (for module %s) is not running, probably DEAD immediately after start (ID: %s)" % (
                    self.jmeno, self.moduleName, self.docker_id))

    def stop(self):
        """
        Stop the docker container

        :return: None
        """
        if self.status():
            try:
                self.runHost("docker stop %s" % self.docker_id, verbose=is_not_silent())
                self.runHost("docker rm %s" % self.docker_id, verbose=is_not_silent())
            except Exception as e:
                print_debug(e, "docker already removed")
                pass

    def status(self):
        """
        get status if container is running

        :return: bool
        """
        if self.docker_id and self.docker_id[
                              : 12] in self.runHost(
            "docker ps", shell=True, verbose=is_not_silent()).stdout:
            return True
        else:
            return False

    def run(self, command="ls /", **kwargs):
        """
        Run command inside module, all params what allows avocado are passed inside shell,ignore_status, etc.

        :param command: str
        :param kwargs: dict
        :return: avocado.process.run
        """
        self.start()
        return self.runHost(
            """docker exec %s bash -c "%s" """ %
            (self.docker_id, sanitize_cmd(command)),
            **kwargs)

    def copyTo(self, src, dest):
        """
        Copy file to module

        :param src: str path to source file
        :param dest: str path to file inside module
        :return: None
        """
        self.start()
        self.runHost("docker cp %s %s:%s" % (src, self.docker_id, dest), verbose=is_not_silent())

    def copyFrom(self, src, dest):
        """
        Copy file from module

        :param src: str path of file inside module
        :param dest: str path of destination file
        :return: None
        """
        self.start()
        self.runHost("docker cp %s:%s %s" % (self.docker_id, src, dest), verbose=is_not_silent())

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
        return self.runHost("""bash -c "%s" """ %
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


class NspawnHelper(RpmHelper):
    """
    Class for MODULE testing via NSPAWN created environment, it is type of virtualization,
    something between chroot (MOCK) and full virtualization. For more info read:
    https://www.freedesktop.org/software/systemd/man/systemd-nspawn.html

    This class is derived from RPM HELPER, so that it uses same section in config file
    """

    def __init__(self):
        """
        Set basic variables for NSPAWN environment, the most important is that it set
        relative change root path
        """
        super(NspawnHelper, self).__init__()
        self.baseprefix = os.path.join(BASEPATHDIR, "chroot_")
        self.__selinuxState = None
        time.time()
        actualtime = time.time()
        if get_if_do_cleanup():
            self.jmeno = "%s_%r" % (self.moduleName, actualtime)
        else:
            self.jmeno = self.moduleName
        self.chrootpath = os.path.abspath(self.baseprefix + self.jmeno)
        print_info("name of CHROOT directory:", self.chrootpath)
        trans_dict["ROOT"] = self.chrootpath

    def setUp(self):
        """
        It is called by child class and it is same method as Avocado/Unittest has. It prepares environment
        for systemd nspawn based testing
        * installing dependencies from config
        * setup environment from config

        :return: None
        """

        if not os.environ.get('MTF_SKIP_DISABLING_SELINUX'):
            # TODO: workaround because systemd nspawn is now working well in F-25
            # (failing because of selinux)
            self.__selinuxState = self.runHost(
            "getenforce", ignore_status=True).stdout.strip()
            self.runHost("setenforce Permissive", ignore_status=True, verbose=is_not_silent(), sudo=True)
        self.setModuleDependencies()
        self.setRepositoriesAndWhatToInstall()
        self.installTestDependencies()
        self.__prepareSetup()
        self.__callSetupFromConfig()
        self.__bootMachine()

    def __is_killed(self):
        for foo in range(DEFAULTRETRYTIMEOUT):
            time.sleep(1)
            out = self.runHost("machinectl status %s" % self.jmeno, verbose=is_debug(), ignore_status=True)
            if out.exit_status != 0:
                print_debug("NSPAWN machine %s stopped" % self.jmeno)
                return True
        raise NspawnExc("Unable to stop machine %s within %d" % (self.jmeno, DEFAULTRETRYTIMEOUT))

    def __is_booted(self):
        for foo in range(DEFAULTRETRYTIMEOUT):
            time.sleep(1)
            out = self.runHost("machinectl status %s" % self.jmeno, verbose=is_debug(), ignore_status=True)
            if "systemd-logind" in out.stdout:
                print_debug("NSPAWN machine %s booted" % self.jmeno)
                return True
        raise NspawnExc("Unable to start machine %s within %d" % (self.jmeno, DEFAULTRETRYTIMEOUT))

    def __do_smart_start_cleanup(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """

        if get_if_do_cleanup():
            # delete directory with same same (in case used option DO NOT CLEANUP)
            if os.path.exists(self.chrootpath):
                shutil.rmtree(self.chrootpath, ignore_errors=True)
            # DELETE every chroot dir in case any exists
            # Commented out, because it had side effect for multihost testing. Has to be improved
            #dirstodelete = glob.glob(self.baseprefix + "*")
            #if get_if_module() and dirstodelete:
            #    for dtd in dirstodelete:
            #        shutil.rmtree(dtd, ignore_errors=True)
            os.mkdir(self.chrootpath)

    def __prepareSetup(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """
        self.__do_smart_start_cleanup()
        if not os.path.exists(os.path.join(self.chrootpath, "usr")):
            if not self.PackagesInstalled(["systemd-container"]):
                self.runHost("{HOSTPACKAGER} install systemd-container", verbose=is_not_silent(), sudo=True)
            # workaround in case machined blocked by selinux, disabled for now
            # self.runHost("sudo systemctl restart systemd-machined", verbose=is_not_silent(), sudo=True)
            repos_to_use = ""
            counter = 0
            for repo in self.repos:
                counter = counter + 1
                repos_to_use += " --repofrompath %s%d,%s" % (
                    self.moduleName, counter, repo)
            try:
                @Retry(attempts=DEFAULTRETRYCOUNT, timeout=DEFAULTRETRYTIMEOUT * 60, delay=2 * 60,
                       error=NspawnExc("RETRY: Unable to install packages"))
                def tmpfunc():
                    self.runHost(
                        "%s install --nogpgcheck --setopt=install_weak_deps=False --installroot %s --allowerasing --disablerepo=* --enablerepo=%s* %s %s" %
                        (trans_dict["HOSTPACKAGER"], self.chrootpath, self.moduleName, repos_to_use,
                         self.whattoinstallrpm), verbose=is_not_silent())

                tmpfunc()
            except Exception as e:
                raise NspawnExc(
                    "ERROR: Unable to install packages %s\n original exeption:\n%s\n" %
                    (self.whattoinstallrpm, str(e)))
            # COPY yum repository inside NSPAW, to be able to do installations
            insiderepopath = os.path.join(self.chrootpath, self.yumrepo[1:])
            try:
                os.makedirs(os.path.dirname(insiderepopath))
            except:
                pass
            counter = 0
            f = open(insiderepopath, 'w')
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

            #        shutil.copy(self.yumrepo, insiderepopath)
            #        self.runHost("sed s/enabled=0/enabled=1/ -i %s" % insiderepopath, ignore_status=True)
            for repo in self.repos:
                if "file:///" in repo:
                    src = repo[7:]
                    srcto = os.path.join(self.chrootpath, src[1:])
                    try:
                        os.makedirs(os.path.dirname(srcto))
                    except Exception as e:
                        print_debug(e, "Unable to create DIR (already created)", srcto)
                        pass
                    try:
                        shutil.copytree(src, srcto)
                    except Exception as e:
                        print_debug(e, "Unable to copy files from:", src, "to:", srcto)
                        pass
            pkipath = "/etc/pki/rpm-gpg"
            pkipath_ch = os.path.join(self.chrootpath, pkipath[1:])
            try:
                os.makedirs(pkipath_ch)
            except BaseException:
                pass
            for filename in glob.glob(os.path.join(pkipath, '*')):
                shutil.copy(filename, pkipath_ch)
            print_info("repo prepared for microdnf:", insiderepopath, open(insiderepopath, 'r').read())

    def __bootMachine(self):

        @Retry(attempts=DEFAULTRETRYCOUNT, timeout=DEFAULTRETRYTIMEOUT,
               error=NspawnExc("RETRY: Unable to start nspawn machine"))
        def tempfnc():
            print_debug("starting container via command:",
                        "systemd-nspawn --machine=%s -bD %s" % (self.jmeno, self.chrootpath))
            nspawncont = process.SubProcess(
                "systemd-nspawn --machine=%s -bD %s" %
                (self.jmeno, self.chrootpath), verbose=is_debug())
            nspawncont.start()
            self.__is_booted()

        tempfnc()
        print_info("machine: %s started" % self.jmeno)

        trans_dict["GUESTIPADDR"] = trans_dict["HOSTIPADDR"]
        self.ipaddr = trans_dict["GUESTIPADDR"]

    def status(self, command="/bin/true"):
        """
        Return status of module

        :param command: which command used for do that. it could be defined inside config
        :return: bool
        """
        try:
            if 'status' in self.info and self.info['status']:
                a = self.run(self.info['status'], shell=True, verbose=False, ignore_bg_processes=True)
            else:
                a = self.run("%s" % command, shell=True, verbose=False, ignore_bg_processes=True)
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
            self.run(self.info['start'], shell=True, ignore_bg_processes=True)
        else:
            self.run("%s" % command, shell=True, ignore_bg_processes=True)

    def stop(self, command="/bin/true"):
        """
        stop the RPM based module (like systemctl stop service)

        :param args: Do not use it directly (It is defined in config.yaml)
        :param command: Do not use it directly (It is defined in config.yaml)
        :return: None
        """
        if 'stop' in self.info and self.info['stop']:
            self.run(self.info['stop'], shell=True, ignore_bg_processes=True)
        else:
            self.run("%s" % command, shell=True, ignore_bg_processes=True)

    def run(self, command="ls /", **kwargs):
        """
        Run command inside nspawn module type. It uses machinectl shell command.
         It need few workarounds, that's why it the code seems so strange

        TODO: workaround because machinedctl is unable to behave like ssh. It is bug
        systemd-run should be used, but in F-25 it does not contain --wait option

        :param command: str command to be executed
        :param kwargs: dict parameters passed to avocado.process.run
        :return: avocado.process.run
        """
        lpath = "/var/tmp"
        if not kwargs:
            kwargs = {}
        should_ignore = kwargs.get("ignore_status")
        kwargs["ignore_status"] = True

        # workaound, try to stop shell in case already running (it sometimes happened)
        # self.runHost("systemctl -M {machine} stop container-shell@0.service".format(machine=self.jmeno), ignore_status=True, verbose=is_debug())
        comout = self.runHost("""machinectl shell root@{machine} /bin/bash -c "({comm})>{pin}/stdout 2>{pin}/stderr; echo $?>{pin}/retcode; sleep 1" """.format(
                machine=self.jmeno,
                comm=sanitize_cmd(command),
                pin=lpath),
            **kwargs)
        if comout.exit_status != 0:
            raise NspawnExc("This command should not fail anyhow inside NSPAWN:", sanitize_cmd(command))
        try:
            kwargs["verbose"] = is_not_silent()
            b = self.runHost(
                'bash -c "cat {chroot}{pin}/stdout; cat {chroot}{pin}/stderr > /dev/stderr; exit `cat {chroot}{pin}/retcode`"'.format(
                    chroot=self.chrootpath,
                    pin=lpath),
                **kwargs)
        finally:
            comout.stdout = b.stdout
            comout.stderr = b.stderr
            comout.exit_status = b.exit_status
            removesworkaround = re.search('[^(]*\((.*)\)[^)]*', comout.command)
            if removesworkaround:
                comout.command = removesworkaround.group(1)
            if comout.exit_status == 0 or should_ignore:
                return comout
            else:
                raise process.CmdError(comout.command, comout)

    def selfcheck(self):
        """
        Test if default command will pass, it is more important for nspawn, because it happens that
        it does not returns anything

        :return: avocado.process.run
        """
        return self.run().stdout

    def copyTo(self, src, dest):
        """
        Copy file to module from host

        :param src: source file on host
        :param dest: destination file on module
        :return: None
        """
        self.runHost(
            " machinectl copy-to  %s %s %s" %
            (self.jmeno, src, dest), timeout=DEFAULTPROCESSTIMEOUT, ignore_bg_processes=True, verbose=is_not_silent())

    def copyFrom(self, src, dest):
        """
        Copy file from module to host

        :param src: source file on module
        :param dest: destination file on host
        :return: None
        """
        self.runHost(
            " machinectl copy-from  %s %s %s" %
            (self.jmeno, src, dest), timeout=DEFAULTPROCESSTIMEOUT, ignore_bg_processes=True, verbose=is_not_silent())

    def tearDown(self):
        """
        cleanup environment after test is finished and call cleanup section in config file

        :return: None
        """
        try:
            self.stop()
        except Exception as stopexception:
            print_info("STOP caused exception this is bad, but have to continue to terminate machine!!!", stopexception)
            pass

        try:
            self.runHost("machinectl poweroff %s" % self.jmeno, verbose=is_not_silent())
            self.__is_killed()
        except Exception as poweroffex:
            print_info("Unable to stop machine via poweroff, terminating", poweroffex)
            try:
                self.runHost("machinectl terminate %s" % self.jmeno, ignore_status=True)
                self.__is_killed()
            except Exception as poweroffexterm:
                print_info("Unable to stop machine via terminate, STRANGE", poweroffexterm)
                pass
            pass

        if not os.environ.get('MTF_SKIP_DISABLING_SELINUX'):
            # TODO: workaround because systemd nspawn is now working well in F-25
            # (failing because of selinux)
            self.runHost(
                "setenforce %s" %
                self.__selinuxState,
                ignore_status=True, verbose=is_not_silent())
        if get_if_do_cleanup() and os.path.exists(self.chrootpath):
            shutil.rmtree(self.chrootpath, ignore_errors=True)
        self.__callCleanupFromConfig()

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


# INTERFACE CLASS FOR GENERAL TESTS OF MODULES
class AvocadoTest(Test):
    """
    MAIN class for inheritance what should be used for tests based on this framework.
    It is intended for tests what fits all module types, what does not have specific usecases for some module type.
    Class is derived from AVOCADO TEST class.

    This class is interface to *HELPER classed and use them as backend

    It is not allowed to do instances of this class!!!
    Instance is done when test is executed by test scheduler like avocado/unittest

    :avocado: disable
    """

    def __init__(self, *args, **kwargs):
        super(AvocadoTest, self).__init__(*args, **kwargs)

        (self.backend, self.moduleType) = get_backend()
        self.moduleProfile = get_profile()
        print_info(
            "Module Type: %s; Profile: %s" %
            (self.moduleType, self.moduleProfile))

    def cancel(self, *args, **kwargs):
        try:
            super(AvocadoTest, self).cancel(*args, **kwargs)
        except AttributeError:
            raise exceptions.TestDecoratorSkip(*args, **kwargs)

    def setUp(self):
        """
        Unittest setUp method. It prepares environment for selected module type like NSPAWN, DOCKER, RPM
        It is called when instance of test is created.

        When you redefine this method in your class, don't forget to call super(self.__class__,self).setUp()

        :return: None
        """
        return self.backend.setUp()

    def tearDown(self, *args, **kwargs):
        """
        Unittest tearDown method. It clean environment for selected module type like NSPAWN, DOCKER, RPM after test is done
        It is called when instance of test is finished.

        When you redefine this method in your class, don't forget to call super(self.__class__,self).tearDown()

        :return: None
        """
        return self.backend.tearDown(*args, **kwargs)

    def start(self, *args, **kwargs):
        """
        Start the module, it uses start action from config file for selected module or it calls default start
        in case start action is not defined in config file

        :param args: Do not use it directly (It is defined in config.yaml)
        :param kwargs: Do not use it directly (It is defined in config.yaml)
        :return: None
        """
        return self.backend.start(*args, **kwargs)

    def stop(self, *args, **kwargs):
        """
        Stop the module, it uses stop action from config file for selected module or it calls default stop
        in case stop action is not defined in config file (for some module type, stop action does not have sense,
        like docker, stop is done via docker stop dockerID)

        :param args: Do not use it directly (It is defined in config.yaml)
        :param kwargs: Do not use it directly (It is defined in config.yaml)
        :return: None
        """
        return self.backend.stop(*args, **kwargs)

    def run(self, *args, **kwargs):
        """
        Run command inside module, parametr command and others are passed to proper module Helper

        :param args: command
        :param kwargs: shell, ignore_status, verbose
        :return: object avocado.process.run
        """
        return self.backend.run(*args, **kwargs)

    def runCheckState(self, command="ls /", expected_state=0,
                      output_text=None, *args, **kwargs):
        """
        derived from self.run method but allows to add also to pass expected return code.

        :param command: str Command to run
        :param expected_state: int expected value of return code of command or last command in case of shell
        :param output_text: str Description of commands, what it does (in case of empty, command is default)
        :param args: pass thru
        :param kwargs: pass thru
        :return: None
        """
        cmd = self.run(command, ignore_status=True, *args, **kwargs)
        output_text = command if not output_text else output_text
        if cmd.exit_status == expected_state:
            self.log.info(
                "command (RC=%d, expected=%d): %s" %
                (cmd.exit_status, expected_state, output_text))
        else:
            self.fail(
                "command (RC=%d, expected=%d): %s" %
                (cmd.exit_status, expected_state, output_text))

    def getConfig(self):
        """
        Return dict object of loaded config file

        :return: dict
        """
        return self.backend.config

    def getConfigModule(self):
        """
        Return just part specific for this module type (module section in config file)

        :return: dict
        """
        return self.backend.info

    def runHost(self, *args, **kwargs):
        """
        Run command on host (local machine). all parameters are passed inside. the most important is command
        what contains command to run

        :param args: pass thru
        :param kwargs: pass thru
        :return: object of avocado.process.run
        """
        return self.backend.runHost(*args, **kwargs)

    def getModulemdYamlconfig(self, *args, **kwargs):
        """
        Return dict of actual moduleMD file

        :param args: pass thru
        :param kwargs: pass thru
        :return: dict
        """
        return self.backend.getModulemdYamlconfig(*args, **kwargs)

    def getActualProfile(self):
        """
        Return actual profile set profile via env variable PROFILE, could be used for filtering tests with skipIf method
        Actually it returns list of packages, because profiles are not defined well

        :return: str
        """
        self.start()
        allpackages = self.run(r'rpm -qa --qf="%{{name}}\n"', verbose=is_not_silent()).stdout.split('\n')
        return allpackages

    def copyTo(self, *args, **kwargs):
        """
        Copy file from host machine to module

        :param src: source file from host
        :param dest: destination file inside module
        :return: None
        """
        return self.backend.copyTo(*args, **kwargs)

    def copyFrom(self, *args, **kwargs):
        """
        Copy file from module to host machine

        :param src: source file from host
        :param dest: destination file inside module
        :return: None
        """
        return self.backend.copyFrom(*args, **kwargs)

    def getIPaddr(self, *args, **kwargs):
        """
        Return ip addr string of guest machine
        In many cases it should be same as host machine and port should be forwarded to host

        :return: str
        """
        return self.backend.getIPaddr(*args, **kwargs)

    def getArch(self):
        """
        get system architecture string

        :return: str
        """
        return self.backend.getArch()

    def getModuleDependencies(self):
        """
        get list of module dependencies dictionary, there is structure like:
        {module_name: {stream: master, urls=[repo_url1, repo_url2]},
         dependent_module_name: {stream: f26, urls=[repo_url3]}}

        :return: dict
        """
        return self.backend.getModuleDependencies()


# INTERFACE CLASSES FOR SPECIFIC MODULE TESTS
class ContainerAvocadoTest(AvocadoTest):
    """
    Class for writing tests specific just for DOCKER
    derived from AvocadoTest class.

    :avocado: disable
    """

    def setUp(self):
        if self.moduleType != "docker":
            self.skip("Docker specific test")
        super(ContainerAvocadoTest, self).setUp()

    def checkLabel(self, key, value):
        """
        check label of docker image, expect key value (could be read from config file)

        :param key: str
        :param value: str
        :return: bool
        """
        if key in self.backend.containerInfo['Labels'] and (
                    value in self.backend.containerInfo['Labels'][key]):
            return True
        return False


class RpmAvocadoTest(AvocadoTest):
    """
    Class for writing tests specific just for LOCAL (system) RPM testing
    derived from AvocadoTest class.

    :avocado: disable
    """

    def setUp(self):
        if self.moduleType != "rpm":
            self.skip("Rpm specific test")
        super(RpmAvocadoTest, self).setUp()


class NspawnAvocadoTest(AvocadoTest):
    """
    Class for writing tests specific just for RPM module testing inside NSPAWN env
    derived from AvocadoTest class.

    :avocado: disable
    """

    def setUp(self):
        if self.moduleType != "nspawn":
            self.skip("Nspawn specific test")
        super(NspawnAvocadoTest, self).setUp()


def get_backend():
    """
    Return proper module type, set by config by default_module section, or defined via
    env variable "MODULE"

    :return: tuple (specific module object, str)
    """
    amodule = os.environ.get('MODULE')
    readconfig = CommonFunctions()
    readconfig.loadconfig()
    if "default_module" in readconfig.config and readconfig.config[
        "default_module"] is not None and amodule is None:
        amodule = readconfig.config["default_module"]
    if amodule == 'docker':
        return ContainerHelper(), amodule
    elif amodule == 'rpm':
        return RpmHelper(), amodule
    elif amodule == 'nspawn':
        return NspawnHelper(), amodule
    else:
        raise ModuleFrameworkException("Unsupported MODULE={0}".format(amodule), "supproted are: docker, rpm, nspawn")

# To keep backward compatibility. This method could be used by pure avocado tests and is already used
get_correct_backend = get_backend


def get_profile():
    """
    Return profile name string

    :return: str
    """
    amodule = os.environ.get('PROFILE')
    if not amodule:
        amodule = "default"
    return amodule


def get_url():
    """
    Return actual URL if overwritten by
    env variable "URL"

    It redefines location of testing subject

    :return:
    """
    amodule = os.environ.get('URL')
    return amodule


def get_config():
    """
    Read the module's configuration file

    :default: ``./config.yaml`` in the ``tests`` directory of the module's root directory
    :envvar: **CONFIG=path/to/file** overrides default value.
    :return: str
    """
    cfgfile = os.environ.get('CONFIG') or './config.yaml'
    try:
       with open(cfgfile, 'r') as ymlfile:
           xcfg = yaml.load(ymlfile.read())
           return xcfg
    except IOError:
       raise ConfigExc(
           "Error: File '%s' doesn't appear to exist or it's not a YAML file." %
            cfgfile + " " +
           "Tip: If the CONFIG envvar is not set, mtf-generator looks for './config'.")


def get_compose_url():
    """
    Return Compose Url if set in config or via
    env variable COMPOSEURL

    :return: str
    """
    compose = os.environ.get('COMPOSEURL')
    readconfig = CommonFunctions()
    readconfig.loadconfig()
    if compose is None:
        if readconfig.config.get("compose-url"):
            compose = readconfig.config.get("compose-url")
        elif readconfig.config['module']['rpm'].get("repo"):
            compose = readconfig.config['module']['rpm'].get("repo")
        else:
            compose = readconfig.config['module']['rpm'].get("repos")[0]
    return compose


def get_modulemd():
    """
    Return dict of moduleMD file for module, It is read from config, from module-url section,
    if not defined it reads modulemd file from compose-url in case of set, or there is used
    env variable MODULEMDURL (eventually COMPOSEURL) for that

    :return: dict
    """
    mdf = os.environ.get('MODULEMDURL')
    readconfig = CommonFunctions()
    readconfig.loadconfig()
    try:
        if mdf:
            return mdf
        elif readconfig.config.get("modulemd-url"):
            return readconfig.config.get("modulemd-url")
        else:
            a = ComposeParser(get_compose_url())
            b = a.variableListForModule(readconfig.config.get("name"))
            return [x[12:] for x in b if 'MODULEMDURL=' in x][0]
    except AttributeError:
        return None
