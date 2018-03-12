#!/usr/bin/python
# -*- coding: utf-8 -*-
# Tool to start MTF tests
# Author Petr Sklenar psklenar@gmail.com
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

import argparse
import os
import tempfile
import json
import glob
import imp
import re

import subprocess
import core, common, mtfexceptions
#from moduleframework.common import conf, get_module_type, get_config, get_backend_list, list_modules_from_config
#from moduleframework.core import print_info, print_debug
from mtf.metadata.tmet.filter import filtertests
from mtf.metadata.tmet import common as metadata_common
#from moduleframework.mtfexceptions import DefaultConfigExc, ModuleFrameworkException


def mtfparser():
    # for right name of man; man page generator needs it: script_name differs, its defined in setup.py
    script_name = "mtf"
    description = \
"""
VARIABLES

    AVOCADO_LOG_DEBUG=yes enables avocado debug output.

    DEBUG=yes enables debugging mode to test output.

    CONFIG defines the module configuration file. It defaults to config.yaml.

    MODULE defines tested module type, if default-module is not set in config.yaml.

            =docker uses the docker section of config.yaml.
            =rpm uses the rpm section of config.yaml and tests RPMs directly on a host.
            =nspawn tests RPMs in a virtual environment with systemd-nspawn.

    URL overrides the value of module.docker.container or module.rpm.repo.
       The URL should correspond to the MODULE variable, for example:
            URL=docker.io/modularitycontainers/haproxy if MODULE=docker
            URL=https://phracek.fedorapeople.org/haproxy-module-repo # if MODULE=nspawn or MODULE=rpm

    MODULEMDURL overwrites the location of a moduleMD file.

    COMPOSEURL overwrites the location of a compose Pungi build.

    MTF_SKIP_DISABLING_SELINUX=yes
       does not disable SELinux. In nspawn type on Fedora 25 SELinux should be disabled,
       because it does not work well with SELinux enabled.

    MTF_DO_NOT_CLEANUP=yes does not clean up module after tests execution.

    MTF_REUSE=yes uses the same module between tests. It speeds up test execution.

    MTF_REMOTE_REPOS=yes disables downloading of Koji packages and creating a local repo.

    MTF_DISABLE_MODULE=yes disables module handling to use nonmodular test mode.
"""
    parser = argparse.ArgumentParser(
        # TODO
        prog="{0}".format(script_name),
        description=description,
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="see http://meta-test-family.readthedocs.io for more info",
        usage="[VARIABLES] {0} [options] local_tests".format(script_name),
    )
    parser.add_argument("--linter", "-l", action="store_true",
                        default=False, help='adds additional compose checks')
    parser.add_argument("--setup", action="store_true",
                        default=False, help='Setup by mtfenvset')
    parser.add_argument("--action", action="store", default='run',
                        help='Action for avocado, see avocado --help for subcommands')
    parser.add_argument("--version", action="store_true",
                        default=False, help='show version and exit')
    parser.add_argument("--metadata", action="store_true",
                        default=False, help="""load configuration for test sets from metadata file
                        (https://github.com/fedora-modularity/meta-test-family/blob/devel/mtf/metadata/README.md)""")


    # Solely for the purpose of manpage generator, copy&paste from setup.py
    parser.man_short_description = \
""" 
tool to test components for a modular Fedora.

mtf is a main binary file of Meta-Test-Family.

It tests container images and/or modules with user defined tests using avocado framework as test runner.
"""

    # parameters tights to avocado
    group_avocado = parser.add_argument_group(
        'arguments forwarded to avocado')

    group_avocado.add_argument(
        "--xunit", action="store", help='Enable xUnit result format and write it to FILE. Use - to redirect to the standard output.')
    # some useful bash variables
    # there are more possible variables up to the doc, not sure what could be like options too
    group = parser.add_argument_group(
        'additional arguments are like environment variables up to the http://meta-test-family.readthedocs.io/en/latest/user_guide/environment_variables.html ')
    group.add_argument("--module", action="store",
                       help='Module type, like: docker, nspawn, rpm or openshift')
    group.add_argument("--debug", action="store_true", help='more logging')
    group.add_argument("--config", action="store",
                       help='defines the module configuration file')
    group.add_argument("--url", action="store",
                       help='URL overrides the value of module.docker.container or module.rpm.repo.')
    group.add_argument("--modulemdurl", action="store",
                       help='overwrites the location of a moduleMD file')
    return parser


def cli():
    # unknown options are forwarded to avocado run
    args, unknown = mtfparser().parse_known_args()

    if args.version:
        print "0.7.7"
        exit(0)

    # uses additional arguments, set up variable asap, its used afterwards:
    if args.debug:
        os.environ['DEBUG'] = 'yes'
        os.environ['AVOCADO_LOG_DEBUG'] = 'yes'
    if args.config:
        os.environ['CONFIG'] = args.config
    if args.url:
        os.environ['URL'] = args.url
    if args.modulemdurl:
        os.environ['MODULEMDURL'] = args.modulemdurl

    core.print_debug("Options: linter={0}, setup={1}, action={2}, module={3}".format(
        args.linter, args.setup, args.action, args.module))
    core.print_debug(
        "remaining options for avocado or test files: {0}".format(unknown))

    # environment usage:
    #   read: os.environ.get('MODULE')
    #   write: os.environ['MODULE']

    # MODULE could be from:
    #   1. environment ... MODULE=docker etc
    #   2. argument ... --module=docker
    #   3. from config.yaml in default_module
    #   4. default module stored in general mtf config yaml file

    if os.environ.get('MODULE') is not None:
        # environment is the highest priority because mtf uses environment (too much)
        args.module = os.environ['MODULE']
    if not args.module:
        args.module = common.get_module_type()

    os.environ['MODULE'] = args.module

    if not os.environ.get('URL'):
        try:
            common.get_config(reload=True)
        except mtfexceptions.DefaultConfigExc:
            raise mtfexceptions.DefaultConfigExc("You have to set URL variable (via URL envar or --url parameter) in case of default config")
    supported_modules = set(common.get_backend_list() + common.list_modules_from_config())
    if args.module in supported_modules:
        # for debug purposes, to be sure about module variables or options
        core.print_debug("MODULE={0}, options={1}".format(
            os.environ.get('MODULE'), args.module))
    else:
        # TODO: what to do here? whats the defaults value for MODULE, do I know it?
        raise mtfexceptions.ModuleFrameworkException("MODULE={0} ; we support {1}".format(
            os.environ.get('MODULE'), supported_modules))

    core.print_debug("MODULE={0}".format(os.environ.get('MODULE')))
    return args, unknown


class AvocadoStart(object):
    tests = []
    json_tmppath = None
    additionalAvocadoArg = []
    AVOCADO = "avocado"
    A_KNOWN_PARAMS_SIMPLE=["-s", "-z", "-v", "-V",
                           "--silent",
                           "--show-job-log",
                           "--replay-resume",
                           "--filter-by-tags-include-empty",
                           "--archive",
                           "--journal",
                           "--"
                           ]
    def __init__(self, args, unknown):
        # choose between TESTS and ADDITIONAL ENVIRONMENT from options
        if args.linter:
            self.tests += glob.glob("{MTF_TOOLS}/{GENERIC_TEST}/*.py".format(
                MTF_TOOLS=metadata_common.MetadataLoaderMTF.MTF_LINTER_PATH,
                GENERIC_TEST=common.conf["generic"]["generic_tests"]))
            self.tests += glob.glob("{MTF_TOOLS}/{STATIC_LINTERS}/*.py".format(
                MTF_TOOLS=metadata_common.MetadataLoaderMTF.MTF_LINTER_PATH,
                STATIC_LINTERS=common.conf["generic"]["static_tests"]))
        self.args = args

        # parse unknow options and try to find what parameter is test
        while unknown:
            if unknown[0] in self.A_KNOWN_PARAMS_SIMPLE:
                self.additionalAvocadoArg.append(unknown[0])
                unknown = unknown[1:]
            elif unknown[0].startswith("-"):
                if "=" in unknown[0] or len(unknown) < 2:
                    self.additionalAvocadoArg.append(unknown[0])
                    unknown = unknown[1:]
                else:
                    self.additionalAvocadoArg += unknown[0:2]
                    unknown = unknown[2:]
            elif glob.glob(unknown[0]):
                # dereference filename via globs
                testlist = glob.glob(unknown[0])
                self.tests += testlist
                unknown = unknown[1:]
            else:
                self.tests.append(unknown[0])
                unknown = unknown[1:]

        if self.args.metadata:
            core.print_info("Using Metadata loader for tests and filtering")
            metadata_tests = filtertests(backend="mtf", location=os.getcwd(), linters=False, tests=[], tags=[], relevancy="")
            tests_dict = [x[metadata_common.SOURCE] for x in metadata_tests]
            self.tests += tests_dict
            core.print_debug("Loaded tests via metadata file: %s" % tests_dict)
        core.print_debug("tests = {0}".format(self.tests))
        core.print_debug("additionalAvocadoArg = {0}".format(
            self.additionalAvocadoArg))

    def check_tests(self):
        summary_line = "TEST TYPES SUMMARY"
        prefix_line = "Type"
        output = subprocess.check_output([self.AVOCADO, "list", "-V", "--"] + self.tests)
        assert summary_line in output
        badstates = ["NOT_A_TEST", "MISSING", "ACCESS_DENIED", "BROKEN_SYMLINK"]
        badtests = []
        # remove header line and remove last lines with is test types summary
        testlines = []
        for line in output.split("\n"):
            testline = line.strip()
            if testline.startswith(prefix_line) or not testline:
                continue
            elif testline.startswith(summary_line):
                break
            else:
                splitted = testline.split(" ", 1)
                if splitted[0] in badstates:
                    badtests.append(splitted[1].strip())
        if badtests:
            core.print_info("", "ERROR: There are bad tests:", "-------------")
            core.print_info(*badtests)
            exit(19)

    def avocado_run(self):
        self.check_tests()
        self.json_tmppath = tempfile.mktemp()
        avocado_args = ["--json", self.json_tmppath]
        if self.args.xunit:
            avocado_args += ["--xunit", self.args.xunit]
        return self.avocado_general(action=self.args.action, avocado_default_args=avocado_args)

    def avocado_general(self, action, avocado_default_args=[]):
        """

        :param action: what avocado action to run: run, list, ...
        :param avocado_default_args: list avocado additional argument
        :return: return code of executed avocado command
        """
        rc=0
        try:
            subprocess.check_call([self.AVOCADO, action] + avocado_default_args + self.additionalAvocadoArg + self.tests)
        except subprocess.CalledProcessError as cpe:
            rc = cpe.returncode
        return rc

    def _tcinfo(self, testcases, header, logs=True, description=True):
        """
        Parse testcases dics and print output for them in nicer format
        Main purpose is to display docstrings of testcases for failures
        example:
            def test_some(something)
                '''
                This is line1.
                This is line2.
                :return: None
                '''
                self.assertTrue(False, msg="This is fail reason")
        procudes line:    desc -> This is line1. This is line2.
                          reason -> This is fail reason
        :param testcases: dict of testcases
        :param header: str what to print as header
        :param logs: boolean if print logs for these testcases (default True)
        :param description: boolean if print description = docs strings for test class + function
        :return: None
        """
        if testcases:
            emptydelimiter = ""
            harddelimiter = "------------------------"
            core.print_info(emptydelimiter, "{0} {1} {0}".format(harddelimiter, header))
            for testcase in testcases:
                tcname = testcase
                if re.search('^[0-9]+-', testcase.get('id',"")):
                    tcname = testcase.get('id').split("-", 1)[1]
                tcnameoutput = tcname
                splitted = re.search("(.*):(.+)\.(.+)$", tcname)
                if splitted:
                    docstrcls = []
                    docstrtst = []
                    testfile, classname, fnname = splitted.groups()
                    try:
                        testmodule = imp.load_source("test", testfile)
                        if getattr(testmodule, classname).__doc__:
                            docstrcls = getattr(testmodule, classname).__doc__.strip().split("\n")
                        if getattr(getattr(testmodule, classname), fnname).__doc__:
                            docstrtst = getattr(getattr(testmodule, classname), fnname).__doc__.strip().split("\n")
                        tcnameoutput = " ".join([x for x in docstrcls + docstrtst if not re.search(":.*:", x)])
                        # TODO: replace more whitespaces just by one - we should find better solution how to that
                        tcnameoutput = ' '.join(tcnameoutput.split())
                    except Exception as e:
                        core.print_debug("(INFO) Error happen when parsing testcase name ({})".format(tcname), e)
                        pass
                core.print_info("TEST {0}:  {1}".format(testcase.get('status'), tcname))
                if description and tcnameoutput!=tcname and tcnameoutput and tcnameoutput.strip():
                    core.print_info("     desc -> {0}".format(tcnameoutput))
                if testcase.get('fail_reason') and testcase.get('fail_reason') != "None":
                    core.print_info("     reason -> {0}".format(testcase.get('fail_reason')))
                if logs:
                    core.print_info("     {0}".format(testcase.get('logfile')))
                core.print_info(emptydelimiter)

    def show_error(self):
        if os.path.exists(self.json_tmppath):
            try:
                # file has to by json, otherwise it fails
                json_data = open(self.json_tmppath).read()
                data = json.loads(json_data)
            except (IOError, ValueError) as e:
                # file is not readable as json: No JSON object could be decoded
                print(e)
                # remove file as its not readable
                os.remove(self.json_tmppath)
                # fatal error when this command fails, its unexpected
                exit(127)
            FAILS = ['ERROR', 'FAIL']
            SKIPS = ['SKIP', 'CANCEL']
            skipstatuses = [x for x in data['tests'] if x.get('status') in SKIPS]
            failstatuses = [x for x in data['tests'] if x.get('status') in FAILS]
            self._tcinfo(skipstatuses, "SKIPPED TESTS", logs=False)
            self._tcinfo(failstatuses, "FAILED TESTS")
            os.remove(self.json_tmppath)


def main():
    core.print_debug('verbose/debug mode')
    args, unknown = cli()

    if args.setup:
        # mtfenvset need bash environment!
        from moduleframework.mtf_environment import mtfenvset
        mtfenvset()

    a = AvocadoStart(args, unknown)
    if args.action == 'run':
        returncode = a.avocado_run()
        a.show_error()
    else:
        # when there is any need, change general method or create specific one:
        returncode = a.avocado_general(action=args.action)
    exit(returncode)




