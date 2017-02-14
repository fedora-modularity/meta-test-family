#!/usr/bin/python

import os
import re
from avocado import utils

RHKEY = "fd431d51"

class ContainerHelper():
    def __init__(self, icontainer):
        #brew-pulp-docker01.web.prod.ext.phx2.redhat.com:8888/rhel7/cockpit-ws:122-5
        #/mnt/redhat/brewroot/packages/cockpit-ws-docker/131/1/images/docker-image-sha256:71df4da82ff401d88e31604439b5ce67563e6bae7056f75f8f6dc715b64b4e02.x86_64.tar.gz
        self.tarbased=True
        self.name="testcontainer"
        self.icontainer = icontainer
        self.prepareEnv()
        self.startDocker()
        self.pullImage()
        
        
    def prepareEnv(self):
        process.run("yum -y install docker")

    def startDocker(self):
        if not ".tar.gz" in self.icontainer:
            self.tarbased = False
            registry=re.search("([^/]*)", self.icontainer).groups()[0]
            if registry not in open('/etc/sysconfig/docker', 'rw').read()):
                with open("/etc/sysconfig/docker", "a") as myfile:
                    myfile.write("INSECURE_REGISTRY='--insecure-registry $REGISTRY %s'" % registry)
            process.run("system restart docker")

    def pullImage(self):
        if self.tarbased:
            process.run("docker import %s %s" % (self.icontainer, self.name))
        else:
            process.run("docker pull %s" % self.icontainer)
            self.name = self.icontainer
    

    def containerExec(self, args = "-t -i", command = "/bin/bash"):
        process.run("docker run %s %s %s" % (args, self.name, command))
        process.run("docker ps | grep  %s" % self.name)
        self.docker_id = process.run("docker ps | grep %s |cut -d " " -f 1" % self.name,shell=True).stdout

    def containerStop():
        process.run("docker stop %s" % self.docker_id)
        process.run("docker rm %s" % self.docker_id)
    

    def cockpitSigning():
        process.run("docker run --entrypoint /bin/bash %s -c 'ls / | grep bin'" % self.name , shell = True)
        packages = process.run("docker run --entrypoint /bin/bash %s -c 'rpm -qa --qf=\"%{name}-%{version}-%{release} %{SIGPGP:pgpsig}\n\"'")
        process.run("docker run --entrypoint /bin/bash %s -c 'yum repolist | grep \"repolist: 0\"'", shell = True)

    def CockcpitLabelCheck(){
        XLABEL=$@
        rlRun "docker inspect $ATOMIC |grep '$XLABEL'"
}



if __name__ == '__main__':
    main()
