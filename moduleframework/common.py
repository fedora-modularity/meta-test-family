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
Custom configuration and debugging library.
"""

import netifaces
import socket
import os
import urllib
import yaml
import subprocess
import copy
import random
import string
import requests
import warnings
import ast
import glob
import avocado.utils
import mtfexceptions
import core


class MTFConfParser(dict):
    configdir = "mtf.conf.d"
    source_cfg = os.path.join(*(["/"] + core.DATADIR + [configdir]))
    default_cfg = os.path.join("/etc", configdir)
    user_cfg = os.path.expanduser("~/." + configdir)
    pattern = "*.yaml"

    def __init__(self):
        config = {}
        for cfgdir in [self.source_cfg, self.default_cfg, self.user_cfg]:
            core.print_debug("MTF config dir search: {}".format(cfgdir))
            if os.path.exists(cfgdir):
                core.print_info("MTF config dir exists, search for {}/{}".format(cfgdir, self.pattern))
                for cfgfile in glob.glob(os.path.join(cfgdir, self.pattern)):
                    core.print_info("MTF config load: {}".format(cfgfile))
                    config.update(yaml.load(open(cfgfile)))
        assert config.get("generic")
        super(MTFConfParser, self).__init__(config)


conf = MTFConfParser()


defroutedev = netifaces.gateways().get('default').values(
)[0][1] if netifaces.gateways().get('default') else "lo"
hostipaddr = netifaces.ifaddresses(defroutedev)[2][0]['addr']
hostname = socket.gethostname()
dusername = "test"
dpassword = "test"
ddatabase = "basic"
hostpackager = subprocess.check_output([conf["generic"]["packager_cmd"]], shell=True).strip()
guestpackager = hostpackager

__persistent_config = None

# translation table for {VARIABLE} in the config.yaml file
trans_dict = {"HOSTIPADDR": hostipaddr,
              "GUESTIPADDR": hostipaddr,
              "DEFROUTE": defroutedev,
              "HOSTNAME": hostname,
              "ROOT": "/",
              "USER": dusername,
              "PASSWORD": dpassword,
              "DATABASENAME": ddatabase,
              "HOSTPACKAGER": hostpackager,
              "GUESTPACKAGER": guestpackager,
              "GUESTARCH": conf["generic"]["arch"],
              "HOSTARCH": conf["generic"]["arch"]
              }


def generate_unique_name(size=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(size))


def get_openshift_local():
    """
    Return the **OPENSHIFT_LOCAL** envvar.
    :return: bool
    """
    return bool(os.environ.get('OPENSHIFT_LOCAL'))


def get_openshift_ip():
    """
    Return the **OPENSHIFT_IP** envvar or None.
    :return: OpenShift IP or None
    """
    return os.environ.get('OPENSHIFT_IP') or conf.get("openshift",{}).get("ip")


def get_openshift_user():
    """
    Return the **OPENSHIFT_USER** envvar or None.
    :return: OpenShift User or None
    """
    return os.environ.get('OPENSHIFT_USER') or conf.get("openshift",{}).get("user")


def get_openshift_passwd():
    """
    Return the **OPENSHIFT_PASSWORD** envvar or None.
    :return: OpenShift password or None
    """
    return os.environ.get('OPENSHIFT_PASSWORD') or conf.get("openshift",{}).get("password")


def get_if_install_default_profile():
    """
        Return the **MTF_INSTALL_DEFAULT** envvar.

        :return: bool
        """
    envvar = os.environ.get('MTF_INSTALL_DEFAULT')
    return bool(envvar)


def is_recursive_download():
    """
    Return the **MTF_RECURSIVE_DOWNLOAD** envvar.

    :return: bool
    """
    return bool(os.environ.get("MTF_RECURSIVE_DOWNLOAD"))


def get_if_do_cleanup():
    """
    Return the **MTF_DO_NOT_CLEANUP** envvar.

    :return: bool
    """
    cleanup = os.environ.get('MTF_DO_NOT_CLEANUP')
    return not bool(cleanup)


def get_if_reuse():
    """
        Return the **MTF_REUSE** envvar.

        :return: bool
        """
    reuse = os.environ.get('MTF_REUSE')
    return bool(reuse)


def get_if_remoterepos():
    """
    Return the **MTF_REMOTE_REPOS** envvar.

    :return: bool
    """
    remote_repos = os.environ.get('MTF_REMOTE_REPOS')
    return bool(remote_repos)


def get_odcs_envvar():
    return os.environ.get('MTF_ODCS')


def is_true(value):
    # which values are considered as true
    true_values = ['yes', 'YES', 'yes', 'True', 'true', 'ok', 'OK']
    if isinstance(value, str) and value in true_values:
        return True
    return False


def get_openidc_auth():
    """
    use ODCS for creating composes as URL parameter
    It enables this feature in case MTF_ODCS envvar is set
    MTF_ODCS=yes -- use openidc and token for your user
    MTF_ODCS=OIDC_token_string -- use this token for authentication

    :envvar MTF_ODCS: yes or token
    :return:
    """
    odcstoken = get_odcs_envvar()

    # in case you dont have token enabled, try to ask for openidc via web browser
    if is_true(odcstoken):
        if conf.get("openidc").get("token"):
            # use value defined in config file if defined
            return conf["openidc"]["token"]
        # to not have hard dependency on openidc (use just when using ODCS without defined token)
        import openidc_client
        # Get the auth token using the OpenID client.
        oidc = openidc_client.OpenIDCClient(*conf["openidc"]["auth"])
        scopes = conf["openidc"]["scopes"]
        try:
            odcstoken = oidc.get_token(scopes, new_token=True)
        except requests.exceptions.HTTPError as e:
            core.print_info(e.response.text)
            raise mtfexceptions.ModuleFrameworkException("Unable to get token via OpenIDC for your user")
    if odcstoken and len(odcstoken)<10:
        raise mtfexceptions.ModuleFrameworkException("Unable to parse token for ODCS, token is too short: %s" % odcstoken)
    return odcstoken


def get_if_module():
    """
    Return the **MTF_DISABLE_MODULE** envvar.

    :return: bool
    """
    disable_module = os.environ.get('MTF_DISABLE_MODULE')
    return not bool(disable_module)


def sanitize_text(text, replacement="_", invalid_chars=["/", ";", "&", ">", "<", "|"]):

    """
    Replace invalid characters in a string.

    invalid_chars=["/", ";", "&", ">", "<", "|"]

    :param replacement: text to sanitize
    :param invalid_chars: replacement char, default: "_"
    :return: str
    """
    for char in invalid_chars:
        if char in text:
            text = text.replace(char, replacement)
    return text


def sanitize_cmd(cmd):
    """
    Escape apostrophes in a command line.

    :param cmd: command to sanitize
    :return: str
    """
    if '"' in cmd:
        cmd = cmd.replace('"', r'\"')
    return cmd


def translate_cmd(cmd, translation_dict=None):
    if not translation_dict:
        return cmd
    try:
        formattedcommand = cmd.format(**translation_dict)
    except KeyError:
        raise mtfexceptions.ModuleFrameworkException(
            "Command is formatted by using trans_dict. If you want to use "
            "brackets { } in your code, please use {{ }}. Possible values "
            "in trans_dict are: %s. \nBAD COMMAND: %s"
            % (translation_dict, cmd))
    return formattedcommand


def get_profile():
    """
    Return a profile name.

    If the **PROFILE** envvar is not set, a profile name is
    set to be `default`.

    :return: str
    """

    return os.environ.get('PROFILE') or conf["modularity"]["default_profile"]


def get_url():
    """
    Return the **URL** envvar.

    :return: str
    """
    url = os.environ.get('URL')
    return url


def get_compose_url():
    """
    Return Compose URL.

    If the **COMPOSEURL** ennvar is not set, it's defined from the ``./config.yaml``.

    :return: str
    """
    readconfig = get_config()
    compose_url = os.environ.get('COMPOSEURL') or readconfig.get("compose-url")
    return [compose_url] if compose_url else []


def get_modulemdurl():
    """
    Read a moduleMD file.

    If the **MODULEMDURL** envvar is not set, module-url section of
    the ``config.yaml`` file is checked. If none of them is set, then
    the ***COMPOSE_URL* envvar is checked.

    :return: string
    """
    mdf = os.environ.get('MODULEMDURL')
    return mdf


class CommonFunctions(object):
    """
    Basic class to read configuration data and execute commands on a host machine.
    """
    config = None
    modulemdConf = None
    component_name = None
    source = None
    arch = None
    sys_arch = None
    is_it_module = False
    packager = None
    # general use case is to have forwarded services to host (so thats why it is same)
    _ip_address = trans_dict["HOSTIPADDR"]
    _dependency_list = None

    def __init__(self, *args, **kwargs):
        # general use case is to have forwarded services to host (so thats why it is same)
        trans_dict["GUESTARCH"] = self.getArch()
        self.loadconfig()

    def loadconfig(self):
        """
        Load configuration from config.yaml file.

        :return: None
        """
        # we have to copy object. because there is just one global object, to improve performance
        self.config = copy.deepcopy(get_config(reload=True))
        self.info = self.config.get("module", {}).get(get_module_type_base())
        # if there is inheritance join both dictionary
        self.info.update(self.config.get("module", {}).get(get_module_type()))
        if not self.info:
            raise mtfexceptions.ConfigExc("There is no section for (module: -> %s:) in the configuration file." %
                            get_module_type_base())

        if self.config.get('modulemd-url') and get_if_module():
            self.is_it_module = True
        else:
            pass

        self.component_name = sanitize_text(self.config['name'])
        self.source = self.config.get('source')
        self.set_url()

    def set_url(self, url=None, force=False):
        """
        Set url via parameter or via URL envvar
        It is repo or image name.

        :envvar: **URL=url://localtor or docker url locator** overrides default value.
        :param url:
        :param force:
        :return:
        """
        url = url or get_url() or self.info.get("url")
        if url and ((not self.info.get("url")) or force):
                self.info["url"] = url

        if not self.info.get("url"):
            if get_module_type_base() in ["docker", "openshift"]:
                self.info["url"]=self.info.get("container")
            elif get_module_type_base() in ["rpm", "nspawn"]:
                self.info["url"] = self.info.get("repo") or self.info.get("repos")
        # url has to be dict in case of rpm/nspanw (it is allowed to use ; as separator for more repositories)
        if get_module_type_base() in ["rpm", "nspawn"] and isinstance(self.info["url"], str):
            self.info["url"] = self.info["url"].split(";")

    def get_url(self):
        """
        get location of repo(s) or image

        :return: str
        """
        return self.info.get("url")

    def get_template(self):
        """
        get location of template from config.yaml file
        :return: str
        """
        return self.info.get(conf["openshift"]["template"])

    def get_docker_pull(self):
        """
        Gets boolean value if image should be pulled or not.
        :return: bool
        """
        docker_pull = self.info.get("docker_pull")
        if docker_pull is None:
            return True
        try:
            return ast.literal_eval(docker_pull)
        except ValueError:
            return False

    def getArch(self):
        """
        Get system architecture.

        :return: str
        """
        if not self.sys_arch:
            self.sys_arch = self.runHost(command='uname -m', verbose=False).stdout.strip()
        return self.sys_arch

    def runHost(self, command="ls /", **kwargs):
        """
        Run commands on a host.

        :param common: command to exectute
        ** kwargs: avocado.utils.process.run params like: shell, ignore_status, verbose
        :return: avocado.process.run
        """

        return avocado.utils.process.run("%s" % translate_cmd(command, translation_dict=trans_dict), **kwargs)

    def get_test_dependencies(self):
        """
        Get test dependencies from a configuration file

        :return: list of test dependencies
        """
        return self.config.get('testdependencies', {}).get('rpms', [])

    def installTestDependencies(self, packages=None):
        """
        Install packages on a host machine to prepare a test environment.

        :param (list): packages to install. If not specified, rpms from config.yaml
                       will be installed.
        :return: None
        """
        if not packages:
            packages = self.get_test_dependencies()

        if packages:
            core.print_info("Installs test dependencies: ", packages)
            # you have to have root permission to install packages:
            try:
                self.runHost(
                    "{HOSTPACKAGER} install " +
                    " ".join(packages),
                    ignore_status=False, verbose=core.is_debug())
            except avocado.utils.process.CmdError as e:
                raise mtfexceptions.CmdExc("Installation failed; Do you have permission to do that?", e)

    def getPackageList(self, profile=None):
        """
        Return list of packages what has to be installed inside module

        :param profile: get list for intended profile instead of default method for searching
        :return: list of packages (rpms)
        """
        package_list = []
        mddata = self.getModulemdYamlconfig()
        if not profile:
            if 'packages' in self.config:
                packages_rpm = self.config.get('packages', {}).get('rpms', [])
                packages_profiles = []
                for profile_in_conf in self.config.get('packages', {}).get('profiles', []):
                    packages_profiles += mddata['data']['profiles'][profile_in_conf]['rpms']
                package_list += packages_rpm + packages_profiles
            if get_if_install_default_profile():
                profile_append = mddata.get('data', {})\
                    .get('profiles', {}).get(get_profile(), {}).get('rpms', [])
                package_list += profile_append
        else:
            package_list += mddata['data']['profiles'][profile].get('rpms', [])
        core.print_info("PCKGs to install inside module:", package_list)
        return package_list

    def getModuleDependencies(self):
        """
        Return module dependencies.

        :return: list
        """
        warnings.warn("Function getModuleDependencies is deprecated. Use self.dependency_list instead",
                      DeprecationWarning)
        return self.dependency_list

    @property
    def dependency_list(self):
        """
        Return module dependencies.

        :return: list
        """

        return self._dependency_list

    @dependency_list.setter
    def dependency_list(self, value):
        self._dependency_list = value

    def getModulemdYamlconfig(self, urllink=None):
        """
        Return moduleMD file yaml object.
        It can be used also for loading another yaml file via url parameter

        :param (str): url link to load. Default url defined in the `config.yaml` file,
                      can be overridden by the **CONFIG** envvar.
        :return: dict
        """
        link = {"data": {}}
        if urllink:
            modulemd = urllink
        elif self.is_it_module:
            if self.modulemdConf:
                return self.modulemdConf
            else:
                modulemd = get_modulemdurl()
                if not modulemd:
                    modulemd = self.config.get("modulemd-url")
        else:
            return link
        try:
            ymlfile = urllib.urlopen(modulemd)
            link = yaml.load(ymlfile)
        except IOError as e:
            raise mtfexceptions.ConfigExc("File '%s' cannot be load" % modulemd, e)
        except yaml.parser.ParserError as e:
            raise mtfexceptions.ConfigExc("Module MD file contains errors: '%s'" % e, modulemd)
        if not urllink:
            self.modulemdConf = link
        return link

    def getIPaddr(self):
        """
        Return protocol (IP or IPv6) address on a guest machine.

        In many cases it should be same as a host machine's and a port
        should be forwarded to a host.

        :return: str
        """
        return self.ip_address

    @property
    def ip_address(self):
        """
        Return protocol (IP or IPv6) address on a guest machine.

        In many cases it should be same as a host machine's and a port
        should be forwarded to a host.

        :return: str
        """
        return self._ip_address

    @ip_address.setter
    def ip_address(self, value):
        self._ip_address = value

    def _callSetupFromConfig(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """
        if self.info.get("setup"):
            self.runHost(self.info.get("setup"), shell=True, ignore_bg_processes=True, verbose=core.is_not_silent())

    def _callCleanupFromConfig(self):
        """
        Internal method, do not use it anyhow

        :return: None
        """
        if self.info.get("cleanup"):
            self.runHost(self.info.get("cleanup"), shell=True, ignore_bg_processes=True, verbose=core.is_not_silent())

    def run(self, command, **kwargs):
        """
        Run command inside module, for local based it is same as runHost

        :param command: str of command to execute
        :param kwargs: dict from avocado.process.run
        :return: avocado.process.run
        """

        return self.runHost('bash -c "%s"' % sanitize_cmd(command), **kwargs)

    def get_packager(self):
        if not self.packager:
            self.packager = self.run(conf["generic"]["packager_cmd"], verbose=False).stdout.strip()
        return self.packager

    def status(self, command="/bin/true"):
        """
        Return status of module

        :param command: which command used for do that. it could be defined inside config
        :return: bool
        """
        try:
            command = self.info.get('status') or command
            a = self.run(command, shell=True, ignore_bg_processes=True, verbose=core.is_not_silent())
            core.print_debug("command:", a.command, "stdout:", a.stdout, "stderr:", a.stderr)
            return True
        except BaseException:
            return False

    def start(self, command="/bin/true"):
        """
        start the RPM based module (like systemctl start service)

        :param command: Do not use it directly (It is defined in config.yaml)
        :return: None
        """
        command = self.info.get('start') or command
        self.run(command, shell=True, ignore_bg_processes=True, verbose=core.is_debug())
        self.status()
        trans_dict["GUESTPACKAGER"] = self.get_packager()

    def stop(self, command="/bin/true"):
        """
        stop the RPM based module (like systemctl stop service)

        :param command: Do not use it directly (It is defined in config.yaml)
        :return: None
        """
        command = self.info.get('stop') or command
        self.run(command, shell=True, ignore_bg_processes=True, verbose=core.is_not_silent())

    def install_packages(self, packages=None):
        """
        Install packages in config (by config or via parameter)

        :param packages:
        :return:
        """
        if not packages:
            packages = self.getPackageList()
        if packages:
            a = self.run("%s install %s" % (self.get_packager()," ".join(packages)),
                         ignore_status=True,
                         verbose=False)
            if a.exit_status == 0:
                core.print_info("Packages installed via %s" % self.get_packager(), a.stdout)
            else:
                core.print_info(
                    "Nothing installed via %s, but package list is not empty" % self.get_packager(),
                    packages)
                raise mtfexceptions.CmdExc("ERROR: Unable to install packages inside: %s" % packages)

    def tearDown(self):
        """
        cleanup enviroment and call cleanup from config

        :return: None
        """
        if get_if_do_cleanup():
            self.stop()
            self._callCleanupFromConfig()
        else:
            core.print_info("TearDown phase skipped.")

    def copyTo(self, src, dest):
        """
        Copy file to module from host

        :param src: source file on host
        :param dest: destination file on module
        :return: None
        """
        if  src is not dest:
            self.run("cp -rf %s %s" % (src, dest))

    def copyFrom(self, src, dest):
        """
        Copy file from module to host

        :param src: source file on module
        :param dest: destination file on host
        :return: None
        """
        if src is not dest:
            self.run("cp -rf %s %s" % (src, dest))

    def run_script(self, filename, *args, **kwargs):
        """
        run script or binary inside module
        :param filename: filename to copy to module
        :param args: pass this args as cmdline args to run binary
        :param kwargs: pass thru to avocado process.run
        :return: avocado process.run object
        """
        dest = "/tmp/%s" % generate_unique_name()
        self.copyTo(filename, dest)
        #self.run("bash %s" % dest)
        parameters = ""
        if args:
            parameters = " " + " ".join(args)
        return self.run("bash " + dest + parameters, **kwargs)


def get_config(fail_without_url=True, reload=False):
    """
    Read the module's configuration file.

    :default: ``./config.yaml`` in the ``tests`` directory of the module's root
     directory
    :envvar: **CONFIG=path/to/file** overrides default value.
    :return: str
    """
    global __persistent_config
    if not __persistent_config or reload:
        cfgfile = os.environ.get('CONFIG')
        if cfgfile:
            if os.path.exists(cfgfile):
                core.print_debug("Config file defined via envvar: %s" % cfgfile)
            else:
                raise mtfexceptions.ConfigExc("File does not exist although defined CONFIG envvar: %s" % cfgfile)
        else:
            cfgfile = "./config.yaml"
            if os.path.exists(cfgfile):
                core.print_debug("Using module config file: %s" % cfgfile)
            else:
                if fail_without_url and not get_url():
                    raise mtfexceptions.DefaultConfigExc("You have to use URL envvar for testing your images or repos")
                cfgfile = "/usr/share/moduleframework/docs/example-config-minimal.yaml"
                core.print_debug("Using default minimal config: %s" % cfgfile)


        try:
            with open(cfgfile, 'r') as ymlfile:
                xcfg = yaml.load(ymlfile.read())
            doc_name = ['modularity-testing', 'meta-test-family', 'meta-test']
            if xcfg.get('document') not in doc_name:
                raise mtfexceptions.ConfigExc("bad yaml file: item (%s)" %
                                doc_name, xcfg.get('document'))
            if not xcfg.get('name'):
                raise mtfexceptions.ConfigExc("Missing (name:) in config file")
            if not xcfg.get("module"):
                raise mtfexceptions.ConfigExc("No module in yaml config defined")
            # copy rpm section to nspawn, in case not defined explicitly
            # make it backward compatible
            if xcfg.get("module", {}).get("rpm") and not xcfg.get("module", {}).get("nspawn"):
                xcfg["module"]["nspawn"] = copy.deepcopy(xcfg.get("module", {}).get("rpm"))
            __persistent_config = xcfg
            return xcfg
        except IOError:
            raise mtfexceptions.ConfigExc(
                "Error: File '%s' doesn't appear to exist or it's not a YAML file. "
                "Tip: If the CONFIG envvar is not set, mtf-generator looks for './config'."
                % cfgfile)
    else:
        return __persistent_config


def list_modules_from_config():
    """
    Get all possible modules based on config file

    :return: list
    """
    modulelist = get_config(fail_without_url=False).get("module",{}).keys()
    return modulelist


def get_backend_list():
    """
    Get backends

    :return: list
    """
    base_module_list = ["rpm", "nspawn", "docker", "openshift"]
    return base_module_list


def get_module_type():
    """
    Get which module are you actually using.

    :return: str
    """
    amodule = os.environ.get('MODULE')
    readconfig = get_config(fail_without_url=False)
    if amodule is None and readconfig.get("default_module"):
        amodule = readconfig["default_module"]
    if amodule is None and conf.get("default_module"):
        amodule = conf["default_module"]
    if amodule in list_modules_from_config():
        return amodule
    else:
        raise mtfexceptions.ModuleFrameworkException("Unsupported MODULE={0}".format(amodule),
                                       "supported are: %s" % list_modules_from_config())


def get_module_type_base():
    """
    Get which BASE module (parent) are you using

    :return: str
    """
    module_type = get_module_type()
    parent = module_type
    if module_type not in get_backend_list():
        parent = get_config().get("module", {}).get(module_type, {}).get("parent")
        if not parent:
            raise mtfexceptions.ModuleFrameworkException("Module (%s) does not provide parent backend parameter (there are: %s)" %
                                           (module_type, get_backend_list()))
    if parent not in get_backend_list():
        raise mtfexceptions.ModuleFrameworkException("As parent is allowed just base type: %s" % get_backend_list)
    return parent


def get_docker_file(dir_name=conf["docker"]["dockerfiledefaultlocation"]):
    """
    Function returns full path to dockerfile.
    :param dir_name: dir_name, where should be Dockerfile located
    :return: full_path to Dockerfile
    """
    fromenv = os.environ.get("DOCKERFILE")
    if fromenv:
        dockerfile = fromenv
    else:
        dockerfile = os.path.join(dir_name, conf["docker"]["dockerfile"])
    if not os.path.exists(dockerfile):
        core.print_debug("Dockerfile does not exists (you can use DOCKERFILE "
                    "envvar to set to another): %s" % dockerfile)
        dockerfile = None
    return dockerfile

def get_helpmd_file(dir_name=conf["docker"]["dockerfiledefaultlocation"]):
    """
    Function returns full path to HelpMD file.
    :param dir_name: dir_name, where should be helpMD file located
    :return: full_path to Dockerfile
    """
    fromenv = os.environ.get("HELPMDFILE")
    if fromenv:
        helpmdfile = fromenv
    elif os.environ.get("DOCKERFILE"):
        # when DOCKERFILE is placed, search for HelpMD file in same directory
        helpmdfile = os.path.join(os.path.dirname(os.environ.get("DOCKERFILE")), conf["docker"]["helpmdfile"])
    else:
        helpmdfile = os.path.join(dir_name, conf["docker"]["helpmdfile"])
    if not os.path.exists(helpmdfile):
        core.print_debug("Help MD file does not exists (you can use HELPMDFILE "
                    "envvar to set to another): %s" % helpmdfile)
        helpmdfile = None
    return helpmdfile


def getBasePackageSet(modulesDict=None, isModule=True, isContainer=False):
    """
    Get list of base packages (for bootstrapping of various module types)
    It is used internally, you should not use it in case you don't know where to use it.

    :param modulesDict: dictionary of dependent modules
    :param isModule: bool is module
    :param isContainer: bool is contaner?
    :return: list of packages to install
    """
    # nspawn container need to install also systemd to be able to boot
    out = []

    if isModule:
        if isContainer:
            out = conf["packages"]["container"]
        else:

            out = conf["packages"]["common"] + conf["packages"]["basic_modular"]
    else:
        if isContainer:
            out = []
        else:
            out = conf["packages"]["common"] + conf["packages"]["basic"]
    core.print_info("Base packages to install:", out)
    return out


def get_base_compose():
    default_release = "27"
    release = os.environ.get("MTF_FEDORA_RELEASE") or default_release
    if release == "master":
        release = default_release
    compose_url = os.environ.get("MTF_COMPOSE_BASE")
    if not compose_url:
        tmpcompose = conf.get("compose", {}).get("baseurlrepo")
        if tmpcompose:
            compose_url = tmpcompose.format(
                RELEASE=release, ARCH=conf["generic"]["arch"])
    return compose_url
