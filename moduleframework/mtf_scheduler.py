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
import moduleframework
import tempfile
import textwrap
import sys
import json

from avocado.utils import process
from moduleframework import common


def mtfparser():
    # for right name of man; man page generator needs it: script_name differs, its defined in setup.py
    script_name = "mtf"
    parser = argparse.ArgumentParser(
        # TODO
        prog="{0}".format(script_name),
        description=textwrap.dedent('''\
        unknown arguments are forwarded to avocado:
           optionally use additional avocado param like --show-job-log, see avocado action --help'''),
        formatter_class=argparse.RawTextHelpFormatter,
        # epilog(with http link) is used in some error msg too:
        epilog="see http://meta-test-family.readthedocs.io for more info",
        usage="{0} [options] local_tests".format(script_name),
    )
    parser.add_argument("--linter", "-l", action="store_true",
                        default=False, help='adds additional compose checks')
    parser.add_argument("--setup", action="store_true",
                        default=False, help='Setup by mtfenvset')
    parser.add_argument("--action", action="store", default='run',
                        help='Action for avocado, see avocado --help for subcommands')
    # Solely for the purpose of manpage generator, copy&paste from setup.py
    parser.man_short_description = "tool to test components for a modular Fedora"

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
                       help='Module type, like: docker, nspawn or rpm')
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

    common.print_debug("Options: linter={0}, setup={1}, action={2}, module={3}".format(
        args.linter, args.setup, args.action, args.module))
    common.print_debug(
        "remaining options for avocado or test files: {0}".format(unknown))

    # environment usage:
    #   read: os.environ.get('MODULE')
    #   write: os.environ['MODULE']

    # MODULE could be from:
    #   1. common.get_module_type() ... it reads config.yaml and treceback if it doesn't exist
    #   2. environment ... MODULE=docker etc
    #   3. argument ... --module=docker
    try:
        args.module = common.get_module_type()
        # TODO it wrongly writes: 'Using default minimal config ...', change in common.py
    except moduleframework.mtfexceptions.ModuleFrameworkException:
        pass

    if os.environ.get('MODULE') is not None:
        # environment is the highest priority because mtf uses environment (too much)
        args.module = os.environ['MODULE']

    if args.module:
        # setup also environment
        os.environ['MODULE'] = args.module

    if args.module in common.get_backend_list():
        # for debug purposes, to be sure about module variables or options
        common.print_debug("MODULE={0}, options={1}".format(
            os.environ.get('MODULE'), args.module))
    else:
        # TODO: what to do here? whats the defaults value for MODULE, do I know it?
        common.print_info("MODULE={0} ; we support {1} \n === expecting your magic, enjoy! === ".format(
            os.environ.get('MODULE'), common.get_backend_list()))

    common.print_debug("MODULE={0}".format(os.environ.get('MODULE')))
    return args, unknown


class AvocadoStart(object):
    def __init__(self, args, unknown):

        # its used for filepath in loadCli:
        self.json_tmppath = None
        site_libs = os.path.dirname(moduleframework.__file__)
        mtf_tools = "tools"

        # choose between TESTS and ADDITIONAL ENVIRONMENT from options
        self.tests = ''
        if args.linter:
            self.tests = (
                "{SITE_LIB}/{MTF_TOOLS}/*.py".format(SITE_LIB=site_libs, MTF_TOOLS=mtf_tools))
        self.additionalAvocadoArg = ''
        self.args = args

        for param in unknown:
            # take care of this, see tags for safe/unsafe:
            # http://avocado-framework.readthedocs.io/en/52.0/WritingTests.html#categorizing-tests
            if os.path.exists(param):
                # this is list of tests in local file
                self.tests += " {0} ".format(param)
            else:
                # this is additional avocado param
                self.additionalAvocadoArg += " {0} ".format(param)

        common.print_debug("tests = {0}".format(self.tests))
        common.print_debug("additionalAvocadoArg = {0}".format(
            self.additionalAvocadoArg))

    def avocado_run(self):
        self.json_tmppath = tempfile.mktemp()
        avocado_args = "--json {JSON_LOG}".format(
            JSON_LOG=self.json_tmppath)
        if self.args.xunit:
            avocado_args += " --xunit {XUNIT} ".format(XUNIT=self.args.xunit)
        avocadoAction = "avocado {ACTION} {AVOCADO_ARGS}".format(
            ACTION=self.args.action, AVOCADO_ARGS=avocado_args)

        # run avocado with right cmd arguments
        bash = process.run("{AVOCADO} {a} {b}".format(
            AVOCADO=avocadoAction, a=self.additionalAvocadoArg, b=self.tests), shell=True, ignore_status=True)
        common.print_info(bash.stdout, bash.stderr)
        common.print_debug("Command used: ", bash.command)
        return bash.exit_status

    def avocado_general(self):
        # additional parameters
        # self.additionalAvocadoArg: its from cmd line, whats unknown to this tool
        avocado_args = ""  # when needed => specify HERE your additional stuff
        avocadoAction = "avocado {ACTION} {AVOCADO_ARGS}".format(
            ACTION=self.args.action, AVOCADO_ARGS=avocado_args)
        bash = process.run("{AVOCADO} {a} {b}".format(
            AVOCADO=avocadoAction, a=self.additionalAvocadoArg, b=self.tests), shell=True, ignore_status=True)
        common.print_info(bash.stdout, bash.stderr)
        common.print_debug("Command used: ", bash.command)
        return bash.exit_status

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
            # errors follow after 'normal' output with no delimiter, then with -------
            delimiter = ""
            for testcase in data['tests']:
                if testcase.get('status') in ['ERROR', 'FAIL']:
                    common.print_info(delimiter)
                    common.print_info("TEST:   {0}".format(testcase.get('id')))
                    common.print_info("ERROR:  {0}".format(
                        testcase.get('fail_reason')))
                    common.print_info("        {0}".format(
                        testcase.get('logfile')))
                    delimiter = "-------------------------"
            os.remove(self.json_tmppath)


def main():
    common.print_debug('verbose/debug mode')
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
        returncode = a.avocado_general()
    exit(returncode)




