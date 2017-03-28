#!/usr/bin/python

import yaml
import sys
import os

ARCH="x86_64"

class FedMsgParser():
    def __init__(self,yamlinp):
        self.out = []
        raw = yaml.load(yamlinp)
        #"kojipkgs.fedoraproject.org/repos/module-" + module_name + "-" + module_stream + "/latest"
        self.topic=raw["topic"]
        if self.topic == "org.fedoraproject.prod.mbs.module.state.change":
            self.out = self.modulechangemessage(raw["msg"])

    def modulechangemessage(self,msg):
        self.rpmrepo = "http://kojipkgs.fedoraproject.org/repos/module-%s-%s-%s/latest/%s" % (
            msg["name"], msg["stream"], msg["version"], ARCH )

        omodulefile = "module.yaml"
        mdfile = open(omodulefile,mode = "w")
        mdfile.write(msg["modulemd"])
        mdfile.close()
        output = []
        output.append("URL=%s" % self.rpmrepo)
        output.append("MODULEMDURL=file://%s" % os.path.abspath(omodulefile))
        output.append("MODULE=rpm")
        return output

stdinput = "".join(sys.stdin.readlines()).strip()
a=FedMsgParser(stdinput)
print " ".join(a.out)