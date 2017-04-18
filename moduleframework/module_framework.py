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

import os
import sys
import re
import shutil
import yaml
import json
import time
import urllib
import logging
from avocado import Test
from avocado import utils
from avocado.core import exceptions
from avocado.utils import service
from compose_info import ComposeParser
import pdc_data


LOGPARAMS = logging.getLogger('params')

def skipTestIf(value, text="Test not intended for this module profile"):
    if value:
        raise exceptions.TestDecoratorSkip(text)

class CommonFunctions(object):
    config = None

    def runHost(self, command="ls /", **kwargs):
        return utils.process.run("%s" % command, **kwargs)

    def installTestDependencies(self, packages = None):
        if not packages and 'testdependecies' in self.config and 'rpms' in self.config['testdependecies']:
            packages = self.config['testdependecies']['rpms']
        if packages:
            self.runHost("dnf -y install " + " ".join(packages), ignore_status=True)

    def loadconfig(self):
        self.__modulemdConf = None
        self.config = get_correct_config()
        self.moduleName = self.config['name']
        self.packages = self.config['packages'].get('rpms') if self.config.has_key('packages') and  self.config['packages'].has_key('rpms') and self.config['packages'].get('rpms') else None
        self.source = self.config.get('source') if self.config.get('source') else self.config['module']['rpm'].get('source')

    def getModulemdYamlconfig(self, urllink=None):
        if urllink:
            ymlfile = urllib.urlopen(urllink)
            cconfig = yaml.load(ymlfile)
            return cconfig
        else:
            if self.config is None:
                self.loadconfig()
            if not self.__modulemdConf:
                ymlfile = urllib.urlopen(get_correct_modulemd())
                self.__modulemdConf = yaml.load(ymlfile)
            return self.__modulemdConf

class ContainerHelper(CommonFunctions):
    """
    :avocado: disable
    """

    def __init__(self):
        self.loadconfig()
        self.info = self.config['module']['docker']
        self.tarbased = None
        self.jmeno = None
        self.docker_id = None
        self.icontainer = get_correct_url() if get_correct_url()  else self.info['container']
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
        return self.icontainer

    def getDockerInstanceName(self):
        return self.jmeno

    def setUp(self):
        self.installTestDependencies()
        self.__prepare()
        self.__prepareContainer()
        self.__pullContainer()
        self.__callSetupFromConfig()

    def tearDown(self):
        self.stop()
        self.__callCleanupFromConfig()

    def __prepare(self):
        if not os.path.isfile('/usr/bin/docker-current'):
            self.runHost("dnf -y install docker")

    def __prepareContainer(self):
        if self.tarbased == False and self.jmeno == self.icontainer and "docker.io" not in self.info['container']:
            registry = re.search("([^/]*)", self.icontainer).groups()[0]
            if registry not in open('/etc/sysconfig/docker', 'rw').read():
                with open("/etc/sysconfig/docker", "a") as myfile:
                    myfile.write(
                        "INSECURE_REGISTRY='--insecure-registry $REGISTRY %s'" %
                        registry)
        service_manager = service.ServiceManager()
        service_manager.start('docker')

    def __pullContainer(self):
        if self.tarbased:
            self.runHost(
                "docker import %s %s" %
                (self.icontainer, self.jmeno))
        elif "docker=" in self.icontainer:
            pass
        else:
            self.runHost("docker pull %s" % self.jmeno)

        self.containerInfo = json.loads(
            self.runHost(
                "docker inspect --format='{{json .Config}}'  %s" %
                self.jmeno).stdout)

    def start(self, args="-it -d", command="/bin/bash"):
        if not self.status():
            if 'start' in self.info and self.info['start']:
                self.docker_id = self.runHost(
                    "%s -d %s" %
                    (self.info['start'], self.jmeno), shell=True).stdout
            else:
                self.docker_id = self.runHost(
                    "docker run %s %s %s" %
                    (args, self.jmeno, command), shell=True).stdout
            self.docker_id = self.docker_id.strip()
            if self.packages:
                self.run("dnf -y install %s" % " ".join(self.packages), ignore_status=True)
                self.run("microdnf -y install %s" % " ".join(self.packages), ignore_status=True)
        self.docker_id = self.docker_id.strip()


    def stop(self):
        if self.status():
            try:
                self.runHost("docker stop %s" % self.docker_id)
                self.runHost("docker rm %s" % self.docker_id)
            except Exception as e:
                print e
                print "docker already removed"
                pass

    def status(self):
        if self.docker_id and self.docker_id[:12] in self.runHost("docker ps", shell = True).stdout:
            return True
        else:
            return False

    def run(self, command="ls /", **kwargs):
        self.start()
        return self.runHost('docker exec %s bash -c "%s"' %
                                 (self.docker_id, command.replace('"', r'\"')), **kwargs)

    def copyTo(self, src, dest):
        self.start()
        self.runHost("docker cp %s %s:%s" % (src, self.docker_id, dest))

    def copyFrom(self, src, dest):
        self.start()
        self.runHost("docker cp %s:%s %s" % (self.docker_id, src, dest))

    def __callSetupFromConfig(self):
        if self.info.get("setup"):
            self.runHost(self.info.get("setup"), shell = True)

    def __callCleanupFromConfig(self):
        if self.info.get("cleanup"):
            self.runHost(self.info.get("cleanup"), shell = True)

class RpmHelper(CommonFunctions):
    """
    :avocado: disable
    """
    def __init__(self):
        self.loadconfig()
        self.yumrepo = os.path.join(
            "/etc", "yum.repos.d", "%s.repo" %
                                   self.moduleName)
        self.info = self.config['module']['rpm']
        self.baseruntimerepo = get_latest_baseruntime_repo_url()
        if self.packages:
            self.whattoinstallrpm=" ".join(self.packages)
        elif self.getModulemdYamlconfig()['data'].get('profiles'):
            self.whattoinstallrpm = " ".join(
                self.getModulemdYamlconfig()['data']['profiles'][get_correct_profile()]['rpms'])
        else:
            self.whattoinstallrpm = " ".join(self.getModulemdYamlconfig()['data']['components']['rpms'])

        if get_correct_url():
            self.repos = [get_correct_url(), self.baseruntimerepo]
        elif self.info.get('repo'):
            self.repos = [self.info.get('repo'), self.baseruntimerepo]
        elif self.info.get('repos'):
            self.repos = self.info.get('repos')
        else:
            raise ValueError("no RPM given in file or via URL")

    def getURL(self):
        return ";".join(self.repos)

    def setUp(self):
        self.installTestDependencies()
        self.__prepare()
        self.__prepareSetup()
        self.__callSetupFromConfig()

    def tearDown(self):
        self.stop()
        self.__callCleanupFromConfig()

    def __prepare(self):
        # if not os.path.exists(self.installroot):
        #    shutil.rmtree(self.installroot)
         #   os.makedirs(self.installroot)
        if not os.path.isfile(self.yumrepo):
            counter = 0
            f = open(self.yumrepo, 'w')
            for repo in self.repos:
                counter = counter + 1
                add = """[%s%d]
name=%s%d
baseurl=%s
enabled=0
gpgcheck=0

""" % (self.moduleName, counter, self.moduleName, counter, repo)
                f.write(add)
            f.close()

    def __prepareSetup(self):
        try:
            self.runHost(
                "dnf -y --disablerepo=* --enablerepo=%s* --allowerasing install %s" %
                (self.moduleName, self.whattoinstallrpm))
            self.runHost(
                "dnf -y --disablerepo=* --enablerepo=%s* --allowerasing distro-sync" % self.moduleName,
                ignore_status=True)
        except Exception as e:
            raise Exception("ERROR: Unable to install packages %s from repositories \n%s\n original exeption:\n%s\n" %
                            (self.whattoinstallrpm,
                            utils.process.run("cat %s" % self.yumrepo).stdout,
                            e))

    def status(self, command="/bin/true"):
        if 'status' in self.info and self.info['status']:
            self.runHost(self.info['status'], shell=True)
        else:
            self.runHost("%s" % command, shell=True)

    def start(self, command="/bin/true"):
        if 'start' in self.info and self.info['start']:
            self.runHost(self.info['start'], shell=True)
        else:
            self.runHost("%s" % command, shell=True)
        time.sleep(2)

    def stop(self, command="/bin/true"):
        if 'stop' in self.info and self.info['stop']:
            self.runHost(self.info['stop'], shell=True)
        else:
            self.runHost("%s" % command, shell=True)

    def run(self, command="ls /", **kwargs):
        return self.runHost('bash -c "%s"' % command.replace('"', r'\"'), **kwargs)

    def copyTo(self, src, dest):
        self.runHost("cp -r %s %s" % (src, dest))

    def copyFrom(self, src, dest):
        self.runHost("cp -r %s %s" % (src, dest))

    def __callSetupFromConfig(self):
        if self.info.get("setup"):
            self.runHost(self.info.get("setup"), shell = True)

    def __callCleanupFromConfig(self):
        if self.info.get("cleanup"):
            self.runHost(self.info.get("cleanup"), shell = True)


class NspawnHelper(RpmHelper):

    def __init__(self):
        super(NspawnHelper, self).__init__()
        self.chrootpath = os.path.abspath(os.path.join("/opt","chroot_%s" % self.moduleName))
        self.__addionalpackages="systemd"

    def setUp(self):
        self.installTestDependencies()
        self.__prepare()
        self.__prepareSetup()
        self.__callSetupFromConfig()

    def __prepare(self):
        # if not os.path.exists(self.installroot):
        #    shutil.rmtree(self.installroot)
         #   os.makedirs(self.installroot)
        if not os.path.isfile(self.yumrepo):
            counter = 0
            f = open(self.yumrepo, 'w')
            for repo in self.repos:
                counter = counter + 1
                add = """[%s%d]
name=%s%d
baseurl=%s
enabled=0
gpgcheck=0

""" % (self.moduleName, counter, self.moduleName, counter, repo)
                f.write(add)
            f.close()


    def __prepareSetup(self):
        if os.path.exists(self.chrootpath):
            shutil.rmtree(self.chrootpath)
        os.mkdir(self.chrootpath)
        self.runHost("dnf -y install systemd-container")
        try:
            self.runHost(
                "dnf --nogpgcheck install --installroot %s -y --allowerasing --disablerepo=* --enablerepo=%s* %s %s" %
                (self.chrootpath, self.moduleName, self.whattoinstallrpm, self.__addionalpackages))
        except Exception as e:
            raise Exception("ERROR: Unable to install packages %s from repositories \n%s\n original exeption:\n%s\n" %
                            (self.whattoinstallrpm,
                            utils.process.run("cat %s" % self.yumrepo).stdout,
                            e))
        self.nspawncont = utils.process.SubProcess("systemd-nspawn --machine=%s -bD %s" % (self.moduleName, self.chrootpath))
        self.nspawncont.start()
        time.sleep(30)

    def run(self, command="ls /", **kwargs):
        return self.runHost('machinectl shell root@%s /bin/bash -c "%s"' % (self.moduleName, command.replace('"', r'\"')), **kwargs)

    def selfcheck(self):
        return self.run().stdout

    def copyTo(self, src, dest):
        self.runHost("cp -r %s %s/%s" % (src, self.chrootpath, dest))

    def copyFrom(self, src, dest):
        self.runHost("cp -r %s/%s %s" % (self.chrootpath, src, dest))

    def tearDown(self):
        self.stop()
        self.runHost("machinectl poweroff %s" % self.moduleName)
        self.nspawncont.stop()
        self.__callCleanupFromConfig()

    def __callSetupFromConfig(self):
        if self.info.get("setup"):
            self.runHost(self.info.get("setup"), shell = True)

    def __callCleanupFromConfig(self):
        if self.info.get("cleanup"):
            self.runHost(self.info.get("cleanup"), shell = True)


# INTERFACE CLASS FOR GENERAL TESTS OF MODULES
class AvocadoTest(Test):
    """
    :avocado: disable
    """
    def setUp(self):
        (self.backend, self.moduleType) =  get_correct_backend()
        self.moduleProfile = get_correct_profile()
        LOGPARAMS.info(
            "Module Type: %s; Profile: %s" %
            (self.moduleType, self.moduleProfile))
        self.backend.setUp()

    def tearDown(self, *args, **kwargs):
        return self.backend.tearDown(*args, **kwargs)

    def start(self, *args, **kwargs):
        return self.backend.start(*args, **kwargs)

    def stop(self, *args, **kwargs):
        return self.backend.stop(*args, **kwargs)

    def run(self, *args, **kwargs):
        return self.backend.run(*args, **kwargs)

    def runCheckState(self, command = "ls /", expected_state=0, output_text = None, *args, **kwargs):
        cmd = self.run(command, ignore_status=True, *args, **kwargs)
        output_text = command if not output_text else output_text
        if cmd.exit_status == expected_state:
            self.log.info("command (RC=%d, expected=%d): %s" % (cmd.exit_status, expected_state, output_text))
        else:
            self.fail("command (RC=%d, expected=%d): %s" % (cmd.exit_status, expected_state, output_text))

    def getConfig(self):
        return self.backend.config

    def getConfigModule(self):
        return self.backend.info

    def runHost(self, *args, **kwargs):
        return self.backend.runHost(*args, **kwargs)

    def getModulemdYamlconfig(self, *args, **kwargs):
        return self.backend.getModulemdYamlconfig(*args, **kwargs)

    def getActualProfile(self):
        self.start()
        allpackages = self.run(r'rpm -qa --qf="%{name}\n"').stdout.split('\n')
        return allpackages

    def copyTo(self, *args, **kwargs):
        return self.backend.copyTo(*args, **kwargs)

    def copyFrom(self, *args, **kwargs):
        return self.backend.copyFrom(*args, **kwargs)


# INTERFACE CLASSES FOR SPECIFIC MODULE TESTS
class ContainerAvocadoTest(AvocadoTest):
    """
    :avocado: disable
    """
    def setUp(self):
        super(ContainerAvocadoTest, self).setUp()
        if self.moduleType != "docker":
            self.skip("Docker specific test")

    def checkLabel(self, key, value):
        if key in self.backend.containerInfo['Labels'] and (
                value in self.backend.containerInfo['Labels'][key]):
            return True
        return False


class RpmAvocadoTest(AvocadoTest):
    """
    :avocado: disable
    """
    def setUp(self):
        super(RpmAvocadoTest, self).setUp()
        if self.moduleType != "rpm":
            self.skip("Rpm specific test")


def get_correct_backend():
    amodule = os.environ.get('MODULE')
    readconfig = CommonFunctions()
    readconfig.loadconfig()
    if readconfig.config.has_key("default_module") and readconfig.config["default_module"] is not None and amodule == None:
        amodule = readconfig.config["default_module"]
    if amodule == 'docker':
        return ContainerHelper(), amodule
    elif amodule == 'rpm':
        return RpmHelper(), amodule
    elif amodule == 'nspawn':
        return NspawnHelper(), amodule
    else:
        raise ValueError("Unsupported MODULE={0}".format(amodule))

def get_correct_profile():
    amodule = os.environ.get('PROFILE')
    if not amodule:
        amodule="default"
    return amodule

def get_correct_url():
    amodule = os.environ.get('URL')
    return amodule

def get_correct_config():
    cfgfile = os.environ.get('CONFIG')
    if not cfgfile:
        cfgfile="config.yaml"
    if not os.path.exists(cfgfile):
        raise ValueError("Config file (%s) does not exist or is inaccesible (you can also redefine own by CONFIG=path/to/configfile.yaml env variable)" % cfgfile)
    with open(cfgfile, 'r') as ymlfile:
        xcfg = yaml.load(ymlfile)
        if xcfg['document'] != 'modularity-testing':
            raise ValueError("Bad Config file, not yaml or does not contain proper document type" % cfgfile)
    return xcfg

def get_compose_url():
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

def get_correct_modulemd():
    mdf = os.environ.get('MODULEMDURL')
    readconfig = CommonFunctions()
    readconfig.loadconfig()
    if  mdf:
        return mdf
    elif readconfig.config.get("modulemd-url"):
        return readconfig.config.get("modulemd-url")
    else:
        a = ComposeParser(get_compose_url())
        b = a.variableListForModule(readconfig.config.get("name"))
        return [x[12:] for x in b if 'MODULEMDURL=' in x][0]


def get_latest_baseruntime_repo_url(fake=False):
    if fake:
        return "http://mirror.vutbr.cz/fedora/releases/25/Everything/x86_64/os/"
    else:
        brt = pdc_data.PDCParser()
        brt.setLatestPDC("base-runtime")
        return brt.generateRepoUrl()
