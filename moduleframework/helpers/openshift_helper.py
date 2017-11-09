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
from moduleframework.common import CommonFunctions
from moduleframework.mtfexceptions import ContainerExc, ConfigExc


class OpenShiftHelper(CommonFunctions):
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
        self.docker_id = None
        self.icontainer = self.get_url()
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

    def get_container_url(self):
        """
        It returns actual URL link string to container, It is same as URL

        :return: str
        """
        return self.icontainer

    def get_docker_instance_name(self):
        """
        Return docker instance name what will be used inside docker as docker image name
        :return: str
        """
        return self.container_name

    def _app_exists(self):
        """
        It checks if an application already exists in OpenShift environment
        :return: True, application exists
                 False, application does not exist
        """
        oc_status = self.runHost("oc status", ignore_status=True)
        if 'dc/%s' % self.app_name in oc_status.stdout:
            common.print_info("Application already exists.")
            return True
        oc_services = self.runHost("oc get services -o json")
        json_svc = self._convert_string_to_json(oc_services.stdout)
        if not json_svc["items"]:
            return False
        return True

    def _convert_string_to_json(self, string):
        """
        It converts a string to json format
        :param string: String to format to json
        :return: json output
        """
        return json.loads(string)

    def _remove_apps_from_openshift_namespaces(self, oc_service="svc"):
        """
        It removes an application from specific "namespace" like svc, dc, is.
        :param oc_service: Service from which we would like to remove application
        """
        # Check status of svc/dc/is
        oc_get = self.runHost("oc get %s" % oc_service, ignore_status=True).stdout
        # The output is like
        # dovecot     172.30.1.1:5000/myproject/dovecot     latest    15 minutes ago
        # memcached   172.30.1.1:5000/myproject/memcached   latest    13 minutes ago

        app_found = [x for x in oc_get.split('\n') if x.startswith(self.app_name)]
        if app_found:
            # If application exists in svc / dc / is namespace, then remove it
            oc_delete = self.runHost("oc delete %s/%s" % (oc_service, self.app_name), ignore_status=True)

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
        oc_new_app = self.runHost("oc new-app %s --name=%s" % (self.container_name,
                                                               self.app_name),
                                  ignore_status=True)
        common.print_info(oc_new_app.stdout)
        time.sleep(1)

    def _verify_pod(self):
        """
        It verifies if an application POD is initiated and ready for testing
        :return: False, application is not initiated during 10 seconds
                 True, application is initiated and ready for testing
        """
        pod_initiated = False
        for x in range(0, 20):
            pod_state = self.runHost("oc get pods", ignore_status=True)
            pod_state = pod_state.stdout.split('\n')
            for pod in pod_state:
                if pod.startswith(self.app_name):
                    if "Running" in pod and "deploy" not in pod:
                        pod_initiated = True
                        break
            time.sleep(1)
            if pod_initiated:
                break
        return pod_initiated

    def setUp(self):
        """
        It is called by child class and it is same methof as Avocado/Unittest has. It prepares environment
        for docker testing
        * start docker if not
        * pull docker image
        * setup environment from config
        * run and store identification

        :return: None
        """
        self.icontainer = self.get_url()

    def _openshift_login(self, oc_ip="127.0.0.1", oc_user='developer', oc_passwd='developer', env=False):
        """
        It logins to an OpenShift environment on specific IP and under user and his password.
        :param oc_ip: an IP where is an OpenShift environment running
        :param oc_user: an username under which we can login to OpenShift environment
        :param oc_passwd: a password for specific username
        :param env:
        :return:
        """
        if env:
            if 'OPENSHIFT_IP' in os.environ:
                oc_ip = os.environ.get('OPENSHIFT_IP')
            if 'OPENSHIFT_USER' in os.environ:
                oc_user = os.environ.get('OPENSHIFT_USER')
            if 'OPENSHIFT_PASSWORD' in os.environ:
                oc_passwd = os.environ.get('OPENSHIFT_PASSWORD')

        oc_output = self.runHost("oc login %s:8443 --username=%s --password=%s" % (oc_ip,
                                                                                   oc_user,
                                                                                   oc_passwd),
                                 verbose=common.is_not_silent())
        common.print_debug(oc_output.stdout)
        return oc_output.exit_status

    def tearDown(self):
        """
        Cleanup environment and call also cleanup from config

        :return: None
        """
        super(OpenShiftHelper, self).tearDown()
        if common.get_if_do_cleanup():
            # TODO will be implemented later on. I have to find a usecase what to remove
            pass

    def _get_ip_instance(self):
        """
        It gets and IP address of an application from of OpenShift POD.
        :return: True: getting IP address was successful
                 False: getting IP address was not successful
        """
        oc_get_service = self.runHost("oc get service -o json")
        service = self._convert_string_to_json(oc_get_service.stdout)
        try:
            for svc in service["items"]:
                if "clusterIP" in svc.get("spec"):
                    common.trans_dict['GUESTIPADDR'] = svc.get("spec").get("clusterIP")
            return True
        except KeyError as e:
            common.print_info(e.message)
            return False
        except IndexError as e:
            common.print_info(e.message)
            return False

    def start(self):
        """
        starts the OpenShift application

        :param args: Do not use it directly (It is defined in config.yaml)
        :param command: Do not use it directly (It is defined in config.yaml)
        :return: None
        """
        if not self._app_exists():
            self._create_app()
            # Verify application is really deploy and prepared for testing.
            self._verify_pod()
            # TODO fix in case IP is not present. We should failed.
            self._get_ip_instance()

    def stop(self):
        """
        Stops the OpenShift

        :return: None
        """
        if self.status():
            try:
                self._app_remove()
            except Exception as e:
                common.print_info(e, "OpenShift application already removed")
                pass

    def status(self):
        """
        get status of an OpenShift

        :return: bool
        """
        if self._app_exists():
            return True
        else:
            return False

    def run(self, command="ls /", **kwargs):
        """
        Run command inside module, all params what allows avocado are passed inside shell,ignore_status, etc.

        :param command: str
        :param kwargs: dict
        :return: avocado.process.run
        """
        return self.runHost("%s" % common.sanitize_cmd(command), **kwargs)
