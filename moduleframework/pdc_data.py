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
from pdc_client import PDCClient
import core, common, mtfexceptions, timeoutlib


def get_module_nsv(name=None, stream=None, version=None):
    name = name or os.environ.get('MODULE_NAME')
    stream = stream or os.environ.get('MODULE_STREAM')
    version = version or os.environ.get('MODULE_VERSION')
    return {'name':name, 'stream':stream, 'version':version}


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
        if common.conf.get('pdc'):
            pdcdata = self.__getDataFromPdc(name=name, stream=stream, version=version)
            self.stream = pdcdata['stream']
            self.version = pdcdata['version']
        else:
            self.stream = modulensv['stream']
            self.version = modulensv['version']

    def __getDataFromPdc(self, name, stream, version, active=True):
        """
        Internal method, do not use it

        :return: None
        """
        if not self.pdcdata:
            pdc_query = {'name': name, 'active': active}
            if stream:
                pdc_query['stream'] = stream
            if version:
                pdc_query['version'] = version
            @timeoutlib.Retry(attempts=common.conf["generic"]["retrycount"], timeout=common.conf["generic"]["retrytimeout"], error=mtfexceptions.PDCExc("Could not query PDC server"))
            def retry_tmpfunc():
                # Using develop=True to not authenticate to the server
                pdc_session = PDCClient(common.conf["pdc"]["pdc_server"], ssl_verify=True, develop=True)
                core.print_debug(pdc_session, pdc_query)
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
        return common.get_base_compose()


    def generateGitHash(self):
        """
        Return string of generated commit hash fopr git, to switch to proper test version

        :return: str
        """
        return self.getmoduleMD()['data']['xmd']['mbs']['commit']

    def getmoduleMD(self):
        self.get_pdc_info()
        return self.modulemd

    def get_pdc_info(self):
        return self.__getDataFromPdc(name=self.name, stream=self.stream, version=self.version)

    def generateModuleMDFile(self):
        """
        Store moduleMD file locally from PDC to tempmodule.yaml file
        It should not be used ouside this library.

        :return: str url of file
        """
        omodulefile = common.conf["modularity"]["tempmodulefile"]
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
        core.print_debug("tree traverse from %s: %s"% (self.name, deps))
        for dep in deps:
            if dep not in parentdict:
                parentdict[dep] = deps[dep]
                a = PDCParser(dep, deps[dep])
                a.__generateDepModules_solver(parentdict=parentdict)

    def get_module_identifier(self):
        if self.version:
            return "%s:%s:%s" % (self.name, self.stream, self.version)
        elif self.stream:
            return "%s:%s" % (self.name, self.stream)
        else:
            return "%s" % (self.name)


class PDCParserKoji(PDCParserGeneral):
    def download_tagged(self,dirname):
        """
        Downloads packages to directory, based on koji tags
        It downloads just ARCH and noarch packages

        :param dirname: string
        :return: None
        """
        core.print_info("DOWNLOADING ALL packages for %s_%s_%s" % (self.name, self.stream, self.version))
        for foo in process.run("koji list-tagged --quiet %s" % self.get_pdc_info()["koji_tag"], verbose=core.is_debug()).stdout.split("\n"):
            pkgbouid = foo.strip().split(" ")[0]
            if len(pkgbouid) > 4:
                core.print_debug("DOWNLOADING: %s" % foo)

                @timeoutlib.Retry(attempts=common.conf["generic"]["retrycount"] * 10, timeout=common.conf["generic"]["retrytimeout"] * 60,
                       delay=common.conf["generic"]["retrytimeout"],
                       error=mtfexceptions.KojiExc(
                           "RETRY: Unbale to fetch package from koji after %d attempts" % (common.conf["generic"]["retrycount"] * 10)))
                def tmpfunc():
                    a = process.run(
                        "cd %s; koji download-build %s  -a %s -a noarch" %
                        (dirname, pkgbouid, common.conf["generic"]["arch"]), shell=True, verbose=core.is_debug(), ignore_status=True)
                    if a.exit_status == 1:
                        if "packages available for" in a.stdout.strip():
                            core.print_debug(
                                'UNABLE TO DOWNLOAD package (intended for other architectures, GOOD):', a.command)
                        else:
                            raise mtfexceptions.KojiExc(
                                'UNABLE TO DOWNLOAD package (KOJI issue, BAD):', a.command)

                tmpfunc()
        core.print_info("DOWNLOADING finished")

    def get_repo(self):
        """
        Return string of generated repository located LOCALLY
        It downloads all tagged packages and creates repo via createrepo

        :return: str
        """
        dir_prefix = common.conf["nspawn"]["basedir"]
        process.run("{HOSTPACKAGER} install createrepo koji".format(
            **common.trans_dict), ignore_status=True)
        if common.is_recursive_download():
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
            if common.is_recursive_download():
                allmodules = self.generateDepModules()
                for mo in allmodules:
                    localrepo = PDCParserKoji(mo, allmodules[mo])
                    localrepo.download_tagged(dirname)

            process.run(
                "cd %s; createrepo -v %s" %
                (absdir, absdir), shell=True, verbose=core.is_debug())
        return "file://%s" % absdir


class PDCParserODCS(PDCParserGeneral):
    compose_type = common.conf["odcs"]["compose_type"]
    odcsauth = common.conf["odcs"]["auth"]

    def get_repo(self):
        # import moved here, to avoid messages when you don't need to use ODCS
        from odcs.client.odcs import ODCS, AuthMech

        if self.odcsauth.get("auth_mech") == AuthMech.OpenIDC:
            if not self.odcsauth.get("openidc_token"):
                self.odcsauth["openidc_token"] = common.get_openidc_auth()
        odcs = ODCS(common.conf["odcs"]["url"], **self.odcsauth)
        core.print_debug("ODCS Starting module composing: %s" % odcs,
                    "%s compose for: %s" % (self.compose_type, self.get_module_identifier()))
        compose_builder = odcs.new_compose(self.get_module_identifier(),
                                           self.compose_type,
                                           **common.conf["odcs"]["new_compose_dict"])
        timeout_time=common.conf["odcs"]["timeout"]
        core.print_debug("ODCS Module compose started, timeout set to %ss" % timeout_time)
        compose_state = odcs.wait_for_compose(compose_builder["id"], timeout=timeout_time)
        core.print_debug("ODCS compose debug info for: %s" % self.get_module_identifier(), compose_state)
        if compose_state["state_name"] == "done":
            compose = "{compose}/{arch}/os".format(compose=compose_state["result_repo"], arch=common.conf["generic"]["arch"])
            core.print_info("ODCS Compose done, URL with repo file", compose)
            return compose
        else:
            raise mtfexceptions.PDCExc("ODCS: Failed to generate compose for module: %s" %
                                       self.get_module_identifier())


def get_repo_url(wmodule="base-runtime", wstream=None):
    """
    Return URL location of rpm repository.
    It reads data from PDC and construct url locator.
    It is used to solve repos for dependent modules (eg. memcached is dependent on perl and baseruntime)

    :param wmodule: module name
    :param wstream: module stream
    :return: str
    """

    tmp_pdc = PDCParser(wmodule, wstream)
    return tmp_pdc.get_repo()


PDCParser = PDCParserGeneral
if common.get_odcs_envvar():
    PDCParser = PDCParserODCS
elif not common.get_if_remoterepos():
    PDCParser = PDCParserKoji


def test_PDC_general_base_runtime():
    core.print_info(sys._getframe().f_code.co_name)
    parser = PDCParserGeneral("base-runtime", "master")
    assert not parser.generateDepModules()
    assert "module-" in parser.get_pdc_info()["koji_tag"]
    core.print_info(parser.get_repo())
    assert common.conf["compose"]["baseurlrepo"][:30] in parser.get_repo()
    core.print_info(parser.generateParams())
    assert len(parser.generateParams()) == 3
    assert "MODULE=nspawn" in " ".join(parser.generateParams())
    core.print_info("URL=%s" % common.conf["compose"]["baseurlrepo"][:30])
    assert "URL=%s" % common.conf["compose"]["baseurlrepo"][:30] in " ".join(parser.generateParams())


def test_PDC_general_nodejs():
    core.print_info(sys._getframe().f_code.co_name)
    parser = PDCParserGeneral("nodejs", "8")
    deps = parser.generateDepModules()
    core.print_info(deps)
    assert 'platform' in deps


def test_PDC_koji_nodejs():

    common.conf["nspawn"]["basedir"]="."
    core.print_info(sys._getframe().f_code.co_name)
    parser = PDCParserKoji("nodejs", "8")
    deps = parser.generateDepModules()
    core.print_info(deps)
    assert 'platform' in deps
    core.print_info(parser.get_repo())
    assert "file://" in parser.get_repo()
    assert os.path.abspath(common.conf["nspawn"]["basedir"]) in parser.get_repo()
    assert "MODULE=nspawn" in " ".join(parser.generateParams())
    assert "URL=file://" in " ".join(parser.generateParams())
    # TODO: this subtest is too slow, commented out
    #global common.is_recursive_download
    #common.is_recursive_download = lambda: True
    #core.print_info(parser.get_repo())


def test_PDC_ODCS_nodejs():
    core.print_info(sys._getframe().f_code.co_name)
    parser = PDCParserODCS("nodejs", "8")
    # TODO: need to setup MTF_ODCS variable with odcs token, and ODCS version at least 0.1.2
    # or your user will be asked to for token interactively
    if common.get_odcs_envvar():
        core.print_info(parser.get_repo())




#test_PDC_ODCS_nodejs()