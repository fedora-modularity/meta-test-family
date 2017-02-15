#!/usr/bin/python

import os
import re
import yaml
from avocado import Test
from avocado import utils
from avocado import main

RHKEY = "fd431d51"

class CommonFunctions(Test):
    """
    :avocado: disable
    """
    def __init__(self, config="config.yaml"):
        with open(config, 'r') as ymlfile:
            self.config = yaml.load(ymlfile)

class ContainerHelper(CommonFunctions):
    def __init__(self, icontainer):
        #brew-pulp-docker01.web.prod.ext.phx2.redhat.com:8888/rhel7/cockpit-ws:122-5
        #/mnt/redhat/brewroot/packages/cockpit-ws-docker/131/1/images/docker-image-sha256:71df4da82ff401d88e31604439b5ce67563e6bae7056f75f8f6dc715b64b4e02.x86_64.tar.gz
        self.tarbased=True
        self.name="testcontainer"
        self.icontainer = icontainer
        self.prepare()
        self.start()
        self.pull()

    def prepare(self):
        process.run("yum -y install docker")

    def start(self):
        if not ".tar.gz" in self.icontainer:
            self.tarbased = False
            registry=re.search("([^/]*)", self.icontainer).groups()[0]
            if registry not in open('/etc/sysconfig/docker', 'rw').read()):
                with open("/etc/sysconfig/docker", "a") as myfile:
                    myfile.write("INSECURE_REGISTRY='--insecure-registry $REGISTRY %s'" % registry)
            process.run("system restart docker")

    def pull(self):
        if self.tarbased:
            process.run("docker import %s %s" % (self.icontainer, self.name))
        else:
            process.run("docker pull %s" % self.icontainer)
            self.name = self.icontainer
    

    def exec(self, command = "ls /", args=""):
        return process.run("docker exec %s %s %s" % (args, self.docker_id, command))

    def run(self, args = "-it -d", command = "/bin/bash"):
        self.docker_id = process.run("docker run %s %s %s" % (args, self.name, command)).stdout


    def stop():
        process.run("docker stop %s" % self.docker_id)
        process.run("docker rm %s" % self.docker_id)

    def signing():
        # TODO not working because of "'
        if "bin" in self.containerExec(args="--entrypoint /bin/bash",command="ls /"): ...
        if "repolist: 0" in self.containerExec(args="--entrypoint /bin/bash",command="yum repolist"): ...
        packages=self.containerExec(args="--entrypoint /bin/bash",command='rpm -qa --qf="%{name}-%{version}-%{release} %{SIGPGP:pgpsig}\n"').stdout

    def labels(self,text):
        if text in process.run("docker inspect %s"):...

# to have a general class
if 
dockerGeneral config
    

if __name__ == '__main__':
    main()
