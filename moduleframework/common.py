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
Custom exceptions and debugging library.
"""

import sys
import netifaces
import socket
import os
import linecache


class ModuleFrameworkException(Exception):
    """
    Formats exception output.

    :return: None
    """
    def __init__(self, *args, **kwargs):
        super(ModuleFrameworkException, self).__init__(
            'EXCEPTION MTF: ', *args, **kwargs)
        exc_type, exc_obj, tb = sys.exc_info()
        if tb is not None:
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            print "-----------\n| EXCEPTION IN: {} \n| LINE: {}, {} \n| ERROR: {}\n-----------".format(filename, lineno, line.strip(), exc_obj)


class NspawnExc(ModuleFrameworkException):
    """
    Indicates Nspawn module error.
    """
    def __init__(self, *args, **kwargs):
        super(NspawnExc, self).__init__('TYPE nspawn', *args, **kwargs)


class RpmExc(ModuleFrameworkException):
    """
    Indicates Rpm module error.
    """
    def __init__(self, *args, **kwargs):
        super(RpmExc, self).__init__('TYPE rpm', *args, **kwargs)


class ContainerExc(ModuleFrameworkException):
    """
    Indicates Docker module error.
    """
    def __init__(self, *args, **kwargs):
        super(ContainerExc, self).__init__('TYPE container', *args, **kwargs)


class ConfigExc(ModuleFrameworkException):
    """
    Indicates ``tests/config.yaml`` or module's ModuleMD YAML file error.
    File doesn't exist or has a wrong format.

    TIP: If the **CONFIG** envvar is not set, mtf-generator looks for ``./config.yaml``.

    See :mod:`moduleframework.mtf_generator` and `Configuration file`_
    for more information

    .. _Configuration file: ../user_guide/how_to_write_conf_file
    """
    def __init__(self, *args, **kwargs):
        super(ConfigExc, self).__init__('TYPE config', *args, **kwargs)


class PDCExc(ModuleFrameworkException):
    """
    Indicates PDC error.
    """
    def __init__(self, *args, **kwargs):
        super(PDCExc, self).__init__('TYPE PDC', *args, **kwargs)


class KojiExc(ModuleFrameworkException):
    """
    Indicates Koji error: Unable to download a package from Koji.
    """
    def __init__(self, *args, **kwargs):
        super(KojiExc, self).__init__('TYPE Koji', *args, **kwargs)


defroutedev = netifaces.gateways().get('default').values(
)[0][1] if netifaces.gateways().get('default') else "lo"
hostipaddr = netifaces.ifaddresses(defroutedev)[2][0]['addr']
hostname = socket.gethostname()
dusername = "test"
dpassword = "test"
ddatabase = "basic"
hostpackager = "yum -y"
guestpackager = "dnf"
if os.path.exists('/usr/bin/dnf'):
    hostpackager = "dnf -y"
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
    Returns the **DEBUG** envvar.

    :return: bool
    """
    return bool(os.environ.get("DEBUG"))


def is_not_silent():
    """
    Returns the opposite of the **DEBUG** envvar.

    :return: bool
    """
    return not is_debug()


def print_info(*args):
    """
    Prints information from the expected stdout and
    stderr files from the native test scope.

    See `Test log, stdout and stderr in native Avocado modules
    <https://avocado-framework.readthedocs.io/en/latest/WritingTests.html
    #test-log-stdout-and-stderr-in-native-avocado-modules>`_ for more information.

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
                    "String is formatted by using trans_dict."
                    + " " +
                    "If you want to use brackets { } in your code, please use double brackets {{  }}."
                    + " " +
                    "Possible values in trans_dict are: ", trans_dict)
        print >> sys.stderr, out


def print_debug(*args):
    """
    Prints information from the expected stdout and
    stderr files from the native test scope.

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
    Returns the **MTF_RECURSIVE_DOWNLOAD** envvar.

    :return: bool
    """
    return bool(os.environ.get("MTF_RECURSIVE_DOWNLOAD"))

def get_if_do_cleanup():
    """
    Returns the **MTF_DO_NOT_CLEANUP** envvar.

    :return: bool
    """
    cleanup = os.environ.get('MTF_DO_NOT_CLEANUP')
    return not bool(cleanup)


def get_if_remoterepos():
    """
    Returns the **MTF_REMOTE_REPOS** envvar.

    :return: bool
    """
    rreps = os.environ.get('MTF_REMOTE_REPOS')
    return bool(rreps)


def get_if_module():
    """
    Returns the **MTF_DISABLE_MODULE** envvar.

    :return: bool
    """
    rreps = os.environ.get('MTF_DISABLE_MODULE')
    return not bool(rreps)


def normalize_text(text, replacement="_"):
    """
    Replace invalid characters in a string.

    invalid_chars=["/", ";", "&", ">", "<", "|"]

    :arg1: string
    :arg2: replacement char, default: "_"
    :return: string
    """
    out = text
    badchars=["/", ";", "&", ">", "<", "|"]
    for foo in badchars:
        out = out.replace(foo, replacement)
    return out
