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

import json
import os
import time
import random
import string
from avocado.utils.process import CmdError
from moduleframework import common
from moduleframework.helpers.container_helper import ContainerHelper
from moduleframework.mtfexceptions import ConfigExc


class OpenShiftHelper(ContainerHelper):
    """
    Basic Helper class for OpenShift container module type

    :avocado: disable
    """

    def __init__(self):
        """
        set basic object variables
        """
        super(OpenShiftHelper, self).__init__()
        self.name = None
        self.icontainer = self.get_url()
        self.template = self.get_template()
        self.pod_id = None
        self._ip_address = None
        if not self.icontainer:
            raise ConfigExc("No container image specified in the configuration file or environment variable.")
        if "docker=" in self.icontainer:
            self.container_name = self.icontainer[7:]
        else:
            # untrusted source
            self.container_name = self.icontainer
        # application name is taken from docker.io/modularitycontainer/memcached
        self.app_name = self.container_name.split('/')[-1]
        self.app_ip = None
        random_str = ''.join(random.choice(string.lowercase) for _ in range(3))
        self.project_name = "{project}-{random_str}".format(project=self.app_name,
                                                            random_str=random_str)
        common.print_debug(self.icontainer, self.app_name)

    def _get_openshift_ip_registry(self):
        """
        Function returns an IP of OpenShift registry.
        Command which is used for getting this info is `oc get svc -n default docker-registry`
        :return: str or None
        """
        openshift_ip_registry = None
        docker_registry = self.runHost('oc get svc -n default %s -o json' % common.OPENSHIFT_DOCKER_REGISTRY,
                                       ignore_status=True).stdout
        try:
            docker_registry = json.loads(docker_registry)
            openshift_ip_registry = docker_registry.get("spec").get("clusterIP")
        except AttributeError:
            pass
        return openshift_ip_registry

    def _change_openshift_account(self, account="system:admin", password=None):
        """
        Function switches to specific account inside OpenShift environment
        :param account: Either user specified account or 'system:admin'
        :param password: Either user specified account
        """
        if password is None:
            s = self.runHost("oc login -u %s" % account, verbose=common.is_not_silent())
        else:
            s = self.runHost("oc login -u %s -p %s" % (account, password), verbose=common.is_not_silent())


    def _register_docker_to_openshift_registry(self):
        """
        Function pushes an OpenShift docker-registry into docker
        Commands which are use are in this order
        * oc whoami -t
        * switch to OpenShift system:admin account
        * gets an IP of OpenShift registry
        * switch to user defined OpenShift user and password.
        * runs docker login with token and IP:5000
        * tag container name
        * push container name into docker
        """
        whoami = self.runHost("oc whoami -t", ignore_status=True, verbose=common.is_not_silent())

        self._change_openshift_account()
        if self.get_docker_pull():
            self.runHost('docker pull %s' % self.container_name)
        openshift_ip_register = self._get_openshift_ip_registry()
        self._change_openshift_account(account=common.get_openshift_user(),
                                password=common.get_openshift_passwd())

        docker_login = self.runHost('docker login -u {user} -p {token} {ip}:5000'.format(
            user=common.get_openshift_user(),
            token=whoami.stdout.strip(),
            ip=openshift_ip_register), ignore_status=True, verbose=common.is_not_silent())
        oc_path = "{ip}:5000/{project}/{name}".format(ip=openshift_ip_register,
                                                      name=self.app_name,
                                                      project=self.project_name)


        self.runHost('docker tag %s %s' % (self.container_name,
                                           oc_path), ignore_status=True)
        self.runHost('docker push %s' % oc_path, ignore_status=True)

    def _app_exists(self):
        """
        It checks if an application already exists in OpenShift environment
        :return: True, application exists
                 False, application does not exist
        """
        oc_status = self.runHost("oc get dc %s -o json" % self.app_name, ignore_status=True)
        if int(oc_status.exit_status) == 0:
            common.print_info("Application already exists.")
            return True
        oc_pods = self._oc_get_output('pods')
        # Check if 'items' in json output is empty or not
        if not oc_pods:
            return False
        # check if 'items', which is not empty, in json output contains app_name
        if not self._check_resource_in_json(oc_pods):
            return False
        return True

    def _check_resource_in_json(self, json_output, resource='svc'):
        """
        Function checks if json_output contains container with specified name


        :param json_output: an output from an OpenShift command
        :param resource: an resource which is checked in an OpenShift environment
        :return: str if the application exists
                 None if the application does not exist
        """
        try:
            if resource in ['svc', 'dc', 'is', 'pod']:
                labels = json_output.get('metadata').get('labels')
                if labels.get('app') == self.app_name:
                    # In metadata dictionary and name is stored pod_name
                    self.pod_id = json_output.get('metadata', {}).get('name')
                    return self.pod_id
            elif resource == common.TEMPLATE:
                if json_output.get('metadata').get('name') == self.app_name:
                    return json_output.get('metadata').get('name')
            elif resource == common.PROJECT:
                for prj in json_output:
                    name = prj.get('metadata').get('name')
                    if self.app_name in name:
                        return name
            else:
                return None
        except (KeyError, AttributeError) as ex:
            return None

    def _convert_string_to_json(self, inp_string):
        """
        It converts a string to json format and returns first item in items.
        :param inp_string: String to format to json
        :return: items from OpenShift output
        """
        try:
            items = json.loads(inp_string)
            return items.get('items')
        except TypeError:
            return None

    def _get_openshift_template(self):
        """
        Function returns template name from OpenShift environment
        :return: dictionary
        """
        template_name = self._oc_get_output('template')
        common.print_debug(template_name)

    def _oc_get_output(self, resource):
        """
        Function returns json output for specific namespace
        :param resource:
        :return: dict ['item'] from JSON output for specific resource
        """
        # Check status of svc/dc/is
        oc_get = self.runHost("oc get %s -o json" % resource, ignore_status=True).stdout
        oc_get = self._convert_string_to_json(oc_get)
        return oc_get

    def _oc_delete(self, resource, name):
        """
        Function removes a resource with given name from OpenShift environment
        :param resource: a name of resource
        :param name: a name in given resource
        :return: return value from oc delete command
        """

        oc_delete = self.runHost("oc delete %s %s" % (resource, name),
                                 ignore_status=True,
                                 verbose=common.is_not_silent())
        return oc_delete.exit_status

    def _remove_apps_from_openshift_resources(self, oc_service="svc"):
        """
        It removes an application from specific "resource" like svc, dc, is.
        :param oc_service: Service from which we would like to remove application
        """
        oc_get = self._oc_get_output(oc_service)
        for item in oc_get:
            # If application exists in svc / dc / is resource, then remove it
            if self._check_resource_in_json(item, resource=oc_service):
                self._oc_delete(oc_service, self.app_name)

    def _app_remove(self):
        """
        Function removes an application from all OpenShift resources like 'svc', 'dc', 'is'
        """
        if self._app_exists():
            # TODO get info from oc status and delete relevant svc/dc/is/pods
            for ns in ['svc', 'dc', 'is', 'pod', common.TEMPLATE, common.PROJECT]:
                self._remove_apps_from_openshift_resources(ns)

    def _create_app(self, template=None):
        """
        It creates an application in OpenShift environment

        :param template: If parameter present, then create an application from template
        :return: Exit status of oc new-app.
        """
        cmd = ["oc", "new-app"]
        if template is None:
            cmd.append(self.container_name)
        else:
            cmd.extend([template, "-p", "APPLICATION_NAME=%s" % self.app_name])
        cmd.extend(["-l", "mtf_testing=true"])
        cmd.extend(["--name", self.app_name])
        common.print_debug(cmd)
        oc_new_app = self.runHost(' '.join(cmd), ignore_status=True)
        time.sleep(1)
        common.print_debug(oc_new_app.stdout)
        return oc_new_app.exit_status

    def _create_app_by_template(self):
        """
        It creates an application in OpenShift environment by OpenShift template
        Steps:
        * oc cluster up
        * oc create -f <template> -n openshift
        * oc new-app memcached -p APPLICATION_NAME=memcached
        :return:
        """
        self._register_docker_to_openshift_registry()
        self.runHost('oc get is')
        oc_template_app = self.runHost('oc process -f "%s"' % self.template, verbose=common.is_not_silent())
        self._change_openshift_account()
        oc_template_create = None
        try:
            oc_template_create = self.runHost('oc create -f %s -n %s' % (self.template,
                                                                         self.project_name),
                                              verbose=common.is_not_silent())
        except CmdError as cme:
            common.print_info('oc create -f failed with traceback %s' % cme.message)
            self.runHost('oc status')
            self._oc_get_output('all')
            return False
        self._change_openshift_account(account=common.get_openshift_user(),
                                       password=common.get_openshift_passwd())
        template_name = self._get_openshift_template()
        time.sleep(1)
        self._create_app(template=template_name)
        self.runHost('oc status')
        return True

    def _create_app_as_s2i(self):
        pass

    def _get_pod_status(self):
        """
        This method checks if the POD is running within OpenShift environment.
        :return: True if POD is running with status "Running"
                 False all other statuses
        """
        pod_initiated = False
        for pod in self._oc_get_output('pod'):
            common.print_debug(self.pod_id)
            if self._check_resource_in_json(pod):
                self._pod_status = pod.get('status').get('phase')
                if self._pod_status == "Running":
                    pod_initiated = True
                    break
        return pod_initiated

    def _verify_pod(self):
        """
        It verifies if an application POD is initiated and ready for testing
        :return: False, application is not initiated during 10 seconds
                 True, application is initiated and ready for testing
        """
        pod_initiated = False
        for x in range(0, common.OPENSHIFT_INIT_WAIT):
            # We need wait a second before pod is really initiated.
            time.sleep(1)
            if self._get_pod_status():
                pod_initiated = True
                break
        return pod_initiated

    def setUp(self):
        """
        It is called by child class and it is same methof as Avocado/Unittest has. It prepares environment
        for OpenShift testing
        * setup environment from config

        :return: None
        """
        self._callSetupFromConfig()
        self._icontainer = self.get_url()

    def _openshift_login(self, oc_ip="127.0.0.1", oc_user='developer', oc_passwd='developer', env=False):
        """
        It logins to an OpenShift environment on specific IP and under user and his password.
        :param oc_ip: an IP where is an OpenShift environment running
        :param oc_user: an username under which we can login to OpenShift environment
        :param oc_passwd: a password for specific username
        :param env: is used for specification OpenShift IP, user and password, otherwise defaults are used
        :return:
        """
        if env:
            oc_ip = common.get_openshift_ip()
            oc_user = common.get_openshift_user()
            oc_passwd = common.get_openshift_passwd()
        oc_output = self.runHost("oc login %s:8443 --username=%s --password=%s" % (oc_ip,
                                                                                   oc_user,
                                                                                   oc_passwd),
                                 verbose=common.is_not_silent())
        return oc_output.exit_status

    def tearDown(self):
        """
        Cleanup environment and call also cleanup from config

        :return: None
        """
        super(OpenShiftHelper, self).tearDown()
        try:
            self._app_remove()
        except Exception as e:
            common.print_info(e, "OpenShift application already removed")
            pass

    def _get_ip_instance(self):
        """
        This method verifies that we can obtain an IP address of the application
        deployed within OpenShift.
        :return: True: getting IP address was successful
                 False: getting IP address was not successful
        """
        service = self._oc_get_output('service')
        try:
            for svc in service:
                if svc.get('metadata').get('labels').get('app') == self.app_name:
                    self.ip_address = svc.get('spec').get("clusterIP")
                    common.trans_dict['GUESTIPADDR'] = self.ip_address
            return True
        except KeyError as e:
            common.print_info(e.message)
            return False
        except IndexError as e:
            common.print_info(e.message)
            return False

    @property
    def ip_address(self):
        """
        Return protocol (IP or IPv6) address on a POD OpenShift instance.

        It returns IP address of POD instance

        :return: str
        """
        return self._ip_address

    @ip_address.setter
    def ip_address(self, value):
        self._ip_address = value

    def start(self, command="/bin/bash"):
        """
        starts the OpenShift application

        :param command: Do not use it directly (It is defined in config.yaml)
        :return: None
        """
        # Clean environment before running tests
        try:
            self._app_remove()
        except Exception as e:
            common.print_info(e, "OpenShift applications were removed")
            pass

        project = self.runHost('oc new-project %s' % self.project_name,
                               ignore_status=True,
                               verbose=common.is_not_silent())
        if self.template is None:
            if not self._app_exists():
            # This part is used for running an application without template or s2i
                self._create_app()
        else:
            common.print_debug(self.template)
            self._change_openshift_account(account=common.get_openshift_user(),
                                           password=common.get_openshift_passwd())
            self._remove_apps_from_openshift_resources(common.TEMPLATE)
            if not self._create_app_by_template():
                return False
        # Verify application is really deploy and prepared for testing.
        if not self._verify_pod():
            return False

        self._get_ip_instance()

    def stop(self):
        """
        This method checks if the application is deployed within OpenShift environment
        and removes service, deployment config and imagestream from OpenShift.

        :return: None
        """
        self._change_openshift_account(account=common.get_openshift_user(),
                                       password=common.get_openshift_passwd())
        self._oc_get_output('all')
        if self._app_exists():
            try:
                self._app_remove()
            except Exception as e:
                common.print_info(e, "OpenShift application already removed")
                pass

    def status(self, command="ls /"):

        """
        Function returns whether the application exists
        and is Running in OpenShift environment

        :param command: Do not use it directly (It is defined in config.yaml)
        :return: bool

        """
        status = False
        if self._app_exists():
            command = self.info.get('start') or command
            return self.runHost('oc exec %s %s' % (self.pod_id, common.sanitize_cmd(command)))

    def run(self, command="ls /", **kwargs):
        """
        Run command inside OpenShift POD, all params what allows avocado are passed inside shell,ignore_status, etc.
        https://docs.openshift.com/container-platform/3.6/dev_guide/executing_remote_commands.html

        :param command: str
        :param kwargs: dict
        :return: avocado.process.run
        """
        ret_val = 0
        cmd_object = self.runHost('oc exec %s %s' % (self.pod_id, common.sanitize_cmd(command)))
        if cmd_object.exit_status != 0:
            ret_val = 1
        return ret_val
