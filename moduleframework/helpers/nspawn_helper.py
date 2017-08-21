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
# Authors: Petr Hracek <phracek@redhat.com>
#

import shutil
import re
import glob
import time

from moduleframework.timeoutlib import Retry
from moduleframework.common import *
from moduleframework.exceptions import *
from moduleframework.module_framework import get_if_do_cleanup
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
        if get_if_do_cleanup():
            self.jmeno = "%s_%r" % (self.moduleName, actualtime)
        else:
            self.jmeno = self.moduleName
        self.chrootpath = os.path.abspath(self.baseprefix + self.jmeno)
        print_info("name of CHROOT directory:", self.chrootpath)
        trans_dict["ROOT"] = self.chrootpath

    def setUp(self):
        """
        It is called by child class and it is same method as Avocado/Unittest has. It prepares environment
        for systemd nspawn based testing
        * installing dependencies from config
        * setup environment from config

        :return: None
        """

        self.setModuleDependencies()
        self.setRepositoriesAndWhatToInstall()
        self.installTestDependencies()
        self.__prepareSetup()
        self.__callSetupFromConfig()
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

    def __do_smart_start_cleanup(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """

        if get_if_do_cleanup():
            # delete directory with same same (in case used option DO NOT CLEANUP)
            if os.path.exists(self.chrootpath):
                shutil.rmtree(self.chrootpath, ignore_errors=True)
            # DELETE every chroot dir in case any exists
            # Commented out, because it had side effect for multihost testing. Has to be improved
            #dirstodelete = glob.glob(self.baseprefix + "*")
            #if get_if_module() and dirstodelete:
            #    for dtd in dirstodelete:
            #        shutil.rmtree(dtd, ignore_errors=True)
            os.mkdir(self.chrootpath)

    def __prepareSetup(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """
        self.__do_smart_start_cleanup()
        if not os.path.exists(os.path.join(self.chrootpath, "usr")):

            repos_to_use = ""
            counter = 0
            for repo in self.repos:
                counter = counter + 1
                repos_to_use += " --repofrompath %s%d,%s" % (
                    self.moduleName, counter, repo)
            try:
                @Retry(attempts=DEFAULTRETRYCOUNT, timeout=DEFAULTRETRYTIMEOUT * 60, delay=2 * 60,
                       error=NspawnExc("RETRY: Unable to install packages"))
                def tmpfunc():
                    self.runHost(
                        "%s install --nogpgcheck --setopt=install_weak_deps=False --installroot %s --allowerasing --disablerepo=* --enablerepo=%s* %s %s" %
                        (trans_dict["HOSTPACKAGER"], self.chrootpath, self.moduleName, repos_to_use,
                         self.whattoinstallrpm), verbose=is_not_silent())

                tmpfunc()
            except Exception as e:
                raise NspawnExc(
                    "ERROR: Unable to install packages %s\n original exeption:\n%s\n" %
                    (self.whattoinstallrpm, str(e)))
            # COPY yum repository inside NSPAW, to be able to do installations
            insiderepopath = os.path.join(self.chrootpath, self.yumrepo[1:])
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
                    srcto = os.path.join(self.chrootpath, src[1:])
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
            pkipath_ch = os.path.join(self.chrootpath, pkipath[1:])
            try:
                os.makedirs(pkipath_ch)
            except BaseException:
                pass
            for filename in glob.glob(os.path.join(pkipath, '*')):
                shutil.copy(filename, pkipath_ch)
            print_info("repo prepared for microdnf:", insiderepopath, open(insiderepopath, 'r').read())

    def __bootMachine(self):

        @Retry(attempts=DEFAULTRETRYCOUNT, timeout=DEFAULTRETRYTIMEOUT, delay=21,
               error=NspawnExc("RETRY: Unable to start nspawn machine"))
        def tempfnc():
            print_debug("starting container via command:",
                        "systemd-nspawn --machine=%s -bD %s" % (self.jmeno, self.chrootpath))
            nspawncont = process.SubProcess(
                "systemd-nspawn --machine=%s -bD %s" %
                (self.jmeno, self.chrootpath), verbose=is_debug())
            nspawncont.start()
            self.__is_booted()

        tempfnc()
        print_info("machine: %s started" % self.jmeno)

        trans_dict["GUESTIPADDR"] = trans_dict["HOSTIPADDR"]
        self.ipaddr = trans_dict["GUESTIPADDR"]

    def status(self, command="/bin/true"):
        """
        Return status of module

        :param command: which command used for do that. it could be defined inside config
        :return: bool
        """
        try:
            if 'status' in self.info and self.info['status']:
                a = self.run(self.info['status'], shell=True, verbose=False, ignore_bg_processes=True)
            else:
                a = self.run("%s" % command, shell=True, verbose=False, ignore_bg_processes=True)
            print_debug("command:", a.command, "stdout:", a.stdout, "stderr:", a.stderr)
            return True
        except BaseException:
            return False

    def start(self, command="/bin/true"):
        """
        start the RPM based module (like systemctl start service)

        :param command: Do not use it directly (It is defined in config.yaml)
        :return: None
        """
        if 'start' in self.info and self.info['start']:
            self.run(self.info['start'], shell=True, ignore_bg_processes=True)
        else:
            self.run("%s" % command, shell=True, ignore_bg_processes=True)

    def stop(self, command="/bin/true"):
        """
        stop the RPM based module (like systemctl stop service)

        :param args: Do not use it directly (It is defined in config.yaml)
        :param command: Do not use it directly (It is defined in config.yaml)
        :return: None
        """
        if 'stop' in self.info and self.info['stop']:
            self.run(self.info['stop'], shell=True, ignore_bg_processes=True)
        else:
            self.run("%s" % command, shell=True, ignore_bg_processes=True)

    def run(self, command="ls /", **kwargs):
        """
        Run command inside nspawn module type. It uses machinectl shell command.
         It need few workarounds, that's why it the code seems so strange

        TODO: workaround because machinedctl is unable to behave like ssh. It is bug
        systemd-run should be used, but in F-25 it does not contain --wait option

        :param command: str command to be executed
        :param kwargs: dict parameters passed to avocado.process.run
        :return: avocado.process.run
        """
        lpath = "/var/tmp"
        if not kwargs:
            kwargs = {}
        should_ignore = kwargs.get("ignore_status")
        kwargs["ignore_status"] = True

        comout = self.runHost("""machinectl shell root@{machine} /bin/bash -c "({comm})>{pin}/stdout 2>{pin}/stderr; echo $?>{pin}/retcode; sleep 1" """.format(
                machine=self.jmeno,
                comm=sanitize_cmd(command),
                pin=lpath),
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
        try:
            self.stop()
        except Exception as stopexception:
            print_info("STOP caused exception this is bad, but have to continue to terminate machine!!!", stopexception)
            pass

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

        if not os.environ.get('MTF_SKIP_DISABLING_SELINUX'):
            # TODO: workaround because systemd nspawn is now working well in F-25
            # (failing because of selinux)
            self.runHost(
                "setenforce %s" %
                self.__selinuxState,
                ignore_status=True, verbose=is_not_silent())
        if get_if_do_cleanup() and os.path.exists(self.chrootpath):
            shutil.rmtree(self.chrootpath, ignore_errors=True)
        self.__callCleanupFromConfig()

    def __callSetupFromConfig(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """
        if self.info.get("setup"):
            self.runHost(self.info.get("setup"), shell=True, ignore_bg_processes=True, verbose=is_not_silent())

    def __callCleanupFromConfig(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """
        if self.info.get("cleanup"):
            self.runHost(self.info.get("cleanup"), shell=True, ignore_bg_processes=True, verbose=is_not_silent())

