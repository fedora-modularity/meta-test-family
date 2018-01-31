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
import os
import sys
from avocado.utils import process
from common import print_info, DEFAULTRETRYCOUNT, DEFAULTRETRYTIMEOUT, \
    get_if_remoterepos, BASEPATHDIR, MODULEFILE, print_debug,\
    is_debug, ARCH, is_recursive_download, trans_dict, get_odcs_auth
from moduleframework import mtfexceptions
from pdc_client import PDCClient
from timeoutlib import Retry
try:
    from odcs.client.odcs import ODCS, AuthMech
except:
    print_debug("ODCS  library cannot be imported. ODCS is not supported")


PDC_SERVER = "https://pdc.fedoraproject.org/rest_api/v1/unreleasedvariants"
ODCS_URL = "https://odcs.fedoraproject.org"
DEFAULT_MODULE_STREAM = "master"
BASE_REPO_URL = "https://kojipkgs.fedoraproject.org/compose/latest-Fedora-Modular-{}/compose/Server/{}/os"

def get_module_nsv(name=None, stream=None, version=None):
    name = name or os.environ.get('MODULE_NAME')
    stream = stream or os.environ.get('MODULE_STREAM') or DEFAULT_MODULE_STREAM
    version = version or os.environ.get('MODULE_VERSION')
    return {'name':name, 'stream':stream, 'version':version}


def get_base_compose():
    default_release = "27"
    release = os.environ.get("MTF_FEDORA_RELEASE") or default_release
    if release == "master":
        release = default_release
    compose_url = os.environ.get("MTF_COMPOSE_BASE") or BASE_REPO_URL.format(release, ARCH)
    return compose_url

class PDCParserGeneral():
    """
    Generic class for parsing PDC data (get repo leads to fedora official composes)
    """
    name = None
    stream = None
    version = None
    pdcdata = None
    modulemd = None
    moduledeps = None

    def __init__(self, name, stream=None, version=None):
        """
        Set basic parametrs, module names, streams, versions

        :param name: name of module
        :param stream: optional
        :param version: optional
        :return:
        """
        modulensv = get_module_nsv(name=name, stream=stream, version=version)
        self.name = modulensv['name']
        self.stream = modulensv['stream']
        self.version = modulensv['version']

    def __getDataFromPdc(self):
        """
        Internal method, do not use it

        :return: None
        """
        if not self.pdcdata:
            pdc_query = { 'variant_id' : self.name, 'active': True }
            if self.stream:
                pdc_query['variant_version'] = self.stream
            if self.version:
                pdc_query['variant_release'] = self.version
            @Retry(attempts=DEFAULTRETRYCOUNT, timeout=DEFAULTRETRYTIMEOUT, error=mtfexceptions.PDCExc("Could not query PDC server"))
            def retry_tmpfunc():
                # Using develop=True to not authenticate to the server
                pdc_session = PDCClient(PDC_SERVER, ssl_verify=True, develop=True)
                print_debug(pdc_session, pdc_query)
                return pdc_session(**pdc_query)
            mod_info = retry_tmpfunc()
            if not mod_info or "results" not in mod_info.keys() or not mod_info["results"]:
                raise mtfexceptions.PDCExc("QUERY: %s is not available on PDC" % pdc_query)
            self.pdcdata = mod_info["results"][-1]
            self.modulemd = yaml.load(self.pdcdata["modulemd"])
        return self.pdcdata


    def get_repo(self):
        """
        Return string of generated repository located on fedora koji

        :return: str
        """
        return get_base_compose()


    def generateGitHash(self):
        """
        Return string of generated commit hash fopr git, to switch to proper test version

        :return: str
        """
        return self.getmoduleMD()['data']['xmd']['mbs']['commit']

    def getmoduleMD(self):
        self.__getDataFromPdc()
        return self.modulemd

    def get_pdc_info(self):
        return self.__getDataFromPdc()

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
        output.append("URL=%s" % self.get_repo())
        output.append("MODULEMDURL=%s" % self.generateModuleMDFile())
        output.append("MODULE=%s" % "nspawn")
        return output

    def __get_module_requires(self):
        return self.getmoduleMD().get("data", {}).get("dependencies", {}).get("requires", {})

    def generateDepModules(self):
        if  self.moduledeps is None:
            rootdepdict = {}
            self.__generateDepModules_solver(parentdict=rootdepdict)
            self.moduledeps = rootdepdict
        return self.moduledeps

    def __generateDepModules_solver(self, parentdict):
        deps = self.__get_module_requires()
        print_debug("tree traverse from %s: %s"% (self.name, deps))
        for dep in deps:
            if dep not in parentdict:
                parentdict[dep] = deps[dep]
                a = PDCParser(dep, deps[dep])
                a.__generateDepModules_solver(parentdict=parentdict)

    def get_module_identifier(self):
        if self.version:
            return "%s-%s-%s" % (self.name, self.stream, self.version)
        elif self.stream:
            return "%s-%s" % (self.name, self.stream)
        else:
            return "%s-%s" % (self.name, "master")


class PDCParserKoji(PDCParserGeneral):
    def download_tagged(self,dirname):
        """
        Downloads packages to directory, based on koji tags
        It downloads just ARCH and noarch packages

        :param dirname: string
        :return: None
        """
        print_info("DOWNLOADING ALL packages for %s_%s_%s" % (self.name, self.stream, self.version))
        for foo in process.run("koji list-tagged --quiet %s" % self.get_pdc_info()["koji_tag"], verbose=is_debug()).stdout.split("\n"):
            pkgbouid = foo.strip().split(" ")[0]
            if len(pkgbouid) > 4:
                print_debug("DOWNLOADING: %s" % foo)

                @Retry(attempts=DEFAULTRETRYCOUNT * 10, timeout=DEFAULTRETRYTIMEOUT * 60, delay=DEFAULTRETRYTIMEOUT,
                       error=mtfexceptions.KojiExc(
                           "RETRY: Unbale to fetch package from koji after %d attempts" % (DEFAULTRETRYCOUNT * 10)))
                def tmpfunc():
                    a = process.run(
                        "cd %s; koji download-build %s  -a %s -a noarch" %
                        (dirname, pkgbouid, ARCH), shell=True, verbose=is_debug(), ignore_status=True)
                    if a.exit_status == 1:
                        if "packages available for" in a.stdout.strip():
                            print_debug(
                                'UNABLE TO DOWNLOAD package (intended for other architectures, GOOD):', a.command)
                        else:
                            raise mtfexceptions.KojiExc(
                                'UNABLE TO DOWNLOAD package (KOJI issue, BAD):', a.command)

                tmpfunc()
        print_info("DOWNLOADING finished")

    def get_repo(self):
        """
        Return string of generated repository located LOCALLY
        It downloads all tagged packages and creates repo via createrepo

        :return: str
        """
        dir_prefix = BASEPATHDIR
        process.run("{HOSTPACKAGER} install createrepo koji".format(
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
            if not os.path.exists(absdir):
                os.mkdir(absdir)
            self.download_tagged(absdir)
            if is_recursive_download():
                allmodules = self.generateDepModules()
                for mo in allmodules:
                    localrepo = PDCParserKoji(mo, allmodules[mo])
                    localrepo.download_tagged(dirname)

            process.run(
                "cd %s; createrepo -v %s" %
                (absdir, absdir), shell=True, verbose=is_debug())
        return "file://%s" % absdir


class PDCParserODCS(PDCParserGeneral):
    compose_type = "module"
    auth_token = get_odcs_auth()

    def get_repo(self):
        odcs = ODCS(ODCS_URL, auth_mech=AuthMech.OpenIDC, openidc_token=self.auth_token)
        print_debug("ODCS Starting module composing: %s" % odcs,
                    "%s compose for: %s" % (self.compose_type, self.get_module_identifier()))
        compose_builder = odcs.new_compose(self.get_module_identifier(), self.compose_type)
        timeout_time=600
        print_debug("ODCS Module compose started, timeout set to %ss" % timeout_time)
        compose_state = odcs.wait_for_compose(compose_builder["id"], timeout=timeout_time)
        if compose_state["state_name"] == "done":
            compose = "{compose}/{arch}/os".format(compose=compose_state["result_repo"], arch=ARCH)
            print_info("ODCS Compose done, URL with repo file", compose)
            return compose
        else:
            raise mtfexceptions.PDCExc("ODCS: Failed to generate compose for module: %s" %
                                       self.get_module_identifier())

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
    BASEPACKAGESET_WORKAROUND = ["systemd"]
    BASEPACKAGESET_WORKAROUND_NOMODULE = BASEPACKAGESET_WORKAROUND + ["dnf"]
    # https://pagure.io/fedora-kickstarts/blob/f27/f/fedora-modular-container-base.ks
    BASE_MODULAR_CONTAINER = ["rootfiles", "tar", "vim-minimal", "dnf", "dnf-yum", "sssd-client"]
    # https://pagure.io/fedora-kickstarts/blob/f27/f/fedora-modular-container-common.ks
    BASE_MODULAR = ["fedora-modular-release", "bash", "coreutils-single", "glibc-minimal-langpack",
                    "libcrypt", "rpm", "shadow-utils", "sssd-client", "util-linux"]
    if isModule:
        if isContainer:
            out =  BASE_MODULAR_CONTAINER
        else:

            out = BASE_MODULAR + BASEPACKAGESET_WORKAROUND
    else:
        if isContainer:
            out = []
        else:
            out = BASEPACKAGESET_WORKAROUND_NOMODULE
    print_info("Base packages to install:", out)
    return out


def get_repo_url(wmodule="base-runtime", wstream="master"):
    """
    Return URL location of rpm repository.
    It reads data from PDC and construct url locator.
    It is used to solve repos for dependent modules (eg. memcached is dependent on perl and baseruntime)

    :param wmodule: module name
    :param wstream: module stream
    :param fake:
    :return: str
    """

    tmp_pdc = PDCParser(wmodule, wstream)
    return tmp_pdc.get_repo()


PDCParser = PDCParserGeneral
if get_odcs_auth():
    PDCParser = PDCParserODCS
elif not get_if_remoterepos():
    PDCParser = PDCParserKoji

def test_PDC_general_base_runtime():
    print_info(sys._getframe().f_code.co_name)
    parser = PDCParserGeneral("base-runtime", "master")
    assert not parser.generateDepModules()
    assert "module-" in parser.get_pdc_info()["koji_tag"]
    print_info(parser.get_repo())
    assert BASE_REPO_URL[:30] in parser.get_repo()
    print_info(parser.generateParams())
    assert len(parser.generateParams()) == 3
    assert "MODULE=nspawn" in " ".join(parser.generateParams())
    print_info("URL=%s" % BASE_REPO_URL[:30])
    assert "URL=%s" % BASE_REPO_URL[:30] in " ".join(parser.generateParams())

def test_PDC_general_nodejs():
    print_info(sys._getframe().f_code.co_name)
    parser = PDCParserGeneral("nodejs", "8")
    deps = parser.generateDepModules()
    print_info(deps)
    assert 'platform' in deps
    assert 'host' in deps
    assert 'python2' in deps
    assert 'python3' in deps

def test_PDC_koji_nodejs():
    global BASEPATHDIR
    BASEPATHDIR = "."

    print_info(sys._getframe().f_code.co_name)
    parser = PDCParserKoji("nodejs", "8")
    deps = parser.generateDepModules()
    print_info(deps)
    assert 'platform' in deps
    assert 'host' in deps
    assert 'python2' in deps
    assert 'python3' in deps
    print_info(parser.get_repo())
    assert "file://" in parser.get_repo()
    assert os.path.abspath(BASEPATHDIR) in parser.get_repo()
    assert "MODULE=nspawn" in " ".join(parser.generateParams())
    assert "URL=file://" in " ".join(parser.generateParams())
    # TODO: this subtest is too slow, commented out
    #global is_recursive_download
    #is_recursive_download = lambda: True
    #print_info(parser.get_repo())

def test_PDC_ODCS_nodejs():
    print_info(sys._getframe().f_code.co_name)
    parser = PDCParserODCS("nodejs", "8")
    # TODO: need to setup MTF_ODCS variable with odcs token, and ODCS version at least 0.1.2
    # or your user will be asked to for token interactively
    if get_odcs_auth():
        print_info(parser.get_repo())




#test_PDC_ODCS_nodejs()