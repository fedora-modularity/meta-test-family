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
from __future__ import print_function
import sys
import linecache


class ModuleFrameworkException(Exception):
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
            print("-----------\n| EXCEPTION IN: {} \n| LINE: {}, {} \n| ERROR: {}\n-----------".format(filename, lineno, line.strip(), exc_obj))


class NspawnExc(ModuleFrameworkException):
    def __init__(self, *args, **kwargs):
        super(NspawnExc, self).__init__('TYPE nspawn', *args, **kwargs)


class RpmExc(ModuleFrameworkException):
    def __init__(self, *args, **kwargs):
        super(RpmExc, self).__init__('TYPE rpm', *args, **kwargs)


class ContainerExc(ModuleFrameworkException):
    def __init__(self, *args, **kwargs):
        super(ContainerExc, self).__init__('TYPE container', *args, **kwargs)


class ConfigExc(ModuleFrameworkException):
    def __init__(self, *args, **kwargs):
        super(ConfigExc, self).__init__('TYPE config', *args, **kwargs)


class PDCExc(ModuleFrameworkException):
    def __init__(self, *args, **kwargs):
        super(PDCExc, self).__init__('TYPE PDC', *args, **kwargs)


class KojiExc(ModuleFrameworkException):
    def __init__(self, *args, **kwargs):
        super(KojiExc, self).__init__('TYPE Koji', *args, **kwargs)

