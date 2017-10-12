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

import shutil
import re
import glob
import time
import hashlib

from moduleframework.common import *
from moduleframework.exceptions import *
from moduleframework.helpers.rpm_helper import RpmHelper


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
        self.__selinuxState = None
        time.time()
        actualtime = time.time()
        self.chrootpath_baseimage = ""
        if not get_if_reuse():
            self.jmeno = "%s_%r" % (self.moduleName, actualtime)
        else:
            self.jmeno = self.moduleName
        self.chrootpath = os.path.abspath(self.baseprefix + self.jmeno)
        self.__default_command_sleep = 2

    def __machined_restart(self):
        """
        Machined is not reliable well, restart it whenever you want.

        :return: None
        """
        #return self.runHost("systemctl restart systemd-machined", verbose=is_debug(), ignore_status=True)
        # remove restarting when used systemd-run
        pass

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
        self.__prepareSetup()
        self.__create_snaphot()
        self._callSetupFromConfig()
        self.__bootMachine()

    def __is_killed(self):
        for foo in range(DEFAULTRETRYTIMEOUT):
            time.sleep(1)
            out = self.runHost("machinectl status %s" % self.jmeno, verbose=is_debug(), ignore_status=True)
            if out.exit_status != 0:
                print_debug("NSPAWN machine %s stopped" % self.jmeno)
                return True
        raise NspawnExc("Unable to stop machine %s within %d" % (self.jmeno, DEFAULTRETRYTIMEOUT))

    def __is_booted(self):
        for foo in range(DEFAULTRETRYTIMEOUT):
            time.sleep(1)
            out = self.runHost("machinectl status %s" % self.jmeno, verbose=is_debug(), ignore_status=True)
            if "systemd-logind" in out.stdout:
                time.sleep(2)
                print_debug("NSPAWN machine %s booted" % self.jmeno)
                return True
        raise NspawnExc("Unable to start machine %s within %d" % (self.jmeno, DEFAULTRETRYTIMEOUT))

    def __create_snaphot(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """

        if get_if_do_cleanup():
            # delete directory with same same (in case used option DO NOT CLEANUP)
            if os.path.exists(self.chrootpath):
                shutil.rmtree(self.chrootpath, ignore_errors=True)
        # copy files from base image directory to working copy (instead of overlay)
        if self.chrootpath_baseimage != self.chrootpath and \
                not os.path.exists(os.path.join(self.chrootpath, "usr")):
            self.runHost("cp -rf %s %s" % (self.chrootpath_baseimage, self.chrootpath))

    def __prepareSetup(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """
        self.chrootpath_baseimage = os.path.abspath(self.baseprefix +
                                                    self.moduleName +
                                                    "_image_" +
                                                    hashlib.md5(" ".join(self.repos)).hexdigest())
        if not os.path.exists(os.path.join(self.chrootpath_baseimage, "usr")):
            repos_to_use = ""
            counter = 0
            for repo in self.repos:
                counter = counter + 1
                repos_to_use += " --repofrompath %s%d,%s" % (
                    self.moduleName, counter, repo)
            try:
                self.runHost(
                    ("%s install --nogpgcheck --setopt=install_weak_deps=False "
                    "--installroot %s --allowerasing --disablerepo=* --enablerepo=%s* %s %s") %
                    (trans_dict["HOSTPACKAGER"], self.chrootpath_baseimage, self.moduleName, repos_to_use, self.whattoinstallrpm), verbose=is_not_silent())
            except Exception as e:
                raise NspawnExc(
                    "ERROR: Unable to install packages %s\n original exeption:\n%s\n" %
                    (self.whattoinstallrpm, str(e)))
            # COPY yum repository inside NSPAW, to be able to do installations
            insiderepopath = os.path.join(self.chrootpath_baseimage, self.yumrepo[1:])
            try:
                os.makedirs(os.path.dirname(insiderepopath))
            except:
                pass
            counter = 0
            f = open(insiderepopath, 'w')
            for repo in self.repos:
                counter = counter + 1
                add = """[%s%d]
name=%s%d
baseurl=%s
enabled=1
gpgcheck=0

""" % (self.moduleName, counter, self.moduleName, counter, repo)
                f.write(add)
            f.close()

            #        shutil.copy(self.yumrepo, insiderepopath)
            #        self.runHost("sed s/enabled=0/enabled=1/ -i %s" % insiderepopath, ignore_status=True)
            for repo in self.repos:
                if "file:///" in repo:
                    src = repo[7:]
                    srcto = os.path.join(self.chrootpath_baseimage, src[1:])
                    try:
                        os.makedirs(os.path.dirname(srcto))
                    except Exception as e:
                        print_debug(e, "Unable to create DIR (already created)", srcto)
                        pass
                    try:
                        shutil.copytree(src, srcto)
                    except Exception as e:
                        print_debug(e, "Unable to copy files from:", src, "to:", srcto)
                        pass
            pkipath = "/etc/pki/rpm-gpg"
            pkipath_ch = os.path.join(self.chrootpath_baseimage, pkipath[1:])
            try:
                os.makedirs(pkipath_ch)
            except BaseException:
                pass
            for filename in glob.glob(os.path.join(pkipath, '*')):
                shutil.copy(filename, pkipath_ch)
            print_info("repo prepared:", insiderepopath, open(insiderepopath, 'r').read())
        else:
            print_info("Base image for NSPAWN already exist: %s" % self.chrootpath_baseimage)

    def __bootMachine(self):
        """
        Internal function.
        Start machine via nspawn and wait untill booted.

        :return: None
        """
        print_debug("starting NSPAWN")
        nspawncont = process.SubProcess(
            "systemd-nspawn --machine=%s -bD %s" %
            (self.jmeno, self.chrootpath), verbose=is_debug())
        nspawncont.start()
        self.__is_booted()
        print_info("machine: %s started" % self.jmeno)

        trans_dict["GUESTIPADDR"] = trans_dict["HOSTIPADDR"]
        self.ipaddr = trans_dict["GUESTIPADDR"]

    def run (self, command, **kwargs):
        return self.__run_systemdrun(command, **kwargs)

    def start(self, command="/bin/true"):
        """
        Start 'service' inside NSPAWN container
        Keep it running with sleep infinity, systemd-run needs to have it running

        :param command: Do not use it directly (It is defined in config.yaml)
        :return: None
        """
        command = self.info.get('start') or command
        self.__run_systemdrun(command, internal_background=False, ignore_bg_processes=True, verbose=is_debug())
        self.status()
        trans_dict["GUESTPACKAGER"] = self.get_packager()

    def __run_systemdrun(self, command, internal_background=False, **kwargs):
        """
        Run command inside nspawn module type. It uses systemd-run.
        since Fedora 26 there is important --wait option

        :param command: str command to be executed
        :param kwargs: dict parameters passed to avocado.process.run
        :return: avocado.process.run
        """
        self.__machined_restart()
        lpath = "/var/tmp"
        add_wait_var = "--wait"
        add_sleep_infinite = ""
        if internal_background:
            add_wait_var=""
            add_sleep_infinite = "&& sleep infinity"
        try:
            comout = self.runHost("""systemd-run {wait} -M {machine} /bin/bash -c "({comm})>{pin}/stdout 2>{pin}/stderr {sleep}" """.format(
                    wait=add_wait_var,
                    machine=self.jmeno,
                    comm=sanitize_cmd(command),
                    pin=lpath,
                    sleep=add_sleep_infinite),
                **kwargs)
            if not internal_background:
                with open("{chroot}{pin}/stdout".format(chroot=self.chrootpath, pin=lpath), 'r') as content_file:
                    comout.stdout = content_file.read()
                with open("{chroot}{pin}/stderr".format(chroot=self.chrootpath, pin=lpath), 'r') as content_file:
                    comout.stderr = content_file.read()
                comout.command = command
                print_debug(comout)
            return comout
        except process.CmdError as e:
            raise CmdExc("Command in SYSTEMD-RUN failed: %s" % command, e)

    def __run_machinectl(self, command, **kwargs):
        """
        Run command inside nspawn module type. It uses machinectl shell command.
         It need few workarounds, that's why it the code seems so strange

        TODO: workaround because machinedctl is unable to behave like ssh. It is bug
        systemd-run should be used, but in F-25 it does not contain --wait option

        :param command: str command to be executed
        :param kwargs: dict parameters passed to avocado.process.run
        :return: avocado.process.run
        """
        self.__machined_restart()
        lpath = "/var/tmp"
        if not kwargs:
            kwargs = {}
        should_ignore = kwargs.get("ignore_status")
        kwargs["ignore_status"] = True
        comout = self.runHost("""machinectl shell root@{machine} /bin/bash -c "({comm})>{pin}/stdout 2>{pin}/stderr; echo $?>{pin}/retcode; sleep {defaultsleep}" """.format(
                machine=self.jmeno,
                comm=sanitize_cmd(command),
                pin=lpath,
                defaultsleep=self.__default_command_sleep ),
            **kwargs)
        if comout.exit_status != 0:
            raise NspawnExc("This command should not fail anyhow inside NSPAWN:", sanitize_cmd(command))
        try:
            kwargs["verbose"] = is_not_silent()
            b = self.runHost(
                'bash -c "cat {chroot}{pin}/stdout; cat {chroot}{pin}/stderr > /dev/stderr; exit `cat {chroot}{pin}/retcode`"'.format(
                    chroot=self.chrootpath,
                    pin=lpath),
                **kwargs)
        finally:
            comout.stdout = b.stdout
            comout.stderr = b.stderr
            comout.exit_status = b.exit_status
            removesworkaround = re.search('[^(]*\((.*)\)[^)]*', comout.command)
            if removesworkaround:
                comout.command = removesworkaround.group(1)
            if comout.exit_status == 0 or should_ignore:
                return comout
            else:
                raise process.CmdError(comout.command, comout)

    def selfcheck(self):
        """
        Test if default command will pass, it is more important for nspawn, because it happens that
        it does not returns anything

        :return: avocado.process.run
        """
        return self.run().stdout

    def copyTo(self, src, dest):
        """
        Copy file to module from host

        :param src: source file on host
        :param dest: destination file on module
        :return: None
        """
        self.runHost(
            " machinectl copy-to  %s %s %s" %
            (self.jmeno, src, dest), timeout=DEFAULTPROCESSTIMEOUT, ignore_bg_processes=True, verbose=is_not_silent())

    def copyFrom(self, src, dest):
        """
        Copy file from module to host

        :param src: source file on module
        :param dest: destination file on host
        :return: None
        """
        self.runHost(
            " machinectl copy-from  %s %s %s" %
            (self.jmeno, src, dest), timeout=DEFAULTPROCESSTIMEOUT, ignore_bg_processes=True, verbose=is_not_silent())

    def tearDown(self):
        """
        cleanup environment after test is finished and call cleanup section in config file

        :return: None
        """
        if get_if_do_cleanup() and not get_if_reuse():
            try:
                self.stop()
            except Exception as stopexception:
                print_info("Stop action caused exception. It should not happen.",
                           stopexception)
                pass
            self.__machined_restart()
            try:
                self.runHost("machinectl poweroff %s" % self.jmeno, verbose=is_not_silent())
                self.__is_killed()
            except Exception as poweroffex:
                print_info("Unable to stop machine via poweroff, terminating", poweroffex)
                try:
                    self.runHost("machinectl terminate %s" % self.jmeno, ignore_status=True)
                    self.__is_killed()
                except Exception as poweroffexterm:
                    print_info("Unable to stop machine via terminate, STRANGE", poweroffexterm)
                    time.sleep(DEFAULTRETRYTIMEOUT)
                    pass
                pass
            self._callCleanupFromConfig()
            if os.path.exists(self.chrootpath):
                shutil.rmtree(self.chrootpath, ignore_errors=True)
        else:
            print_info("tearDown skipped", "running nspawn: %s" % self.jmeno)
            print_info("To connect to a machine use:",
                       "machinectl shell root@%s /bin/bash" % self.jmeno)
