#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Meta test family (MTF) is a tool to test components of a modular Fedora:
# https://docs.pagure.org/modularity/
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
import re
from avocado import utils
from common import *
from pdc_client import PDCClient
from timeoutlib import Retry

PDC_SERVER = "https://pdc.fedoraproject.org/rest_api/v1/unreleasedvariants"

def getBasePackageSet(modulesDict=None, isModule=True, isContainer=False):
    """
    Get list of base packages (for bootstrapping of various module types)
    It is used internally, you should not use it in case you don't know where to use it.

    :param modulesDict: dictionary of dependent modules
    :param isModule: bool is module
    :param isContainer: bool is contaner?
    :return: list of packages to install 
    """
    # nspawn container need to install also systemd to be able to boot
    out = []
    brmod = "base-runtime"
    brmod_profiles = ["container", "baseimage"]
    BASEPACKAGESET_WORKAROUND = ["systemd"]
    BASEPACKAGESET_WORKAROUND_NOMODULE = ["systemd", "yum"]
    pdc = None
    basepackageset = []
    if isModule:
        if modulesDict.has_key(brmod):
            print_info("Searching for packages base package set inside %s" % brmod)
            pdc = PDCParser()
            pdc.setLatestPDC(brmod, modulesDict[brmod])
            for pr in brmod_profiles:
                if pdc.getmoduleMD()['data']['profiles'].get(pr):
                    basepackageset = pdc.getmoduleMD(
                    )['data']['profiles'][pr]['rpms']
                    break
        if isContainer:
            out = basepackageset
        else:
            out = basepackageset + BASEPACKAGESET_WORKAROUND
    else:
        if isContainer:
            out = basepackageset
        else:
            out = basepackageset + BASEPACKAGESET_WORKAROUND_NOMODULE
    print_info("ALL packages to install:", out)
    return out

def get_repo_url(wmodule="base-runtime", wstream="master", fake=False):
    """
    Return URL location of rpm repository.
    It reads data from PDC and construct url locator.
    It is used to solve repos for dependent modules (eg. memcached is dependent on perl and baseruntime)

    :param wmodule: module name
    :param wstream: module stream
    :param fake:
    :return: str
    """
    if fake:
        return "http://mirror.vutbr.cz/fedora/releases/25/Everything/x86_64/os/"
    else:
        tmp_pdc = PDCParser()
        tmp_pdc.setLatestPDC(wmodule, wstream)
        return tmp_pdc.generateRepoUrl()


class PDCParser():
    """
    Class for parsing PDC data via some setters line setFullVersion, setViaFedMsg, setLatestPDC
    """

    def __getDataFromPdc(self):
        """
        Internal method, do not use it

        :return: None
        """
        # Using develop=True to not authenticate to the server
        pdc_session = PDCClient(PDC_SERVER, ssl_verify=True, develop=True)
        pdc_query = { 'variant_id' : self.name, 'active': True }
        if self.stream:
            pdc_query['variant_version'] = self.stream
        if self.version:
            pdc_query['variant_release'] = self.version
        try:
            mod_info = pdc_session(**pdc_query)
        except Exception as ex:
            raise PDCExc("Could not query PDC server", ex)
        if not mod_info or "results" not in mod_info.keys() or not mod_info["results"]:
            raise PDCExc("QUERY: %s is not available on PDC" % pdc_query)
        self.pdcdata = mod_info["results"][-1]
        self.modulemd = yaml.load(self.pdcdata["modulemd"])

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
        # rpmrepo = "http://kojipkgs.fedoraproject.org/repos/%s/latest/%s" % (
        #    self.pdcdata["koji_tag"] + "-build", ARCH)
        if get_if_remoterepos():
            rpmrepo = "%s/%s/os/" % (URLBASECOMPOSE, ARCH)
            return rpmrepo
        else:
            return self.createLocalRepoFromKoji()

    def generateGitHash(self):
        """
        Return string of generated commit hash fopr git, to switch to proper test version

        :return: str
        """
        return self.getmoduleMD()['data']['xmd']['mbs']['commit']

    def getmoduleMD(self):
        return self.modulemd

    def generateModuleMDFile(self):
        """
        Store moduleMD file locally from PDC to tempmodule.yaml file
        It should not be used ouside this library.

        :return: str url of file
        """
        omodulefile = MODULEFILE
        mdfile = open(omodulefile, mode="w")
        mdfile.write(yaml.dump(self.getmoduleMD()))
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
        x = self.getmoduleMD()
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

    def download_tagged(self,dirname):
        """
        Downloads packages to directory, based on koji tags
        It downloads just ARCH and noarch packages

        :param dirname: string
        :return: None
        """
        print_info("DOWNLOADING ALL packages for %s_%s_%s" % (self.name, self.stream, self.version))
        for foo in utils.process.run("koji list-tagged --quiet %s" % self.pdcdata["koji_tag"], verbose=is_debug()).stdout.split("\n"):
            pkgbouid = foo.strip().split(" ")[0]
            if len(pkgbouid) > 4:
                print_debug("DOWNLOADING: %s" % foo)

                @Retry(attempts=DEFAULTRETRYCOUNT * 10, timeout=DEFAULTRETRYTIMEOUT * 60, delay=DEFAULTRETRYTIMEOUT,
                       error=KojiExc(
                           "RETRY: Unbale to fetch package from koji after %d attempts" % (DEFAULTRETRYCOUNT * 10)))
                def tmpfunc():
                    a = utils.process.run(
                        "cd %s; koji download-build %s  -a %s -a noarch" %
                        (dirname, pkgbouid, ARCH), shell=True, verbose=is_debug(), ignore_status=True)
                    if a.exit_status == 1:
                        if "packages available for" in a.stdout.strip():
                            print_debug(
                                'UNABLE TO DOWNLOAD package (intended for other architectures, GOOD):', a.command)
                        else:
                            raise KojiExc(
                                'UNABLE TO DOWNLOAD package (KOJI issue, BAD):', a.command)

                tmpfunc()
        print_info("DOWNLOADING finished")

    def createLocalRepoFromKoji(self):
        """
        Return string of generated repository located LOCALLY
        It downloads all tagged packages and creates repo via createrepo

        :return: str
        """
        dir_prefix = BASEPATHDIR
        utils.process.run("{HOSTPACKAGER} install createrepo koji".format(
            **trans_dict), ignore_status=True)
        if is_recursive_download():
            dirname = os.path.join(dir_prefix,"localrepo_recursive")
        else:
            dirname = os.path.join(dir_prefix, "localrepo_%s_%s_%s" % (self.name, self.stream, self.version))
        absdir = os.path.abspath(dirname)
        # Test if directory contains repository, otherwise download everything again
        if os.path.exists(os.path.join(absdir,"repodata","repomd.xml")):
            pass
        else:
            os.mkdir(absdir)
            self.download_tagged(absdir)
            if is_recursive_download():
                allmodules = self.generateDepModules()
                for mo in allmodules:
                    localrepo = PDCParser()
                    localrepo.setLatestPDC(mo, allmodules[mo])
                    localrepo.download_tagged(dirname)

            utils.process.run(
                "cd %s; createrepo -v %s" %
                (absdir, absdir), shell=True, verbose=is_debug())
        return "file://%s" % absdir

if __name__ == "__main__":
    a = PDCParser()
    a.setLatestPDC(name="memcached", stream="f26")
    dependencies = a.generateDepModules()
    get_if_remoterepos = (lambda: True)
    assert dependencies == {'base-runtime': 'f26', 'shared-userspace': 'f26', 'perl': 'f26'}
    assert "https://kojipkgs.fedoraproject.org/compose/latest-Fedora-Modular-26/compose/Server/x86_64/os/" == a.generateRepoUrl()
    assert "URL=https://kojipkgs.fedoraproject.org/compose/latest-Fedora-Modular-26/compose/Server/x86_64/os/" in a.generateParams()
    assert "MODULE=nspawn" in a.generateParams()
    assert len(a.generateGitHash()) == 41
    assert "Memcached is a high-performance, distributed" in a.getmoduleMD()['data']['description']
