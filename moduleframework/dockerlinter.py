from __future__ import absolute_import, print_function

import os
import re
import ast

from dockerfile_parse import DockerfileParser

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


class DockerLinter(object):
    """
    Class checks a Dockerfile
    It requires only directory with Dockerfile.
    """

    dockerfile = None
    oc_template = None
    dfp = {}
    docker_dict = {}

    def __init__(self, dir_name=None):
        self.dockerfile = os.path.join(dir_name, DOCKERFILE)
        if not self._exist_docker_file():
            self.dfp = None
        else:
            self.dfp = DockerfileParser(path=dir_name)
            self._get_structure_as_dict()

    def _exist_docker_file(self):
        """
        Function checks if docker file exists
        :return: True if exists
        """
        if not os.path.exists(self.dockerfile):
            print("Dockerfile has to exists in the %s directory." % self.dir)
            return False
        return True

    def _get_expose(self, value):
        """Function returns exposes as field"""
        return value.split()

    def _get_from(self, value):
        """Function returns exposes as field"""
        return value.split()

    def _get_run(self, value):
        """Function returns exposes as field"""
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
                     EXPOSE: self._get_expose,
                     VOLUME: self._get_volume,
                     LABEL: self._get_label,
                     FROM: self._get_from,
                     RUN: self._get_run}

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
                if val.startswith("dnf") or " dnf " in val:
                    return False
                else:
                    return True


