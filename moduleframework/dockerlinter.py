#!/usr/bin/python

from __future__ import print_function

import os
import re
import ast
from dockerfile_parse import DockerfileParser
import common

# Dockerfile path
DOCKERFILE = "Dockerfile"
EXPOSE = "EXPOSE"
VOLUME = "VOLUME"
LABEL = "LABEL"
ENV = "ENV"
PORTS = "PORTS"
FROM = "FROM"
RUN = "RUN"


def get_string(value):
    return ast.literal_eval(value)

def getDockerFile(dir_name):
    fromenv = os.environ.get("DOCKERFILE")
    if fromenv:
        dockerfile = fromenv
        dir_name = os.path.dirname(dockerfile)
    else:
        dockerfile = os.path.join(dir_name, DOCKERFILE)
    if not os.path.exists(dockerfile):
        dockerfile = None
        common.print_debug("Dockerfile should exists in the %s directory." % dir_name)
    return dockerfile


class DockerfileLinter(object):
    """
    Class checks a Dockerfile
    It requires only directory with Dockerfile.
    """

    dockerfile = None
    oc_template = None
    dfp = {}
    docker_dict = {}

    def __init__(self, dir_name=None):
        dockerfile = getDockerFile(dir_name)
        if dockerfile:
            self.dfp = DockerfileParser(path=os.path.dirname(dockerfile))
            self.dockerfile  = dockerfile
            self._get_structure_as_dict()
        else:
            self.dfp = None
            self.dockerfile = None

    def _get_general(self, value):
        """
        Function returns exposes as field.
        It is used for RUN, EXPOSE and FROM
        :param value:
        :return:
        """
        return value.split()

    def _get_env(self, value):
        """Function gets env as field"""
        return value.split(" ")

    def _get_volume(self, value):
        """Function evaluates a value and returns as string."""
        return get_string(value)

    def _get_label(self, val):
        """
        Function returns label from Docker file
        except INSTALL, UNINSTALL and RUN label used by atomic.
        :param value: row from Dockerfile
        :return: label_dict
        """
        untracked_values = ['INSTALL', 'UNINSTALL', 'RUN']
        if [f for f in untracked_values if val.startswith(f)]:
            return None
        labels = re.sub('\s\s+', ';', val).split(';')
        labels = [l.replace('"', '') for l in labels]
        try:
            label_dict = {l.split(' ')[0]: l.split(' ')[1] for l in labels}
        except IndexError:
            label_dict = {l.split('=')[0]: l.split('=')[1] for l in labels}
        return label_dict

    def _get_structure_as_dict(self):
        functions = {ENV: self._get_env,
                     EXPOSE: self._get_general,
                     VOLUME: self._get_volume,
                     LABEL: self._get_label,
                     FROM: self._get_general,
                     RUN: self._get_general}

        for struct in self.dfp.structure:
            key = struct["instruction"]
            val = struct["value"]
            if key == LABEL:
                if key not in self.docker_dict:
                    self.docker_dict[key] = {}
                value = functions[key](val)
                if value is not None:
                    self.docker_dict[key].update(value)
            else:
                if key not in self.docker_dict:
                    self.docker_dict[key] = []
                try:
                    ret_val = functions[key](val)
                    for v in ret_val:
                        if v not in self.docker_dict[key]:
                            self.docker_dict[key].append(v)
                except KeyError:
                    print("Dockerfile tag %s is not parsed by MTF" % key)

    def get_docker_env(self):
        if ENV in self.docker_dict and self.docker_dict[ENV]:
            return self.docker_dict[ENV]

    def get_docker_specific_env(self, env_name=None):
        """
        Function returns list of specific env_names or empty list
        :param env_name: Specify env_name for check
        :return: List of env or empty list
        """
        if env_name is None:
            return []
        env_list = self.get_docker_env()
        return [env_name in env_list]

    def get_docker_expose(self):
        """
        Function return docker EXPOSE directives
        :return: list of PORTS
        """
        ports_list = []
        if EXPOSE in self.docker_dict and self.docker_dict[EXPOSE]:
            for p in self.docker_dict[EXPOSE]:
                ports_list.append(int(p))
        return ports_list

    def get_docker_labels(self):
        """
        Function returns docker labels
        :return: label dictionary
        """
        if LABEL in self.docker_dict and self.docker_dict[LABEL]:
            return self.docker_dict[LABEL]
        return None

    def get_specific_label(self, label_name=None):
        """
        Function returns list of specific label names or empty list
        :param label_name: Specify label_name for check
        :return: List of labels or empty list.
        """
        if label_name is None:
            return []
        label_list = self.get_docker_labels()
        return [label_name in label_list]

    def check_baseruntime(self):
        """
        Function returns docker labels
        :return: label dictionary
        """
        if FROM in self.docker_dict:
            return [x for x in self.docker_dict[FROM] if "baseruntime/baseruntime" in x]

    def check_microdnf(self):
        """
        Function returns docker labels
        :return: label dictionary
        """
        if RUN in self.docker_dict:
            for val in self.docker_dict[RUN]:
                if val.startswith("yum") or " yum " in val:
                    return False
                if val.startswith("dnf") or " dnf " in val:
                    return False
                else:
                    return True


