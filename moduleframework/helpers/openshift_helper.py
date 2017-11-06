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
from moduleframework import common
from moduleframework.common import CommonFunctions
from moduleframework.mtfexceptions import ContainerExc, ConfigExc


class OpenShiftHelper(CommonFunctions):
    """
    Basic Helper class for Docker container module type

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
        self.containerInfo = None
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

        common.print_info(self.icontainer)
        common.print_info(self.container_name)
        common.print_info(self.app_name)

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
        common.print_info("OpenShift app_exists")
        oc_status = self.runHost("oc status", ignore_status=True)
        if 'dc/%s' % self.app_name in oc_status.stdout:
            common.print_info("Application already exists.")
            return True
        oc_services = self.runHost("oc get services -o json")
        json_svc = self._convert_string_to_json(oc_services.stdout)
        common.print_info(json_svc["items"])
        if not json_svc["items"]:
            common.print_info("itesms are empty")
            return False
        return True

    def _convert_string_to_json(self, string):
        json_output = json.loads(string)
        common.print_info(json_output)
        return json_output

    def _remove_apps_from_openshift_namespaces(self, oc_service="svc"):
        # Check status of svc/dc/is
        oc_status = self.runHost("oc status %s" % oc_service, ignore_status=True)
        common.print_info(oc_status.stdout)
        # If application exists in svc / dc / is namespace, then remove it
        oc_delete = self.runHost("oc delete %s/%s" % (oc_service, self.app_name), ignore_status=True)
        common.print_info(oc_delete.stdout)

    def _app_remove(self):
        if self._app_exists():
            common.print_info("Application exists")
            # TODO get info from oc status and delete relevat svc/dc/is
            for ns in ['svc', 'dc', 'is']:
                self._remove_apps_from_openshift_namespaces(ns)

    def _create_app(self):
        common.print_info("Create_app in OpenShift")
        # Switching to system user
        #self._openshift_login(oc_user='system', oc_passwd='admin')
        common.print_debug(self.container_name, self.app_name)
        oc_new_app = self.runHost("oc new-app --docker-image=%s --name=%s" % (self.container_name,
                                                                              self.app_name),
                                  ignore_status=True)
        # Switching back to developer user
        #self._openshift_login()
        common.print_info(oc_new_app)

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
        self.containerInfo = self.__load_inspect_json()

    def _openshift_login(self, oc_ip="127.0.0.1", oc_user='developer', oc_passwd='developer', env=False):
        if env:
            if 'OPENSHIFT_IP' in os.environ:
                oc_ip = os.environ.get('OPENSHIFT_IP')
            if 'OPENSHIFT_USER' in os.environ:
                oc_user = os.environ.get('OPENSHIFT_USER')
            if 'OPENSHIFT_PWD' in os.environ:
                oc_passwd = os.environ.get('OPENSHIFT_PWD')

        oc_output = self.runHost("oc login %s:8443 --username=%s --password=%s" % (oc_ip,
                                                                                   oc_user,
                                                                                   oc_passwd),
                                 verbose=common.is_not_silent())
        common.print_debug(oc_output.stderr)
        common.print_debug(oc_output.stdout)
        return oc_output.exit_status

    def tearDown(self):
        """
        Cleanup environment and call also cleanup from config

        :return: None
        """
        super(OpenShiftHelper, self).tearDown()
        if common.get_if_do_cleanup():
            common.print_info("To run a command inside a container execute: ",
                        "docker exec %s /bin/bash" % self.docker_id)

    def __load_inspect_json(self):
        """
        Load json data from docker inspect command

        :return: dict
        """
        return json.loads(
            self.runHost(
                "docker inspect %s" %
                self.container_name, verbose=common.is_not_silent()).stdout)[0]["Config"]

    def _get_ip_instance(self):
        """
        Function return IP address of OpenShift POD.
        :return:
        """
        oc_get_service = self.runHost("oc get service -o json")
        service = self._convert_string_to_json(oc_get_service.stdout)
        try:
            common.print_info(service["items"])
            common.print_info(service["items"][0])
            common.print_info(service["items"][0]["spec"])
            self.app_ip = service["items"][0]["spec"]["clusterIP"]
            common.trans_dict['GUESTIPADDR'] = self.app_ip
            common.print_info(common.trans_dict)
            return True
        except KeyError as e:
            common.print_info(e.message)
            return False

    def start(self):
        """
        start the OpenShift application

        :param args: Do not use it directly (It is defined in config.yaml)
        :param command: Do not use it directly (It is defined in config.yaml)
        :return: None
        """
        common.print_info("OpenShift start")
        if not self._app_exists():
            self._create_app()
            self._get_ip_instance()

    def stop(self):
        """
        Stop the docker container

        :return: None
        """
        if self.status():
            try:
                self._app_remove()
            except Exception as e:
                common.print_debug(e, "OpenShift application already removed")
                pass

    def status(self):
        """
        get status if OpenShift is running

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
