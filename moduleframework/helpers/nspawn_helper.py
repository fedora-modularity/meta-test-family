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
# Authors: Petr Hracek <phracek@redhat.com>
#

import time
import hashlib
import os

from moduleframework.common import BASEPATHDIR, translate_cmd, \
    get_if_reuse, trans_dict, print_info, is_debug, get_if_do_cleanup
from moduleframework.helpers.rpm_helper import RpmHelper
from mtf.backend.nspawn import Image, Container


class NspawnHelper(RpmHelper):
    """
    Class for MODULE testing via NSPAWN created environment, it is type of virtualization,
    something between chroot (MOCK) and full virtualization. For more info read:
    https://www.freedesktop.org/software/systemd/man/systemd-nspawn.html

    This class is derived from RPM HELPER, so that it uses same section in config file
    """

    def __init__(self):
        """
        Set basic variables for NSPAWN environment, the most important is that it set
        relative change root path
        """
        super(NspawnHelper, self).__init__()
        self.baseprefix = os.path.join(BASEPATHDIR, "chroot_")
        time.time()
        actualtime = time.time()
        self.chrootpath_baseimage = ""
        if not get_if_reuse():
            self.name = "%s_%r" % (self.component_name, actualtime)
        else:
            self.name = self.component_name
        self.chrootpath = os.path.abspath(self.baseprefix + self.name)

    def setUp(self):
        """
        It is called by child class and it is same method as Avocado/Unittest has. It prepares environment
        for systemd nspawn based testing
        * installing dependencies from config
        * setup environment from config

        :return: None
        """

        trans_dict["ROOT"] = self.chrootpath
        print_info("name of CHROOT directory:", self.chrootpath)
        self.setRepositoriesAndWhatToInstall()
        # never move this line to __init__ this localtion can change before setUp (set repositories)
        self.chrootpath_baseimage = os.path.abspath(self.baseprefix +
                                                    self.component_name +
                                                    "_image_" +
                                                    hashlib.md5(" ".join(self.repos)).hexdigest())
        self.__image_base = Image(location=self.chrootpath_baseimage,
                                  packageset=self.whattoinstallrpm,
                                  repos=self.repos,
                                  ignore_installed=True)
        self.__image = self.__image_base.create_snapshot(self.chrootpath)
        self.__container = Container(image=self.__image, name=self.name)
        self._callSetupFromConfig()
        self.__container.boot_machine()

    def run(self, command, **kwargs):
        return self.__container.execute(command=translate_cmd(command, translation_dict=trans_dict), **kwargs)

    def start(self, command="/bin/true"):
        """
        Start 'service' inside NSPAWN container
        Keep it running with sleep infinity, systemd-run needs to have it running

        :param command: Do not use it directly (It is defined in config.yaml)
        :return: None
        """
        command = self.info.get('start') or command
        self.run(command, internal_background=False, ignore_bg_processes=True, verbose=is_debug())
        self.status()
        trans_dict["GUESTPACKAGER"] = self.get_packager()

    def selfcheck(self):
        """
        Test if default command will pass, it is more important for nspawn, because it happens that
        it does not returns anything

        :return: avocado.process.run
        """
        return self.run(command="/bin/true").stdout

    def copyTo(self, src, dest):
        """
        Copy file to module from host

        :param src: source file on host
        :param dest: destination file on module
        :return: None
        """
        self.__container.copy_to(src, dest)

    def copyFrom(self, src, dest):
        """
        Copy file from module to host

        :param src: source file on module
        :param dest: destination file on host
        :return: None
        """
        self.__container.copy_from(src, dest)

    def tearDown(self):
        """
        cleanup environment after test is finished and call cleanup section in config file

        :return: None
        """
        if get_if_do_cleanup() and not get_if_reuse():
            try:
                self.__container.stop()
            except:
                pass
            try:
                self.__container.rm()
            except:
                pass
        else:
            print_info("tearDown skipped", "running nspawn: %s" % self.name)
            print_info("To connect to a machine use:",
                       "machinectl shell root@%s /bin/bash" % self.name)
