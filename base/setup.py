#!/usr/bin/python
from __future__ import print_function
import glob
from base import moduleframework
from avocado import utils


class Module(moduleframework.CommonFunctions):

    def __init__(self):
        self.loadconfig()
        self.yamlconfig = self.getModulemdYamlconfig()
        self.profile = moduleframework.PROFILE if moduleframework.PROFILE else "default"
        self.whattoinstall = self.yamlconfig['data']['profiles'][self.profile]
        self.rootdir = "/tmp/tmpmodule1"
        self.rpmsrepo = self.rootdir + "/rpms"
        self.rpmsinstalled = self.rootdir + "/installed"
        utils.process.run("mkdir -p %s" % self.rootdir)
        utils.process.run("mkdir -p %s" % self.rpmsrepo)
        utils.process.run("mkdir -p %s" % self.rpmsinstalled)
        self.baseruntimeyaml = self.getModulemdYamlconfig(
            "https://raw.githubusercontent.com/fedora-modularity/check_modulemd/develop/examples-modulemd/base-runtime.yaml")

    def CreateLocalRepo(self):
        allmodulerpms = " ".join(self.whattoinstall['rpms'])
        allbasertrpms = " ".join(self.baseruntimeyaml['data'][
                                 'profiles']['default']['rpms'])
        utils.process.run(
            "yumdownloader --destdir=%s --resolve %s %s" %
            (self.rpmsrepo, allmodulerpms, allbasertrpms))
        utils.process.run(
            "cd %s; createrepo --database %s" %
            (self.rpmsrepo, self.rpmsrepo), shell=True)
        print("file://%s" % self.rpmsrepo)

    def CreateContainer(self):
        localfiles = glob.glob('%s/*.rpm' % self.rpmsrepo)
        utils.process.run(
            "dnf -y install --disablerepo=* --allowerasing --installroot=%s %s" %
            (self.rpmsinstalled, " ".join(localfiles)))
        print("file://%s" % self.rpmsrepo)

m = Module()
m.CreateLocalRepo()
m.CreateContainer()
