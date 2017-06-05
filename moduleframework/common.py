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
MODULARITY TESTING FRAMEWORK - common
----------------------------
It provides some general functions
"""

import sys
import netifaces
import socket
import os


class ModuleFrameworkException(Exception):
    def __init__(self, *args,**kwargs):
        super(ModuleFrameworkException, self).__init__('EXCEPTION MTF: ', *args,**kwargs)

class NspawnExc(ModuleFrameworkException):
    def __init__(self,*args,**kwargs):
        super(NspawnExc, self).__init__('TYPE nspawn', *args,**kwargs)

class RpmExc(ModuleFrameworkException):
    def __init__(self,*args,**kwargs):
        super(RpmExc, self).__init__('TYPE rpm', *args,**kwargs)

class ContainerExc(ModuleFrameworkException):
    def __init__(self,*args,**kwargs):
        super(ContainerExc, self).__init__('TYPE container', *args,**kwargs)

class ConfigExc(ModuleFrameworkException):
    def __init__(self,*args,**kwargs):
        super(ConfigExc, self).__init__('TYPE config', *args,**kwargs)

class PDCExc(ModuleFrameworkException):
    def __init__(self,*args,**kwargs):
        super(PDCExc, self).__init__('TYPE PDC', *args,**kwargs)

class KojiExc(ModuleFrameworkException):
    def __init__(self,*args,**kwargs):
        super(KojiExc, self).__init__('TYPE Koji', *args,**kwargs)


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
              "GUESTPACKAGER": guestpackager
              }

ARCH = "x86_64"
PDCURL = "https://pdc.fedoraproject.org/rest_api/v1/unreleasedvariants"
REPOMD = "repodata/repomd.xml"
MODULEFILE = 'tempmodule.yaml'
# default value of process timeout in sec
DEFAULTPROCESSTIMEOUT = 2*60
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
