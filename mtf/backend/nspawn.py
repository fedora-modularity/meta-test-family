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
Low level library handling Systemd nspawn containers and images
"""

import os
import logging
import shutil
import glob
import time
import re

from avocado import Test
from avocado.utils import process
from mtf import common
from mtf import mtfexceptions

DEFAULT_RETRYTIMEOUT = 30
DEFAULT_SLEEP = 1
base_package_set = ["systemd"]

is_debug_low = common.is_debug
if is_debug_low():
    logging.basicConfig(level=logging.DEBUG)

class Image(object):
    """
    It represents image object for Nspawn virtualization
    Actually it is directory
    """
    logger = logging.getLogger("Image")
    def __init__(self, repos, packageset, location, installed=False, packager="dnf -y",
                 name="unique", ignore_installed=False):
        self.repos = repos
        self.packageset = list(set(packageset + base_package_set))
        self.location = location
        self.packager = packager
        self.name = name
        baserepodir=os.path.join("/etc", "yum.repos.d")
        # allow to fake environment in ubuntu (for Travis)
        if not os.path.exists(baserepodir):
            baserepodir="/var/tmp"
        self.yumrepo = os.path.join(baserepodir, "%s.repo" % self.name)
        if installed:
            pass
        else:
            try:
                self.__install()
            except mtfexceptions.NspawnExc as e:
                if ignore_installed:
                    pass
                else:
                    raise e

    def create_snapshot(self, destination):
        """
        returns Image object with copyied files from base image
        
        :param destination: directory where to crete copy
        :return: Image
        """
        self.logger.debug("Create Snapshot: %s -> %s" % (self.location, destination))
        # copytree somethimes fails, it is not reliable in case of copy of system
        # shutil.copytree(self.location, destination)
        # cp will do better work
        process.run("cp -rf %s %s" % (self.location, destination))
        return self.__class__(repos=self.repos, packageset=self.packageset,
                              location=destination, installed=True,
                              packager=self.packager, name=self.name)

    def __install(self):
        """
        Internal method for installing packages to chroot and set repositories.
        
        :return: None
        """
        self.logger.debug("Install system to direcory: %s" % self.location)
        if not os.path.exists(os.path.join(self.location, "usr")):
            if not os.path.exists(self.location):
                os.makedirs(self.location)
            repos_to_use = ""
            counter = 0
            for repo in self.repos:
                counter = counter + 1
                repos_to_use += " --repofrompath %s%d,%s" % (
                    self.name, counter, repo)
            self.logger.debug("Install packages: %s" % self.packageset)
            self.logger.debug("Repositories: %s" % self.repos)
            process.run("%s install --nogpgcheck --setopt=install_weak_deps=False "
                 "--installroot %s --allowerasing --disablerepo=* --enablerepo=%s* %s %s" %
                                    (self.packager, self.location, self.name,
                                     repos_to_use, " ".join(self.packageset)),
                        verbose=is_debug_low())
            insiderepopath = os.path.join(self.location, self.yumrepo[1:])
            if not os.path.exists(os.path.dirname(insiderepopath)):
                os.makedirs(os.path.dirname(insiderepopath))
            counter = 0
            with open(insiderepopath, 'w') as f:
                for repo in self.repos:
                    counter = counter + 1
                    add = """[%s%d]
            name=%s%d
            baseurl=%s
            enabled=1
            gpgcheck=0
    
            """ % (self.name, counter, self.name, counter, repo)
                    f.write(add)
            for repo in self.repos:
                if "file:///" in repo:
                    src = repo[7:]
                    srcto = os.path.join(self.location, src[1:])
                    if not os.path.exists(os.path.dirname(srcto)):
                        os.makedirs(os.path.dirname(srcto))
                    shutil.copytree(src, srcto)
            pkipath = "/etc/pki/rpm-gpg"
            pkipath_ch = os.path.join(self.location, pkipath[1:])
            if not os.path.exists(pkipath_ch):
                os.makedirs(pkipath_ch)
            for filename in glob.glob(os.path.join(pkipath, '*')):
                shutil.copy(filename, pkipath_ch)
        else:
            raise mtfexceptions.NspawnExc("Directory %s already in use" % self.location)

    def get_location(self):
        """
        return directory location
        
        :return: str
        """
        return self.location

    def rmi(self):
        shutil.rmtree(self.location)

class Container(object):
    """
    It represents nspawn container virtualization with 
    methods for start/run/execute commands inside
     
    """
    logger = logging.getLogger("Container")
    __systemd_wait_support = False
    __default_command_sleep = 2
    __alternative_boot = False
    
    def __init__(self, image, name=None):
        """
        
        :param image: Image object 
        :param name: optional, use unique name for generating containers in case not given, some name is generated
        """
        self.image = image
        self.name = name or common.generate_unique_name()
        self.location = self.image.get_location()
        self.__systemd_wait_support = self._run_systemdrun_decide()

    def __machined_restart(self):
        # this is removed, it was important for crappy machinectl shell handling
        #self.logger.debug("restart systemd-machined")
        #return process.run("systemctl restart systemd-machined", verbose=is_debug_low(), ignore_status=True)
        pass

    def __is_killed(self):
        for foo in range(DEFAULT_RETRYTIMEOUT):
            time.sleep(DEFAULT_SLEEP)
            out = process.run("machinectl status %s" % self.name, ignore_status=True, verbose=is_debug_low())
            if out.exit_status != 0:
                return True
        raise mtfexceptions.NspawnExc("Unable to stop machine %s within %d" % (self.name, DEFAULT_RETRYTIMEOUT))

    def __is_booted(self):
        for foo in range(DEFAULT_RETRYTIMEOUT):
            time.sleep(DEFAULT_SLEEP)
            out = process.run("machinectl status %s" % self.name, ignore_status=True, verbose=is_debug_low())
            if not self.__alternative_boot:
                if  "systemd-logind" in out.stdout:
                    time.sleep(DEFAULT_SLEEP)
                    return True
            else:
                if "Unit: machine" in out.stdout:
                    time.sleep(DEFAULT_SLEEP)
                    return True
        raise mtfexceptions.NspawnExc("Unable to start machine %s within %d" % (self.name, DEFAULT_RETRYTIMEOUT))

    def boot_machine(self, nspawn_add_option_list=[], boot_cmd="", wait_finish=False):
        """
        start machine via -b option (full boot, default) or 
        via boot_cmd (usefull with wait_finish=True option)
        
        :param nspawn_add_option_list: list - additional nspawn parameters 
        :param boot_cmd: std - command with aruments for starting
        :param wait_finish: - bool - wait to process finish (by default it just wait for creting systemd unit and boot)
        :return: process.Subprocess object 
        """
        self.logger.debug("starting NSPAWN")
        bootmachine = ""
        bootmachine_cmd = ""
        if boot_cmd:
            self.__alternative_boot = True
            bootmachine_cmd = boot_cmd
            process.run("systemctl reset-failed machine-%s.scope" % self.name,
                        ignore_status=True, verbose=is_debug_low())
        else:
            bootmachine = "-b"
        command = "systemd-nspawn --machine=%s %s %s -D %s %s" % \
                  (self.name, " ".join(nspawn_add_option_list), bootmachine, self.location, bootmachine_cmd)
        self.logger.debug("Start command: %s" % command)
        nspawncont = process.SubProcess(command)
        self.logger.info("machine: %s starting" % self.name)
        if wait_finish:
            nspawncont.wait()
        else:
            nspawncont.start()
            self.__is_booted()
        self.logger.info("machine: %s starting finished" % self.name)
        return nspawncont

    def execute(self, command, **kwargs):
        """
        execute command inside container, it hides what method will be used
        
        :param command: str
        :param kwargs: pass thru to avocado.process.run command
        :return: process object
        """
        return self.run_systemdrun(command, **kwargs)

    def _run_systemdrun_decide(self):
        """
        Internal method
        decide if it is possible to use --wait option to systemd

        :return:
        """
        return "--wait" in process.run("systemd-run --help", verbose=is_debug_low()).stdout

    def __systemctl_wait_until_finish(self, machine, unit):
        """
        Internal method
        workaround for systemd-run without --wait option

        :param machine:
        :param unit:
        :return:
        """
        while True:
            output = [x.strip() for x in
                      process.run("systemctl show -M {} {}".format(machine, unit),
                                   verbose=is_debug_low()).stdout.split("\n")]
            retcode = int([x[-1] for x in output if "ExecMainStatus=" in x][0])
            if not ("SubState=exited" in output or "SubState=failed" in output):
                time.sleep(0.1)
            else:
                break
        process.run("systemctl -M {} stop {}".format(machine, unit), ignore_status=True, verbose=is_debug_low())
        return retcode

    def run_systemdrun(self, command, internal_background=False, **kwargs):
        """
        execute command via systemd-run inside container

        :param command:
        :param internal_background:
        :param kwargs:
        :return:
        """
        if not kwargs:
            kwargs = {}
        self.__machined_restart()
        add_sleep_infinite = ""
        unit_name = common.generate_unique_name()
        lpath = "/var/tmp/{}".format(unit_name)
        if self.__systemd_wait_support:
            add_wait_var = "--wait"
        else:
            # keep service exist after it finish, to be able to read exit code
            add_wait_var = "-r"
        if internal_background:
            add_wait_var = ""
            add_sleep_infinite = "&& sleep infinity"
        opts = " --unit {unitname} {wait} -M {machine}".format(wait=add_wait_var,
                                                              machine=self.name,
                                                              unitname=unit_name
                                                              )
        try:
            comout = process.run("""systemd-run {opts} /bin/bash -c "({comm})>{pin}.stdout 2>{pin}.stderr {sleep}" """.format(
                    opts=opts, comm=common.sanitize_cmd(command), pin=lpath, sleep=add_sleep_infinite),
                **kwargs)
            if not internal_background:
                if not self.__systemd_wait_support:
                    comout.exit_status = self.__systemctl_wait_until_finish(self.name,unit_name)
                with open("{chroot}{pin}.stdout".format(chroot=self.location, pin=lpath), 'r') as content_file:
                    comout.stdout = content_file.read()
                with open("{chroot}{pin}.stderr".format(chroot=self.location, pin=lpath), 'r') as content_file:
                    comout.stderr = content_file.read()
                comout.command = command
                os.remove("{chroot}{pin}.stdout".format(chroot=self.location, pin=lpath))
                os.remove("{chroot}{pin}.stderr".format(chroot=self.location, pin=lpath))
                self.logger.debug(comout)
                if not self.__systemd_wait_support and not kwargs.get("ignore_status") and comout.exit_status != 0:
                    raise process.CmdError(comout.command, comout)
            return comout
        except process.CmdError as e:
            raise e

    def run_machinectl(self, command, **kwargs):
        """
        execute command via machinectl shell inside container

        :param command:
        :param kwargs:
        :return:
        """
        self.__machined_restart()
        lpath = "/var/tmp"
        if not kwargs:
            kwargs = {}
        should_ignore = kwargs.get("ignore_status")
        kwargs["ignore_status"] = True
        comout = process.run("""machinectl shell root@{machine} /bin/bash -c "({comm})>{pin}/stdout 2>{pin}/stderr; echo $?>{pin}/retcode; sleep {defaultsleep}" """.format(
                machine=self.name, comm=common.sanitize_cmd(command), pin=lpath,
                defaultsleep=self.__default_command_sleep ), **kwargs)
        if comout.exit_status != 0:
            raise mtfexceptions.NspawnExc("This command should not fail anyhow inside NSPAWN:", command)
        try:
            kwargs["verbose"] = False
            b = process.run(
                'bash -c "cat {chroot}{pin}/stdout; cat {chroot}{pin}/stderr > /dev/stderr; exit `cat {chroot}{pin}/retcode`"'.format(
                    chroot=self.location,
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
        return self.execute("true")

    def copy_to(self, src, dest):
        """
        Copy file to module from host

        :param src: source file on host
        :param dest: destination file on module
        :return: None
        """
        self.logger.debug("copy files (inside) from: %s to: %s" % (src, dest))
        process.run(
            " machinectl copy-to  %s %s %s" %
            (self.name, src, dest), timeout=DEFAULT_RETRYTIMEOUT, verbose=is_debug_low())

    def copy_from(self, src, dest):
        """
        Copy file from module to host

        :param src: source file on module
        :param dest: destination file on host
        :return: None
        """
        self.logger.debug("copy files (outside) from: %s to: %s" % (src, dest))
        process.run(
            " machinectl copy-from  %s %s %s" %
            (self.name, src, dest), timeout=DEFAULT_RETRYTIMEOUT, verbose=is_debug_low())

    def stop(self):
        """
        Stop the nspawn container

        :return:
        """
        self.logger.debug("Stop")
        self.__machined_restart()
        try:
            if not self.__alternative_boot:
                process.run("machinectl poweroff %s" % self.name, verbose=is_debug_low())
            else:
                try:
                    process.run("systemctl kill --kill-who=all -s9 machine-%s.scope" % self.name,
                                ignore_status=True, verbose=is_debug_low())
                except Exception:
                    pass
                try:
                    process.run("systemctl reset-failed machine-%s.scope" % self.name,
                                ignore_status=True, verbose=is_debug_low())
                except Exception:
                    pass
            self.__is_killed()
        except BaseException as poweroffex:
            self.logger.debug("Unable to stop machine via poweroff, terminating : %s" % poweroffex)
            try:
                process.run("machinectl terminate %s" % self.name, ignore_status=True, verbose=is_debug_low())
                self.__is_killed()
            except BaseException as poweroffexterm:
                self.logger.debug("Unable to stop machine via terminate, STRANGE: %s" % poweroffexterm)
                time.sleep(DEFAULT_RETRYTIMEOUT)
                pass
            pass

    def rm(self):
        """
        Remove container image via image method

        :return:
        """
        self.logger.debug("Remove")
        self.image.rmi()


# ====================== Self Tests ======================

class testImage(Test):
    """
    Test Image class for folders and nspawn installation to dirs
    """
    loc1 = "/tmp/dddd1"
    loc2 = "/tmp/dddd2"

    def setUp(self):
        # cleanup dirs, to ensure that it will pass
        # it raises error in case of existing and not used installed=True as option
        process.run("rm -rf %s %s" % (self.loc1, self.loc2), ignore_status=True)
        self.i1=Image(repos=["http://ftp.fi.muni.cz/pub/linux/fedora/linux/releases/26/Everything/x86_64/os/"],
                 packageset=["bash"],
                 location=self.loc1)

    def test_basic(self):
        assert self.loc1 == self.i1.get_location()
        assert os.path.exists(os.path.join(self.i1.get_location(),"usr"))
        self.i2 = self.i1.create_snapshot(self.loc2)
        assert self.loc2 == self.i2.get_location()
        assert os.path.exists(os.path.join(self.i2.get_location(), "usr"))
        self.i2.rmi()

    def tearDown(self):
        try:
            self.i1.rmi()
        except:
            pass
        try:
            self.i2.rmi()
        except:
            pass


class testContainer(Test):
    """
    It tests Container object and his abilities to run various commands
    """
    c1 = None
    cname = "contA"
    def setUp(self):
        loc1 = "/tmp/dddd1"
        self.i1 = Image(repos=["http://ftp.fi.muni.cz/pub/linux/fedora/linux/releases/26/Everything/x86_64/os/"],
                        packageset=["bash", "systemd"], location=loc1, ignore_installed=True)

    def test_basic(self):
        self.c1 = Container(image=self.i1, name=self.cname)
        self.c1.boot_machine()
        assert "sbin" in self.c1.execute(command="ls /").stdout


    def test_basic_noname(self):
        self.c1 = Container(image=self.i1)
        self.c1.boot_machine()
        assert "sbin" in self.c1.execute(command="ls /").stdout

    def test_basic_systemd_run(self):
        self.c1 = Container(image=self.i1, name=self.cname)
        self.c1.boot_machine()
        assert "sbin" in self.c1.run_systemdrun(command="ls /").stdout

    def test_basic_systemd_run_no_wait(self):
        class ContainerNoWait(Container):
            def _run_systemdrun_decide(self):
                return False
        self.c1 = ContainerNoWait(image=self.i1, name=self.cname)
        self.c1.boot_machine()
        assert "sbin" in self.c1.run_systemdrun(command="ls /").stdout


    def BAD_test_basic_machinectl_shell(self):
        # this test is able to break machine (lock machinectl)
        self.c1 = Container(image=self.i1, name=self.cname)
        self.c1.boot_machine()
        assert "sbin" in self.c1.run_machinectl(command="ls /").stdout


    def test_copy(self):
        self.c1 = Container(image=self.i1, name=self.cname)
        self.c1.boot_machine()
        ff1 = "/tmp/ee"
        ff2 = "/tmp/eee"
        process.run("rm -f %s %s" % (ff1, ff2), ignore_status=True)
        self.c1.execute("rm -f %s %s" %(ff1, ff2), ignore_status=True)
        process.run("echo outside > %s" % ff1, shell=True)
        assert "outside" in process.run("cat %s" % ff1).stdout
        self.c1.copy_to(ff1, ff2)
        assert "outside" in self.c1.execute("cat %s" % ff2).stdout
        self.c1.execute("echo inside > %s" % ff1)
        assert "inside" in self.c1.execute("cat %s" % ff1).stdout
        self.c1.copy_from(ff1, ff2)
        assert "inside" in process.run("cat %s" % ff2).stdout

    def test_boot_command(self):
        self.c1 = Container(image=self.i1, name=self.cname)
        self.c1.boot_machine(boot_cmd="sleep 100")
        assert "sleep 100" in process.run("machinectl status %s" % self.cname).stdout
        self.c1.stop()
        try:
            process.run("machinectl status %s" % self.cname)
        except:
            pass
        else:
            assert False

    def test_boot_command_wait(self):
        self.c1 = Container(image=self.i1, name=self.cname)
        sleep_time = 10
        t_before = time.time()
        self.c1.boot_machine(boot_cmd="sleep %s" % sleep_time, wait_finish=True)
        t_after = time.time()
        assert (t_after - t_before) > sleep_time
        assert (t_after - t_before) < sleep_time*1.5
        try:
            process.run("machinectl status %s" % self.cname)
        except:
            pass
        else:
            assert False


    def test_container_additional_options(self):
        self.c1 = Container(image=self.i1, name=self.cname)
        self.c1.boot_machine(nspawn_add_option_list=["--private-network"])
        assert "sbin" in self.c1.execute(command="ls /").stdout
        ifaces = self.c1.execute(command="cat /proc/net/dev")
        print ifaces
        assert "lo:" in ifaces.stdout
        assert len(ifaces.stdout.split("\n")) > 2
        assert  len(ifaces.stdout.split("\n"))<=4

    def tearDown(self):
        self.c1.stop()