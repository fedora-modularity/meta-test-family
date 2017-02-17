#!/usr/bin/python

import os
import sys
import re
import yaml
import json
from avocado import Test
from avocado import utils

class CommonFunctions():

    def loadconfig(self):
        config = os.environ.get('CONFIG') if os.environ.get('CONFIG') else "config.yaml"
        with open(config, 'r') as ymlfile:
            self.config = yaml.load(ymlfile)
            if self.config['document'] != 'modularity-testing':
                print "Bad config file"
                sys.exit(1)
            self.packages = self.config['packages']['rpms']

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
        self.name=None
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
            self.name="testcontainer"
            self.tarbased=True
        elif "docker.io" in self.info['container']:
        # Trusted source
            self.tarbased = False
            self.name = self.icontainer
        else:
        # untrusted source
            self.tarbased = False
            self.name = self.icontainer
            registry=re.search("([^/]*)", self.icontainer).groups()[0]
            if registry not in open('/etc/sysconfig/docker', 'rw').read():
                with open("/etc/sysconfig/docker", "a") as myfile:
                    myfile.write("INSECURE_REGISTRY='--insecure-registry $REGISTRY %s'" % registry)
        try:
            utils.process.run("systemctl status docker")
        except e:
            utils.process.run("systemctl restart docker")

    def pullContainer(self):
        if self.tarbased:
            utils.process.run("docker import %s %s" % (self.icontainer, self.name))
        else:
            utils.process.run("docker pull %s" % self.icontainer)
        self.containerInfo = json.loads(utils.process.run("docker inspect --format='{{json .Config}}'  %s" % self.name ).stdout)

    def start(self, args = "-it -d", command = "/bin/bash"):
        if self.info.has_key('start'):
            self.docker_id = utils.process.run("%s -d %s" % (self.info['start'], self.name)).stdout
        else:
            self.docker_id = utils.process.run("docker run %s %s %s" % (args, self.name, command)).stdout

    def stop(self):
        try:
            utils.process.run("docker stop %s" % self.docker_id)
            utils.process.run("docker rm %s" % self.docker_id)
        except e:
            print "docker already removed"

    def run(self, command = "ls /", args=""):
        
        return utils.process.run("docker exec %s %s %s" % (args, self.docker_id, command))

    
    def SanityConnection():
        return "bin" in self.run("ls /").stdout

    def checkLabel(self, key, value):
        if self.containerInfo['Labels'].has_key(key) and (value in self.containerInfo['Labels'][key]):
            return 0
        return 1

    def SanityLabels(self):
        for key,value in self.info['labels']:
                print self.checkLabel(key, value), key, value 
    
if "docker" in os.environ.get('MODULE'):
    AvocadoTest = ContainerHelper
    
