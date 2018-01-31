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
        common.print_debug(self.icontainer, self.app_name)

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
        oc_services = self.runHost("oc get pods -o json", ignore_status=True).stdout
        oc_services = self._convert_string_to_json(oc_services)
        # Check if 'items' in json output is empty or not
        if not oc_services:
            return False
        # check if 'items', which is not empty, in json output contains app_name
        if not self._check_app_in_json(oc_services):
            return False
        return True

    def _check_app_in_json(self, item):
        """
        Function checks if json_output contains container with specified name


        :param json_output: json output from an OpenShift command
        :return: True if the application exists
                 False if the application does not exist
        """
        try:
            try:
                labels = item.get('metadata').get('labels')
                if labels.get('app') == self.app_name:
                    # In metadata dictionary and name is stored pod_name
                    self.pod_id = item.get('metadata', {}).get('name')
                    return True
            except AttributeError:
                return False
        except KeyError:
            return False

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

    def _remove_apps_from_openshift_namespaces(self, oc_service="svc"):
        """
        It removes an application from specific "namespace" like svc, dc, is.
        :param oc_service: Service from which we would like to remove application
        """
        # Check status of svc/dc/is
        oc_get = self.runHost("oc get %s -o json" % oc_service, ignore_status=True).stdout
        oc_get = self._convert_string_to_json(oc_get)
        # The output is like
        # dovecot     172.30.1.1:5000/myproject/dovecot     latest    15 minutes ago
        # memcached   172.30.1.1:5000/myproject/memcached   latest    13 minutes ago

        for item in oc_get:
            if self._check_app_in_json(item):
                # If application exists in svc / dc / is namespace, then remove it
                oc_delete = self.runHost("oc delete %s %s" % (oc_service, self.app_name),
                                         ignore_status=True,
                                         verbose=common.is_not_silent())

    def _app_remove(self):
        """
        Function removes an application from all OpenShift namespaces like 'svc', 'dc', 'is'
        """
        if self._app_exists():
            # TODO get info from oc status and delete relevat svc/dc/is
            for ns in ['svc', 'dc', 'is']:
                self._remove_apps_from_openshift_namespaces(ns)

    def _create_app(self):
        """
        It creates an application in OpenShift environment
        """
        # Switching to system user
        oc_new_app = self.runHost("oc new-app -l mtf_testing=true %s --name=%s" % (self.container_name,
                                                                                   self.app_name),
                                  ignore_status=True)
        time.sleep(1)

    def _get_pod_status(self):
        """
        This method checks if the POD is running within OpenShift environment.
        :return: True if POD is running with status "Running"
                 False all other statuses
        """
        pod_initiated = False
        pod_state = self.runHost("oc get pods -o json",
                                 ignore_status=True,
                                 verbose=common.is_not_silent())
        pod_state = self._convert_string_to_json(pod_state.stdout)
        for pod in pod_state:
            common.print_debug(self.pod_id)
            if self._check_app_in_json(pod):
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
        oc_get_service = self.runHost("oc get service -o json")
        service = self._convert_string_to_json(oc_get_service.stdout)
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
        if not self._app_exists():
            self._create_app()
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
        return self.runHost('oc exec %s %s' % (self.pod_id, common.sanitize_cmd(command)))
