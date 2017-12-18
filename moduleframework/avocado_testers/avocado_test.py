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
main module provides all helpers for various module types and AVOCADO(unittest) classes
what you should use for your tests (inherited)
"""

from avocado import Test
from avocado.core import exceptions
import warnings

from moduleframework.common import *
from moduleframework.helpers.container_helper import ContainerHelper
from moduleframework.helpers.nspawn_helper import NspawnHelper
from moduleframework.helpers.rpm_helper import RpmHelper
from moduleframework.helpers.openshift_helper import OpenShiftHelper


# INTERFACE CLASS FOR GENERAL TESTS OF MODULES
class AvocadoTest(Test):
    """
    MAIN class for inheritance what should be used for tests based on this framework.
    It is intended for tests what fits all module types, what does not have specific usecases for some module type.
    Class is derived from AVOCADO TEST class.

    This class is interface to *HELPER classed and use them as backend

    It is not allowed to do instances of this class!!!
    Instance is done when test is executed by test scheduler like avocado/unittest

    :avocado: disable
    """

    def __init__(self, *args, **kwargs):
        super(AvocadoTest, self).__init__(*args, **kwargs)

        self.backend = get_backend()
        self.moduleType = get_module_type()
        self.moduleType_base = get_module_type_base()
        self.moduleProfile = get_profile()
        print_info(
            "Module Type: %s - Backend: %s - Profile: %s" %
            (self.moduleType, self.moduleType_base, self.moduleProfile))

    def __print_breaks(self, message):
        delimiterStart = '\n::::::::::::::::::::::::'
        delimiterEnd = '::::::::::::::::::::::::\n'
        self.log.debug("\n{0} {1} {2}".format(delimiterStart, message, delimiterEnd))

    def cancel(self, *args, **kwargs):
        try:
            super(AvocadoTest, self).cancel(*args, **kwargs)
        except AttributeError:
            raise exceptions.TestDecoratorSkip(*args, **kwargs)

    def setUp(self):
        """
        Unittest setUp method. It prepares environment for selected module type like NSPAWN, DOCKER, RPM
        It is called when instance of test is created.

        When you redefine this method in your class, don't forget to call super(self.__class__,self).setUp()

        :return: None
        """
        self.__print_breaks("SETUP")
        return self.backend.setUp()

    def tearDown(self, *args, **kwargs):
        """
        Unittest tearDown method. It clean environment for selected module type like NSPAWN, DOCKER, RPM after test is done
        It is called when instance of test is finished.

        When you redefine this method in your class, don't forget to call super(self.__class__,self).tearDown()

        :return: None
        """
        self.__print_breaks("TEARDOWN")
        return self.backend.tearDown(*args, **kwargs)

    def start(self, *args, **kwargs):
        """
        Start the module, it uses start action from config file for selected module or it calls default start
        in case start action is not defined in config file

        :param args: Do not use it directly (It is defined in config.yaml)
        :param kwargs: Do not use it directly (It is defined in config.yaml)
        :return: None
        """
        self.__print_breaks("START MODULE")
        return self.backend.start(*args, **kwargs)

    def stop(self, *args, **kwargs):
        """
        Stop the module, it uses stop action from config file for selected module or it calls default stop
        in case stop action is not defined in config file (for some module type, stop action does not have sense,
        like docker, stop is done via docker stop dockerID)

        :param args: Do not use it directly (It is defined in config.yaml)
        :param kwargs: Do not use it directly (It is defined in config.yaml)
        :return: None
        """
        self.__print_breaks("STOP")
        return self.backend.stop(*args, **kwargs)

    def run(self, *args, **kwargs):
        """
        Run command inside module, parametr command and others are passed to proper module Helper

        :param args: command
        :param kwargs: shell, ignore_status, verbose
        :return: object avocado.process.run
        """
        self.__print_breaks("COMMAND IN MODULE <->")
        return self.backend.run(*args, **kwargs)

    def runCheckState(self, command="ls /", expected_state=0,
                      output_text=None, *args, **kwargs):
        """
        derived from self.run method but allows to add also to pass expected return code.

        :param command: str Command to run
        :param expected_state: int expected value of return code of command or last command in case of shell
        :param output_text: str Description of commands, what it does (in case of empty, command is default)
        :param args: pass thru
        :param kwargs: pass thru
        :return: None
        """
        cmd = self.run(command, ignore_status=True, *args, **kwargs)
        output_text = command if not output_text else output_text
        if cmd.exit_status == expected_state:
            self.log.info(
                "command (RC=%d, expected=%d): %s" %
                (cmd.exit_status, expected_state, output_text))
        else:
            self.fail(
                "command (RC=%d, expected=%d): %s" %
                (cmd.exit_status, expected_state, output_text))

    def getConfig(self):
        """
        Return dict object of loaded config file

        :return: dict
        """
        return self.backend.config

    def getConfigModule(self):
        """
        Return just part specific for this module type (module section in config file)

        :return: dict
        """
        return self.backend.info

    def runHost(self, *args, **kwargs):
        """
        Run command on host (local machine). all parameters are passed inside. the most important is command
        what contains command to run

        :param args: pass thru
        :param kwargs: pass thru
        :return: object of avocado.process.run
        """
        self.__print_breaks("COMMAND ON HOST <!>")
        return self.backend.runHost(*args, **kwargs)

    def getModulemdYamlconfig(self, *args, **kwargs):
        """
        Return dict of actual moduleMD file

        :param args: pass thru
        :param kwargs: pass thru
        :return: dict
        """
        return self.backend.getModulemdYamlconfig(*args, **kwargs)

    def getActualProfile(self):
        """
        Return actual profile set profile via env variable PROFILE, could be used for filtering tests with skipIf method
        Actually it returns list of packages, because profiles are not defined well

        :return: str
        """
        self.start()
        allpackages = self.run(r'rpm -qa --qf="%{{name}}\n"', verbose=is_not_silent()).stdout.split('\n')
        return allpackages

    def copyTo(self, *args, **kwargs):
        """
        Copy file from host machine to module

        :param src: source file from host
        :param dest: destination file inside module
        :return: None
        """
        return self.backend.copyTo(*args, **kwargs)

    def copyFrom(self, *args, **kwargs):
        """
        Copy file from module to host machine

        :param src: source file from host
        :param dest: destination file inside module
        :return: None
        """
        return self.backend.copyFrom(*args, **kwargs)

    def getIPaddr(self):
        """
        Return ip address string of guest machine
        In many cases it should be same as host machine and port should be forwarded to host

        :return: str
        """
        warnings.warn("Function getIPaddr is deprecated. Use self.ip_address instead",
                      DeprecationWarning)
        return self.backend.ip_address

    @property
    def ip_address(self):
        """
        Return ip address string of guest machine
        In many cases it should be same as host machine and port should be forwarded to host

        :return: str
        """
        return self.backend.ip_address

    def getArch(self):
        """
        get system architecture string

        :return: str
        """
        return self.backend.getArch()

    def getModuleDependencies(self):
        """
        get list of module dependencies dictionary, there is structure like:
        {module_name: {stream: master, urls=[repo_url1, repo_url2]},
         dependent_module_name: {stream: f26, urls=[repo_url3]}}

        :return: dict
        """
        warnings.warn("Function getModuleDependencies is deprecated. Use self.dependency_list instead",
                      DeprecationWarning)
        return self.dependency_list()

    @property
    def dependency_list(self):
        """
        get list of module dependencies dictionary, there is structure like:
        {module_name: {stream: master, urls=[repo_url1, repo_url2]},
         dependent_module_name: {stream: f26, urls=[repo_url3]}}

        :return: dict
        """
        return self.backend.dependency_list

    def run_script(self, *args, **kwargs):
        """
        run script or binary inside module

        :param filename: filename to copy to module
        :param args: pass this args as cmdline args to run binary
        :param kwargs: pass thru to avocado process.run
        :return: avocado process.run object
        """
        return self.backend.run_script(*args, **kwargs)

    def assert_to_warn(self, func, *args, **kwargs):
        """
        run function which you would like to mark as WARN
        :param func: function for run
        :param args: pass this args to run function
        :param kwargs: pass this args to run function
        :return: returns either PASS or WARN
        """
        try:
            func(*args, **kwargs)
        except AssertionError as e:
            self.log.warn("Warning raised: %s" % e)


def get_backend():
    """
    Return proper module backend, set by config by default_module section, or defined via
    env variable "MODULE"

    :return: module object
    """
    parent = get_module_type_base()

    if parent == 'docker':
        return ContainerHelper()
    elif parent == 'rpm':
        return RpmHelper()
    elif parent == 'nspawn':
        return NspawnHelper()
    elif parent == 'openshift':
        return OpenShiftHelper()


# To keep backward compatibility. This method could be used by pure avocado tests and is already used
get_correct_backend = get_backend
