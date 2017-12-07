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
Custom exceptions library.
"""


class ModuleFrameworkException(Exception):
    """
    Formats exception output.
    :return: None
    """
    def __init__(self, *args, **kwargs):
        super(ModuleFrameworkException, self).__init__(
            'EXCEPTION MTF: ' + str(args), **kwargs)


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

class CmdExc(ModuleFrameworkException):
    """
    Indicates Command line error: Command fails on testing machine.
    """
    def __init__(self, *args, **kwargs):
        super(CmdExc, self).__init__('TYPE Command', *args, **kwargs)
