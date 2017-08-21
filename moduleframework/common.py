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
Custom configuration and debugging library.
"""

import netifaces
import socket
import os
import urllib
import yaml
import warnings

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
__rh_release = '/etc/redhat-release'
if os.path.exists(__rh_release):
    hostpackager = "yum -y"
    guestpackager = "microdnf"
    if os.path.exists('/usr/bin/dnf'):
        hostpackager = "dnf -y"
else:
    hostpackager = "apt-get -y"
    guestpackager = "dnf"
ARCH = "x86_64"

# translation table for {VARIABLE} in the config.yaml file
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
# default value of process timeout in seconds
DEFAULTPROCESSTIMEOUT = 2 * 60
DEFAULTRETRYCOUNT = 3
# time in seconds
DEFAULTRETRYTIMEOUT = 30
DEFAULTNSPAWNTIMEOUT = 10


def is_debug():
    """
    Return the **DEBUG** envvar.

    :return: bool
    """
    return bool(os.environ.get("DEBUG"))


def is_not_silent():
    """
    Return the opposite of the **DEBUG** envvar.

    :return: bool
    """
    return is_debug()


def print_info(*args):
    """
    Print information from the expected stdout and
    stderr files from the native test scope.

    See `Test log, stdout and stderr in native Avocado modules
    <https://avocado-framework.readthedocs.io/en/latest/WritingTests.html
    #test-log-stdout-and-stderr-in-native-avocado-modules>`_ for more information.

    :param args: object
    :return: None
    """
    for arg in args:
        result = arg
        if isinstance(arg, basestring):
            try:
                result = arg.format(**trans_dict)
            except KeyError:
                raise ModuleFrameworkException(
                    "String is formatted by using trans_dict. If you want to use "
                    "brackets { } in your code, please use double brackets {{  }}."
                    "Possible values in trans_dict are: %s"
                    % trans_dict)
        print >> sys.stderr, result


def print_debug(*args):
    """
    Print information from the expected stdout and
    stderr files from the native test scope if
    the **DEBUG** envvar is set to True.

    See `Test log, stdout and stderr in native Avocado modules
    <https://avocado-framework.readthedocs.io/en/latest/WritingTests.html
    #test-log-stdout-and-stderr-in-native-avocado-modules>`_ for more information.

    :param args: object
    :return: None
    """
    if is_debug():
        print_info(*args)

def is_recursive_download():
    """
    Return the **MTF_RECURSIVE_DOWNLOAD** envvar.

    :return: bool
    """
    return bool(os.environ.get("MTF_RECURSIVE_DOWNLOAD"))

def get_if_do_cleanup():
    """
    Return the **MTF_DO_NOT_CLEANUP** envvar.

    :return: bool
    """
    cleanup = os.environ.get('MTF_DO_NOT_CLEANUP')
    return not bool(cleanup)


def get_if_remoterepos():
    """
    Return the **MTF_REMOTE_REPOS** envvar.

    :return: bool
    """
    remote_repos = os.environ.get('MTF_REMOTE_REPOS')
    return bool(remote_repos)


def get_if_module():
    """
    Return the **MTF_DISABLE_MODULE** envvar.

    :return: bool
    """
    disable_module = os.environ.get('MTF_DISABLE_MODULE')
    return not bool(disable_module)


def sanitize_text(text, replacement="_", invalid_chars=["/", ";", "&", ">", "<", "|"]):

    """
    Replace invalid characters in a string.

    invalid_chars=["/", ";", "&", ">", "<", "|"]

    :param (str): text to sanitize
    :param (str): replacement char, default: "_"
    :return: str
    """
    for char in invalid_chars:
        if char in text:
            text = text.replace(char, replacement)
    return text


def sanitize_cmd(cmd):
    """
    Escape apostrophes in a command line.

    :param (str): command to sanitize
    :return: str
    """

    if '"' in cmd:
        cmd = cmd.replace('"', r'\"')
    return cmd


def get_profile():
    """
    Return a profile name.

    If the **PROFILE** envvar is not set, a profile name is
    set to be `default`.

    :return: str
    """
    profile = os.environ.get('PROFILE')
    if not profile:
        profile = "default"
    return profile


def get_url():
    """
    Return the **URL** envvar.

    :return: str
    """
    url = os.environ.get('URL')
    return url


def get_config():
    """
    Read the module's configuration file.

    :default: ``./config.yaml`` in the ``tests`` directory of the module's root
     directory
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
            "Error: File '%s' doesn't appear to exist or it's not a YAML file. "
            "Tip: If the CONFIG envvar is not set, mtf-generator looks for './config'."
            % cfgfile)


def get_compose_url():
    """
    Return Compose URL.

    If the **COMPOSEURL** ennvar is not set, it's defined from the ``./config.yaml``.

    :return: str
    """
    compose_url = os.environ.get('COMPOSEURL')
    if not compose_url:
        readconfig = CommonFunctions()
        readconfig.loadconfig()
        try:
            if readconfig.config.get("compose-url"):
                compose_url = readconfig.config.get("compose-url")
            elif readconfig.config['module']['rpm'].get("repo"):
                compose_url = readconfig.config['module']['rpm'].get("repo")
            else:
                compose_url = readconfig.config['module']['rpm'].get("repos")[0]
        except AttributeError:
            return None
    return compose_url


def get_modulemd():
    """
    Read a moduleMD file.

    If the **MODULEMDURL** envvar is not set, module-url section of
    the ``config.yaml`` file is checked. If none of them is set, then
    the ***COMPOSE_URL* envvar is checked.

    :return: dict
    """
    mdf = os.environ.get('MODULEMDURL')
    if not mdf:
        readconfig = CommonFunctions()
        readconfig.loadconfig()
        try:
            if readconfig.config.get("modulemd-url"):
                mdf = readconfig.config.get("modulemd-url")
            else:
                a = ComposeParser(get_compose_url())
                b = a.variableListForModule(readconfig.config.get("name"))
                mdf = [x[12:] for x in b if 'MODULEMDURL=' in x][0]
        except AttributeError:
            return None
    return mdf


class CommonFunctions(object):
    """
    Basic class to read configuration data and execute commands on a host machine.
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
        Get system architecture.

        :return: str
        """
        sys_arch = self.runHost(command='uname -m', verbose=False).stdout.strip()
        return sys_arch

    def runHost(self, command="ls /", **kwargs):
        """
        Run commands on a host.

        :param (str): command to exectute
        ** kwargs: avocado process.run params like: shell, ignore_status, verbose
        :return: avocado.process.run
        """
        try:
            formattedcommand = command.format(**trans_dict)
        except KeyError:
            raise ModuleFrameworkException(
                "Command is formatted by using trans_dict. If you want to use "
                "brackets { } in your code, please use {{ }}. Possible values "
                "in trans_dict are: %s. \nBAD COMMAND: %s"
                % (trans_dict, command))
        return process.run("%s" % formattedcommand, **kwargs)

    def installTestDependencies(self, packages=None):
        """
        Install packages on a host machine to prepare a test environment.

        :param (list): packages to install. If not specified, rpms from config.yaml
                       will be installed.
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
                ignore_status=True, verbose=is_debug())

    def loadconfig(self):
        """
        Load configuration from config.yaml file.

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
        package_list = []
        if not profile:
            if 'packages' in self.config:
                packages_rpm = self.config['packages'].get('rpms') if self.config[
                    'packages'].get('rpms') else []
                packages_profiles = []
                for x in self.config['packages'].get('profiles') if self.config[
                    'packages'].get('profiles') else []:
                    packages_profiles = packages_profiles + \
                                        self.getModulemdYamlconfig()['data']['profiles'][x]['rpms']
                package_list += packages_rpm + packages_profiles

            elif self.getModulemdYamlconfig()['data'].get('profiles') and self.getModulemdYamlconfig()['data'][
                'profiles'].get(get_profile()):
                package_list += self.getModulemdYamlconfig()['data']['profiles'][get_profile()]['rpms']
            else:
                # fallback solution when it is not known what to install
                package_list.append("bash")
        else:
            package_list += self.getModulemdYamlconfig()['data']['profiles'][profile]['rpms']
        print_info("PCKGs to install inside module:", package_list)
        return package_list

    def getModuleDependencies(self):
        """
        Return module dependencies.

        :return: list
        """

        return self.dependencylist

    def getModulemdYamlconfig(self, urllink=None):
        """
        Return moduleMD file yaml object.
        It can be used also for loading another yaml file via url parameter

        :param (str): url link to load. Default url defined in the `config.yaml` file,
                      can be overridden by the **CONFIG** envvar.
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
            raise ConfigExc("Cannot load file: '%s'" % e)

    def getIPaddr(self):
        """
        Return protocol (IP or IPv6) address on a guest machine.

        In many cases it should be same as a host machine's and a port
        should be forwarded to a host.

        :return: str
        """
        return self.ipaddr
