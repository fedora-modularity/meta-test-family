#!/usr/bin/python

import os
import sys
import re
import shutil
import yaml
import json
import time
from avocado import Test
from avocado import utils

MODULE = os.environ.get('MODULE')

class CommonFunctions():

    def loadconfig(self):
        config = os.environ.get('CONFIG') if os.environ.get('CONFIG') else "config.yaml"
        with open(config, 'r') as ymlfile:
            self.config = yaml.load(ymlfile)
            if self.config['document'] != 'modularity-testing':
                print "Bad config file"
                sys.exit(1)
            self.packages = self.config['packages']['rpms']
            self.moduleName = self.config['name']

class ContainerHelper(Test, CommonFunctions):
    """
    :avocado: disable
    """
    def setUp(self):
        self.loadconfig()
        self.info = self.config['module']['docker']
        #brew-pulp-docker01.web.prod.ext.phx2.redhat.com:8888/rhel7/cockpit-ws:122-5
        #/mnt/redhat/brewroot/packages/cockpit-ws-docker/131/1/images/docker-image-sha256:71df4da82ff401d88e31604439b5ce67563e6bae7056f75f8f6dc715b64b4e02.x86_64.tar.gz
        self.tarbased=None
        self.jmeno=None
        self.docker_id=None
        self.icontainer = self.info['container']
        self.prepare()
        self.prepareContainer()
        self.pullContainer()

    def tearDown(self):
        self.stop()

    def prepare(self):
        if not os.path.isfile('/usr/bin/docker-current'):
            utils.process.run("dnf -y install docker")

    def prepareContainer(self):
        if ".tar.gz" in self.icontainer:
            self.jmeno="testcontainer"
            self.tarbased=True
        elif "docker.io" in self.info['container']:
        # Trusted source
            self.tarbased = False
            self.jmeno = self.icontainer
        else:
        # untrusted source
            self.tarbased = False
            self.jmeno = self.icontainer
            registry=re.search("([^/]*)", self.icontainer).groups()[0]
            if registry not in open('/etc/sysconfig/docker', 'rw').read():
                with open("/etc/sysconfig/docker", "a") as myfile:
                    myfile.write("INSECURE_REGISTRY='--insecure-registry $REGISTRY %s'" % registry)
        try:
            utils.process.run("systemctl status docker")
        except Exception as e:
            print e
            utils.process.run("systemctl restart docker")
            pass

    def pullContainer(self):
        if self.tarbased:
            utils.process.run("docker import %s %s" % (self.icontainer, self.jmeno))
        else:
            utils.process.run("docker pull %s" % self.icontainer)
        self.containerInfo = json.loads(utils.process.run("docker inspect --format='{{json .Config}}'  %s" % self.jmeno ).stdout)

    def start(self, args = "-it -d", command = "/bin/bash"):
        if not self.docker_id:
            if self.info.has_key('start'):
                self.docker_id = utils.process.run("%s -d %s" % (self.info['start'], self.jmeno)).stdout
            else:
                self.docker_id = utils.process.run("docker run %s %s %s" % (args, self.jmeno, command)).stdout

    def stop(self):
        try:
            utils.process.run("docker stop %s" % self.docker_id)
            utils.process.run("docker rm %s" % self.docker_id)
        except Exception as e:
            print e
            print "docker already removed"
            pass

    def run(self, command = "ls /", args=""):
        self.start()
        return utils.process.run("docker exec %s %s %s" % (args, self.docker_id, command))

    def checkLabel(self, key, value):
        if self.containerInfo['Labels'].has_key(key) and (value in self.containerInfo['Labels'][key]):
            return True
        return False

class RpmHelper(Test, CommonFunctions):
    """
    :avocado: disable
    """
    def setUp(self):
        self.loadconfig()
        #self.installroot=os.path.join("/opt", self.moduleName)
        #self.installroot="/"
        self.yumrepo=os.path.join("/etc","yum.repos.d","%s.repo" % self.moduleName)
        self.info = self.config['module']['rpm']
        self.prepare()
        self.prepareSetup()

    def tearDown(self):
        self.stop()

    def prepare(self):
        #if not os.path.exists(self.installroot):
        #    shutil.rmtree(self.installroot)
         #   os.makedirs(self.installroot)
        if not os.path.isfile(self.yumrepo):
            counter=0
            f=open(self.yumrepo, 'w')
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

    def prepareSetup(self):
        utils.process.run("dnf -y --disablerepo=* --enablerepo=%s* install %s rpm" % (self.moduleName, self.installroot, self.moduleName))
            
    def status(self, command = "systemctl status"):
        if self.info.has_key('status'):
            utils.process.run(self.info['status'])
        else:
            utils.process.run("%s %s" % (command, self.moduleName))
    
    def start(self, command = "systemctl start"):
        if self.info.has_key('start'):
            utils.process.run(self.info['start'])
        else:
            utils.process.run("%s %s" % (command, self.moduleName))
        time.sleep(2)

    def stop(self, command = "systemctl stop"):
        if self.info.has_key('stop'):
            utils.process.run(self.info['stop'])
        else:
            utils.process.run("%s %s" % (command, self.moduleName))

    def run(self, command = "ls /"):
        return utils.process.run(command)

if "docker" in MODULE:
    AvocadoTest = ContainerHelper
elif "rpm" in MODULE:
    AvocadoTest = RpmHelper
    
