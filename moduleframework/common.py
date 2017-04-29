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

defroutedev = netifaces.gateways().get('default').values(
)[0][1] if netifaces.gateways().get('default') else "lo"
hostipaddr = netifaces.ifaddresses(defroutedev)[2][0]['addr']
hostname = socket.gethostname()
dusername = "test"
dpassword = "test"
ddatabase = "basic"
# translation table for config.yaml files syntax is {VARIABLE} in config file
trans_dict = {"HOSTIPADDR": hostipaddr,
              "DEFROUTE": defroutedev,
              "HOSTNAME": hostname,
              "ROOT": "/",
              "USER": dusername,
              "PASSWORD": dpassword,
              "DATABASENAME": ddatabase
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

def is_debug():
    return bool(os.environ.get("DEBUG"))

def print_info(*args):
    """
    Print data to selected output in case you are not in testing class, there is self.log
    :param args: object
    :return: None
    """
    for arg in args:
        print >> sys.stderr, arg

def print_debug(*args):
    """
    Print data to selected output in case you are not in testing class, there is self.log
    In case DEBUG variable is set
    :param args: object
    :return: None
    """
    if is_debug():
        print_info(*args)
