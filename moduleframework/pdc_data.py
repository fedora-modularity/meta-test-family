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
Module for PDC (Product definition Handling)
Construct repos
Download and create local repos
Construct parameters for automatization (CIs)
"""

import yaml
import os
import json
import urllib
import re
from avocado import utils
from common import *
from timeoutlib import Retry



class PDCParser():
    """
    Class for parsing PDC data via some setters line setFullVersion, setViaFedMsg, setLatestPDC
    """

    @Retry(attempts=20, timeout=DEFAULTRETRYTIMEOUT, delay=20)
    def __getDataFromPdc(self):
        """
        Internal method, do not use it

        :return: None
        """
        PDC = "%s/?variant_name=%s&variant_version=%s&variant_release=%s&active=True" % (
            PDCURL, self.name, self.stream, self.version)
        out=json.load(urllib.urlopen(PDC))["results"]
        if out:
            self.pdcdata = out[-1]
        else:
            raise BaseException("Unable to get data from PDC URL: %s" % PDC)

    def setFullVersion(self, nvr):
        """
        Set parameters of class via name-stream-version string
        Taskotron uses this format

        :param nvr:
        :return: None
        """
        self.name, self.stream, self.version = re.search(
            "(.*)-(.*)-(.*)", nvr).groups()
        self.__getDataFromPdc()

    def setViaFedMsg(self, yamlinp):
        """
        Sets parameters via RAW fedora message from message bus
        used by internal CI

        :param yamlinp: yaml input string
        :return:
        """
        raw = yaml.load(yamlinp)
        self.name = raw["msg"]["name"]
        self.stream = raw["msg"]["stream"]
        self.version = raw["msg"]["version"]
        self.__getDataFromPdc()

    def setLatestPDC(self, name, stream="master", version=""):
        """
        Most flexible method how to set name stream version for search

        :param name: name of module
        :param stream: optional
        :param version: optional
        :return:
        """
        self.name = name
        self.stream = stream
        self.version = version
        self.__getDataFromPdc()

    def generateRepoUrl(self):
        """
        Return string of generated repository located on fedora koji

        :return: str
        """
        rpmrepo = "http://kojipkgs.fedoraproject.org/repos/%s/latest/%s" % (
            self.pdcdata["koji_tag"] + "-build", ARCH)
        return rpmrepo

    def generateGitHash(self):
        """
        Return string of generated commit hash fopr git, to switch to proper test version

        :return: str
        """
        try:
            return self.pdcdata["scmurl"].split("#")[1]
        except BaseException:
            return "master"


    def generateModuleMDFile(self):
        """
        Store moduleMD file locally from PDC to tempmodule.yaml file
        It should not be used ouside this library.

        :return: str url of file
        """
        omodulefile = MODULEFILE
        mdfile = open(omodulefile, mode="w")
        mdfile.write(self.pdcdata["modulemd"])
        mdfile.close()
        return "file://%s" % os.path.abspath(omodulefile)

    def generateParams(self):
        """
        Return list of params what has to be set for automation like:
        MODULE=nspawn MODULEMDURL=file:///...  URL=kojirepo

        :return: list
        """
        output = []
        output.append("URL=%s" % self.generateRepoUrl())
        output.append("MODULEMDURL=%s" % self.generateModuleMDFile())
        output.append("MODULE=%s" % "nspawn")
        return output

    def generateDepModules(self):
        x = yaml.load(self.pdcdata["modulemd"])
        out = {}
        if x["data"].get("dependencies") and x["data"]["dependencies"].get("requires"):
            deps = x["data"]["dependencies"]["requires"]
            for dep in deps:
                a = PDCParser()
                a.setLatestPDC(dep, deps[dep])
                out.update(a.generateDepModules())
            out.update(deps)
        else:
            out = {}
        return out

    def createLocalRepoFromKoji(self):
        """
        Return string of generated repository located LOCALLY
        It downloads all tagged packages and creates repo via createrepo

        :return: str
        """
        utils.process.run("{HOSTPACKAGER} install createrepo koji".format(**trans_dict), ignore_status=True)
        dirname = "localrepo_%s_%s_%s" % (self.name, self.stream, self.version)
        absdir = os.path.abspath(dirname)
        if os.path.exists(absdir):
            pass
        else:
            os.mkdir(absdir)
            for foo in utils.process.run(
                    "koji list-tagged --quiet %s" % self.pdcdata["koji_tag"], verbose=is_debug()).stdout.split("\n"):
                pkgbouid = foo.strip().split(" ")[0]
                if len(pkgbouid) > 4:
                    print_info("DOWNLOADING: %s" % foo)
                    @Retry(attempts=2*60, timeout=2*60*60, delay=60)
                    def tmpfunc():
                        a = utils.process.run(
                            "cd %s; koji download-build %s  -a %s -a noarch" %
                            (absdir, pkgbouid, ARCH), shell=True, verbose=is_debug(),ignore_status=True)
                        if a.exit_status == 1:
                            if "packages available for" in a.stdout.strip():
                                print_info('UNABLE TO DOWNLOAD package (intended for other architectures, GOOD):', a.command)
                            else:
                                raise BaseException('UNABLE TO DOWNLOAD package (KOJI issue, BAD):', a.command)
                    tmpfunc()
            utils.process.run(
                "cd %s; createrepo -v %s" %
                (absdir, absdir), shell=True, verbose=is_debug())
        return "file://%s" % absdir

    def generateParamsLocalKojiPkgs(self):
        """
        Return list of params what has to be set for automation like (local repo):
        MODULE=nspawn MODULEMDURL=file:///...  URL=file:///localrepo

        :return: list
        """
        output = []
        output.append("URL=%s" % self.createLocalRepoFromKoji())
        output.append("MODULEMDURL=%s" % self.generateModuleMDFile())
        output.append("MODULE=%s" % "nspawn")
        return output
