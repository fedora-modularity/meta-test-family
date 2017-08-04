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
It provides some general functions
"""

import netifaces
import socket
import os
import urllib
import yaml

from avocado.utils import process

from moduleframework.exceptions import *
from moduleframework.compose_info import ComposeParser

defroutedev = netifaces.gateways().get('default').values(
)[0][1] if netifaces.gateways().get('default') else "lo"
hostipaddr = netifaces.ifaddresses(defroutedev)[2][0]['addr']
hostname = socket.gethostname()
dusername = "test"
dpassword = "test"
ddatabase = "basic"
hostpackager = "yum -y"
guestpackager = "microdnf"
if os.path.exists('/usr/bin/dnf'):
    hostpackager = "dnf -y"
ARCH = "x86_64"

# translation table for config.yaml files syntax is {VARIABLE} in config file
trans_dict = {"HOSTIPADDR": hostipaddr,
              "GUESTIPADDR": hostipaddr,
              "DEFROUTE": defroutedev,
              "HOSTNAME": hostname,
              "ROOT": "/",
              "USER": dusername,
              "PASSWORD": dpassword,
              "DATABASENAME": ddatabase,
              "HOSTPACKAGER": hostpackager,
              "GUESTPACKAGER": guestpackager,
              "GUESTARCH": ARCH,
              "HOSTARCH": ARCH
              }


BASEPATHDIR = "/opt"
PDCURL = "https://pdc.fedoraproject.org/rest_api/v1/unreleasedvariants"
URLBASECOMPOSE = "https://kojipkgs.fedoraproject.org/compose/latest-Fedora-Modular-26/compose/Server"
REPOMD = "repodata/repomd.xml"
MODULEFILE = 'tempmodule.yaml'
# default value of process timeout in sec
DEFAULTPROCESSTIMEOUT = 2 * 60
DEFAULTRETRYCOUNT = 3
# time in seconds
DEFAULTRETRYTIMEOUT = 30
DEFAULTNSPAWNTIMEOUT = 10


def is_debug():
    return bool(os.environ.get("DEBUG"))


def is_not_silent():
    return not is_debug()


def print_info(*args):
    """
    Print data to selected output in case you are not in testing class, there is self.log

    :param args: object
    :return: None
    """
    for arg in args:
        out = arg
        if isinstance(arg, basestring):
            try:
                out = arg.format(**trans_dict)
            except KeyError:
                raise ModuleFrameworkException(
                    "String is formatted by using trans_dict, if you want to use brackets { } in your code please use {{ or }}, possible values in trans_dict are:",
                    trans_dict)
        print >> sys.stderr, out


def print_debug(*args):
    """
    Print data to selected output in case you are not in testing class, there is self.log
    In case DEBUG variable is set

    :param args: object
    :return: None
    """
    if is_debug():
        print_info(*args)

def is_recursive_download():
    """
    Purpose: Workaround for taskotron
    It changes behaviour of createLocalRepoFromKoji fuction of pdc_data module.
    It tries to download all packages with all dependent modules, not just for one module.
    It fixes issue with taskotron issues caused by checking stdout/stderr activity,
    after 15 minutes without any output it is killed.

    :return: bool
    """
    return bool(os.environ.get("MTF_RECURSIVE_DOWNLOAD"))


def get_if_do_cleanup():
    """
    Returns boolean value in case variable is set.
     It is used internally in code

    :return: bool
    """
    cleanup = os.environ.get('MTF_DO_NOT_CLEANUP')
    return not bool(cleanup)


def get_if_remoterepos():
    """
    Returns boolean value in case variable is set.
    It is used internally in code

    :return: bool
    """
    rreps = os.environ.get('MTF_REMOTE_REPOS')
    return bool(rreps)


def get_if_module():
    """
    Returns boolean value in case variable is set.
    It is used internally in code

    :return: bool
    """
    rreps = os.environ.get('MTF_DISABLE_MODULE')
    return not bool(rreps)


def sanitize_text(text, replacement="_"):

    """
    Replace invalid characters in a string.

    invalid_chars=["/", ";", "&", ">", "<", "|"]

    :param text: string
    :param replacement: replacement char, default: "_"
    :return: string
    """
    invalid_chars=["/", ";", "&", ">", "<", "|"]
    for char in invalid_chars:
        if char in text:
            text = text.replace(char, replacement)
    return text


def sanitize_cmd(cmd):
    """
    Do escaping of characters for command inside apostrophes

    :param cmd: string
    :return: string
    """
    escaping_chars = ['"']
    for char in escaping_chars:
        if char in cmd:
            cmd = cmd.replace(char, '\\'.join(char))
    return cmd


def get_profile():
    """
    Return profile name string

    :return: str
    """
    amodule = os.environ.get('PROFILE')
    if not amodule:
        amodule = "default"
    return amodule


def get_url():
    """
    Return actual URL if overwritten by
    env variable "URL"

    It redefines location of testing subject

    :return:
    """
    amodule = os.environ.get('URL')
    return amodule


def get_config():
    """
    Read the module's configuration file

    :default: ``./config.yaml`` in the ``tests`` directory of the module's root directory
    :envvar: **CONFIG=path/to/file** overrides default value.
    :return: str
    """
    cfgfile = os.environ.get('CONFIG') or './config.yaml'
    try:
       with open(cfgfile, 'r') as ymlfile:
           xcfg = yaml.load(ymlfile.read())
           return xcfg
    except IOError:
       raise ConfigExc(
           "Error: File '%s' doesn't appear to exist or it's not a YAML file." %
            cfgfile + " " +
           "Tip: If the CONFIG envvar is not set, mtf-generator looks for './config'.")


def get_compose_url():
    """
    Return Compose Url if set in config or via
    env variable COMPOSEURL

    :return: str
    """
    compose = os.environ.get('COMPOSEURL')
    readconfig = CommonFunctions()
    readconfig.loadconfig()
    if compose is None:
        if readconfig.config.get("compose-url"):
            compose = readconfig.config.get("compose-url")
        elif readconfig.config['module']['rpm'].get("repo"):
            compose = readconfig.config['module']['rpm'].get("repo")
        else:
            compose = readconfig.config['module']['rpm'].get("repos")[0]
    return compose


def get_modulemd():
    """
    Return dict of moduleMD file for module, It is read from config, from module-url section,
    if not defined it reads modulemd file from compose-url in case of set, or there is used
    env variable MODULEMDURL (eventually COMPOSEURL) for that

    :return: dict
    """
    mdf = os.environ.get('MODULEMDURL')
    readconfig = CommonFunctions()
    readconfig.loadconfig()
    try:
        if mdf:
            return mdf
        elif readconfig.config.get("modulemd-url"):
            return readconfig.config.get("modulemd-url")
        else:
            a = ComposeParser(get_compose_url())
            b = a.variableListForModule(readconfig.config.get("name"))
            return [x[12:] for x in b if 'MODULEMDURL=' in x][0]
    except AttributeError:
        return None


class CommonFunctions(object):
    """
    Basic class doing configuration reading and allow do commands on host machine
    """
    config = None
    modulemdConf = None

    def __init__(self, *args, **kwargs):
        self.config = None
        self.modulemdConf = None
        self.moduleName = None
        self.source = None
        self.arch = None
        self.dependencylist = {}
        self.moduledeps = None
        # general use case is to have forwarded services to host (so thats why it is same)
        self.ipaddr = trans_dict["HOSTIPADDR"]
        trans_dict["GUESTARCH"] = self.getArch()

    def getArch(self):
        """
        get system architecture string

        :return: str
        """
        out = self.runHost(command='uname -m', verbose=False).stdout.strip()
        return out

    def runHost(self, command="ls /", **kwargs):
        """
        Run commands on host

        :param command: command to exectute
        :param kwargs: (avocado process.run) params like: shell, ignore_status, verbose
        :return: avocado.process.run
        """
        try:
            formattedcommand = command.format(**trans_dict)
        except KeyError:
            raise ModuleFrameworkException(
                "Command is formatted by using trans_dict, if you want to use brackets { } in your code please use {{ "
                "or }}, possible values in trans_dict are:",
                trans_dict)
        return process.run("%s" % formattedcommand, **kwargs)

    def installTestDependencies(self, packages=None):
        """
        Which packages install to host system to satisfy environment

        :param packages: List of packages, if not set, it will install rpms from config.yaml
        :return: None
        """
        if not packages:
            typo = 'testdependecies' in self.config
            if typo:
                warnings.warn("'testdependecies' is a typo, please fix",
                              DeprecationWarning)

            # try section without typo first
            packages = self.config.get('testdependencies', {}).get('rpms')
            if packages:
                if typo:
                    warnings.warn("preferring section without typo")
            else:
                # fall back to mistyped test dependency section
                packages = self.config.get('testdependecies', {}).get('rpms')

        if packages:
            self.runHost(
                "{HOSTPACKAGER} install " +
                " ".join(packages),
                ignore_status=True, verbose=is_not_silent())

    def loadconfig(self):
        """
        Load configuration from config.yaml file (it is better to call this explicitly, than in
        __init__ method for our purposes)

        :return: None
        """
        try:
            self.config = get_config()
            self.moduleName = sanitize_text(self.config['name'])
            self.source = self.config.get('source') if self.config.get(
                'source') else self.config['module']['rpm'].get('source')
        except ValueError:
            pass

    def getPackageList(self, profile=None):
        """
        Return list of packages what has to be installed inside module

        :param profile: get list for intended profile instead of default method for searching
        :return: list of packages (rpms)
        """
        out = []
        if not profile:
            if 'packages' in self.config:
                packages_rpm = self.config['packages'].get('rpms') if self.config[
                    'packages'].get('rpms') else []
                packages_profiles = []
                for x in self.config['packages'].get('profiles') if self.config[
                    'packages'].get('profiles') else []:
                    packages_profiles = packages_profiles + \
                                        self.getModulemdYamlconfig()['data']['profiles'][x]['rpms']
                out += packages_rpm + packages_profiles

            elif self.getModulemdYamlconfig()['data'].get('profiles') and self.getModulemdYamlconfig()['data'][
                'profiles'].get(get_profile()):
                out += self.getModulemdYamlconfig()['data']['profiles'][get_profile()]['rpms']
            else:
                # fallback solution when it is not known what to install
                out.append("bash")
        else:
            out += self.getModulemdYamlconfig()['data']['profiles'][profile]['rpms']
        print_info("PCKGs to install inside module:", out)
        return out

    def getModuleDependencies(self):
        return self.dependencylist

    def getModulemdYamlconfig(self, urllink=None):
        """
        Return moduleMD file yaml object.
        It can be used also for loading another yaml file via url parameter

        :param urllink: load this url instead of default one defined in config, or redefined by vaiable CONFIG
        :return: dict
        """
        try:
            if urllink:
                ymlfile = urllib.urlopen(urllink)
                cconfig = yaml.load(ymlfile)
                link = cconfig
            elif not get_if_module():
                trans_dict["GUESTPACKAGER"] = "yum -y"
                link = {"data": {}}
            else:
                if self.config is None:
                    self.loadconfig()
                if not self.modulemdConf:
                    modulemd = get_modulemd()
                    if modulemd:
                        ymlfile = urllib.urlopen(modulemd)
                        self.modulemdConf = yaml.load(ymlfile)
                link = self.modulemdConf
            return link
        except IOError as e:
            raise ConfigExc("Cannot load file")

    def getIPaddr(self):
        """
        Return ip addr string of guest machine
        In many cases it should be same as host machine and port should be forwarded to host

        :return: str
        """
        return self.ipaddr

