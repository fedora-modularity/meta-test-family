#!/usr/bin/python

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

LOGPARAMS = logging.getLogger('params')


def skipTestIf(value, text="Test not intended for this module profile"):
    if value:
        raise exceptions.TestDecoratorSkip(text)

class CommonFunctions():

    def runHost(self, command="ls /", **kwargs):
        return utils.process.run("%s" % command, **kwargs)

    def installTestDependencies(self, packages = None):
        if not packages and 'testdependecies' in self.config and 'rpms' in self.config['testdependecies']:
            packages = self.config['testdependecies']['rpms']
        if packages:
            self.runHost("dnf -y install " + " ".join(packages), ignore_status=True)

    def loadconfig(self):
        self.__modulemdConf = None
        xconfig = os.environ.get('CONFIG') if os.environ.get(
            'CONFIG') else "config.yaml"
        with open(xconfig, 'r') as ymlfile:
            self.config = yaml.load(ymlfile)
            if self.config['document'] != 'modularity-testing':
                print "Bad config file"
                sys.exit(1)
            self.packages = self.config['packages']['rpms']
            self.moduleName = self.config['name']
        self.installTestDependencies()

    def getModulemdYamlconfig(self, urllink=None):
        if urllink:
            ymlfile = urllib.urlopen(urllink)
            cconfig = yaml.load(ymlfile)
            return cconfig
        else:
            if not self.__modulemdConf:
                ymlfile = urllib.urlopen(self.config['modulemd-url'])
                self.__modulemdConf = yaml.load(ymlfile)
            return self.__modulemdConf

class ContainerHelper(CommonFunctions):
    """
    :avocado: disable
    """

    def setUp(self):
        self.loadconfig()
        self.info = self.config['module']['docker']
        self.tarbased = None
        self.jmeno = None
        self.docker_id = None
        self.icontainer = get_correct_url() if get_correct_url()  else self.info['container']
        self.__prepare()
        self.__prepareContainer()
        self.__pullContainer()

    def tearDown(self):
        self.stop()

    def __prepare(self):
        if not os.path.isfile('/usr/bin/docker-current'):
            utils.process.run("dnf -y install docker")

    def __prepareContainer(self):
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
            registry = re.search("([^/]*)", self.icontainer).groups()[0]
            if registry not in open('/etc/sysconfig/docker', 'rw').read():
                with open("/etc/sysconfig/docker", "a") as myfile:
                    myfile.write(
                        "INSECURE_REGISTRY='--insecure-registry $REGISTRY %s'" %
                        registry)
        try:
            utils.process.run("systemctl status docker")
        except Exception as e:
            print e
            utils.process.run("systemctl restart docker")
            pass

    def __pullContainer(self):
        if self.tarbased:
            utils.process.run(
                "docker import %s %s" %
                (self.icontainer, self.jmeno))
        elif "docker=" in self.icontainer:
            pass
        else:
            utils.process.run("docker pull %s" % self.jmeno)

        self.containerInfo = json.loads(
            utils.process.run(
                "docker inspect --format='{{json .Config}}'  %s" %
                self.jmeno).stdout)

    def start(self, args="-it -d", command="/bin/bash"):
        if not self.docker_id:
            if 'start' in self.info and self.info['start']:
                self.docker_id = utils.process.run(
                    "%s -d %s" %
                    (self.info['start'], self.jmeno)).stdout
            else:
                self.docker_id = utils.process.run(
                    "docker run %s %s %s" %
                    (args, self.jmeno, command)).stdout

    def stop(self):
        try:
            utils.process.run("docker stop %s" % self.docker_id)
            utils.process.run("docker rm %s" % self.docker_id)
        except Exception as e:
            print e
            print "docker already removed"
            pass

    def status(self):
        try:
            self.run("true")
            return True
        except Exception as e:
            return False

    def run(self, command="ls /", **kwargs):
        self.start()
        return utils.process.run('docker exec %s bash -c "%s"' %
                                 (self.docker_id, command.replace('"', r'\"')), **kwargs)


class RpmHelper(CommonFunctions):
    """
    :avocado: disable
    """

    def setUp(self):
        self.loadconfig()
        #self.installroot=os.path.join("/opt", self.moduleName)
        # self.installroot="/"
        self.yumrepo = os.path.join(
            "/etc", "yum.repos.d", "%s.repo" %
            self.moduleName)
        self.info = self.config['module']['rpm']
        self.__prepare()
        self.__prepareSetup()

    def tearDown(self):
        self.stop()

    def __prepare(self):
        # if not os.path.exists(self.installroot):
        #    shutil.rmtree(self.installroot)
         #   os.makedirs(self.installroot)
        if not os.path.isfile(self.yumrepo):
            counter = 0
            f = open(self.yumrepo, 'w')
            for repo in self.info['repos']:
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
        whattoinstall = " ".join(self.packages) + " rpm"
        utils.process.run(
            "dnf -y --disablerepo=* --enablerepo=%s* install %s" %
            (self.moduleName, whattoinstall))

    def status(self, command="/bin/true"):
        if 'status' in self.info and self.info['status']:
            utils.process.run(self.info['status'])
        else:
            utils.process.run("%s" % command)

    def start(self, command="/bin/true"):
        if 'start' in self.info and self.info['start']:
            utils.process.run(self.info['start'])
        else:
            utils.process.run("%s" % command)
        time.sleep(2)

    def stop(self, command="/bin/true"):
        if 'stop' in self.info and self.info['stop']:
            utils.process.run(self.info['stop'])
        else:
            utils.process.run("%s" % command)

    def run(self, command="ls /", **kwargs):
        return utils.process.run('bash -c "%s"' % command.replace('"', r'\"'), **kwargs)

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

# INTERFACE CLASSES FOR SPECIFIC MODULE TESTS


class ContainerAvocadoTest(AvocadoTest):
    """
    :avocado: disable
    """

    def checkLabel(self, key, value):
        if key in self.backend.containerInfo['Labels'] and (
                value in self.backend.containerInfo['Labels'][key]):
            return True
        return False


class RpmAvocadoTest(AvocadoTest):
    """
    :avocado: disable
    """
    pass


def get_correct_backend(amodule=os.environ.get('MODULE')):
    if amodule == 'docker':
        return ContainerHelper(), amodule
    elif amodule == 'rpm':
        return RpmHelper(), amodule
    else:
        raise ValueError("Unsupported MODULE={0}".format(amodule))

def get_correct_profile(amodule=os.environ.get('PROFILE')):
    if not amodule:
        amodule="default"
    return amodule

def get_correct_url(amodule=os.environ.get('URL')):
    return amodule
