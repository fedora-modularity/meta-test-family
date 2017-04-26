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

import yaml
import os
import json
import urllib
import re
import sys
from avocado import utils
import shutil

ARCH = "x86_64"
PDCURL = "https://pdc.fedoraproject.org/rest_api/v1/unreleasedvariants"


class PDCParser():

    def __getDataFromPdc(self):
        PDC = "%s/?variant_name=%s&variant_version=%s&variant_release=%s" % (
            PDCURL, self.name, self.stream, self.version)
        self.pdcdata = json.load(urllib.urlopen(PDC))["results"][-1]

    def setFullVersion(self, nvr):
        self.name, self.stream, self.version = re.search(
            "(.*)-(.*)-(.*)", nvr).groups()
        self.__getDataFromPdc()

    def setViaFedMsg(self, yamlinp):
        raw = yaml.load(yamlinp)
        self.name = raw["msg"]["name"]
        self.stream = raw["msg"]["stream"]
        self.version = raw["msg"]["version"]
        self.__getDataFromPdc()

    def setLatestPDC(self, name, stream="master", version=""):
        self.name = name
        self.stream = stream
        self.version = version
        self.__getDataFromPdc()

    def generateRepoUrl(self):
        rpmrepo = "http://kojipkgs.fedoraproject.org/repos/%s/latest/%s" % (
            self.pdcdata["koji_tag"], ARCH)
        return rpmrepo

    def generateModuleMDFile(self):
        omodulefile = "tempmodule.yaml"
        mdfile = open(omodulefile, mode="w")
        mdfile.write(self.pdcdata["modulemd"])
        mdfile.close()
        return "file://%s" % os.path.abspath(omodulefile)

    def generateParams(self):
        output = []
        output.append("URL=%s" % self.generateRepoUrl())
        output.append("MODULEMDURL=%s" % self.generateModuleMDFile())
        output.append("MODULE=%s" % "nspawn")
        return output

    def createLocalRepoFromKoji(self):
        utils.process.run("dnf -y install createrepo koji", ignore_status=True)
        dirname = "localrepo_%s_%s_%s" % (self.name, self.stream, self.version)
        absdir = os.path.abspath(dirname)
        if os.path.exists(absdir):
            pass
        else:
            os.mkdir(absdir)
            for foo in utils.process.run(
                    "koji list-tagged --quiet %s" % self.pdcdata["koji_tag"]).stdout.split("\n"):
                pkgbouid = foo.strip().split(" ")[0]
                if len(pkgbouid) > 4:
                    print >> sys.stderr, "DOWNLOADING:", foo
                    try:
                        utils.process.run(
                            "cd %s; koji download-build %s  -a %s -a noarch" %
                            (absdir, pkgbouid, ARCH), shell=True)
                    except:
                        print >> sys.stderr, 'UNABLE TO DOWNLOAD:', "cd %s; koji download-build %s  -a %s -a noarch" % (absdir, pkgbouid, ARCH)
                        pass
            utils.process.run(
                "cd %s; createrepo -v %s" %
                (absdir, absdir), shell=True)
        return "file://%s" % absdir

    def generateParamsLocalKojiPkgs(self):
        output = []
        output.append("URL=%s" % self.createLocalRepoFromKoji())
        output.append("MODULEMDURL=%s" % self.generateModuleMDFile())
        output.append("MODULE=%s" % "nspawn")
        return output
