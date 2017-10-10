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
USER = "USER"
COPY = "COPY"
ADD = "ADD"
INSTRUCT = "instruction"

def get_string(value):
    return ast.literal_eval(value)


def get_docker_file(dir_name):
    fromenv = os.environ.get("DOCKERFILE")
    if fromenv:
        dockerfile = fromenv
        dir_name = os.getcwd()
    else:
        dir_name = os.path.abspath(dir_name)
        dockerfile = DOCKERFILE
    dockerfile = os.path.join(dir_name, dockerfile)

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
    dfp_structure = {}
    docker_dict = {}

    def __init__(self, dir_name="../"):
        dockerfile = get_docker_file(dir_name)
        if dockerfile:
            self.dockerfile = dockerfile
            with open(self.dockerfile, "r") as f:
                self.dfp = DockerfileParser(fileobj=f)
                self.dfp_structure = self.dfp.structure
                self._get_structure_as_dict()
        else:
            self.dfp = None
            self.dockerfile = None

    def _get_general(self, value):
        """
        Function returns exposes as field.
        It is used for RUN, EXPOSE, USER, COPY, ADD and FROM
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
                     RUN: self._get_general,
                     USER: self._get_general,
                     COPY: self._get_general,
                     ADD: self._get_general,
                     }

        self.docker_dict[LABEL] = {}
        for label in self.dfp.labels:
            self.docker_dict[LABEL][label] = self.dfp.labels[label]
        for struct in self.dfp.structure:
            key = struct[INSTRUCT]
            val = struct["value"]
            if key != LABEL:
                if key not in self.docker_dict:
                    self.docker_dict[key] = []
                try:
                    ret_val = functions[key](val)
                    for v in ret_val:
                        self.docker_dict[key].append(v)
                except KeyError:
                    print("Dockerfile tag %s is not parsed by MTF" % key)

    def get_docker_env(self):
        return self.docker_dict.get(ENV)

    def get_docker_specific_env(self, env_name=None):
        """
        Function returns list of specific env_names or empty list
        :param env_name: Specify env_name for check
        :return: List of env or empty list
        """
        if env_name is None:
            return []
        env_list = self.get_docker_env()
        return [x for x in env_list if env_name in x]

    def get_docker_expose(self):
        """
        Function return docker EXPOSE directives
        :return: list of PORTS
        """
        ports_list = []
        for p in self.docker_dict.get(EXPOSE, []):
            ports_list.append(int(p))
        return ports_list

    def get_docker_labels(self):
        """
        Function returns docker labels
        :return: label dictionary
        """
        return self.docker_dict.get(LABEL, {})

    def get_specific_label(self, label_name=None):
        """
        Function returns list of specific label names or empty list
        :param label_name: Specify label_name for check
        :return: List of labels or empty list.
        """
        if label_name is None:
            return []
        label_list = self.get_docker_labels()
        return [label_list[key] for key in label_list.keys() if label_name == key]

    def check_from_is_first(self):
        """
        Function checks if FROM directive is really first directive.
        :return: True if FROM is first, False if FROM is not first directive
        """
        if self.dfp_structure[0].get('instruction') == 'FROM':
            return True
        else:
            return False

    def check_from_directive_is_valid(self):
        """
        Function checks if FROM directive contains valid format like is specified here
        http://docs.projectatomic.io/container-best-practices/#_line_rule_section
        Regular expression is: ^[a-z0-9.]+(\/[a-z0-9\D.]+)+$
        Example registry:
            registry.fedoraproject.org/f26/etcd
            registry.fedoraproject.org/f26/flannel
            registry.access.redhat.com/rhscl/nginx-18-rhel7
            registry.access.redhat.com/rhel7/rhel-tools
            registry.access.redhat.com/rhscl/postgresql-95-rhel7

        :return:
        """
        correct_format = False
        struct = self.dfp_structure[0]
        if struct.get(INSTRUCT) == 'FROM':
            p = re.compile("^[a-z0-9.]+(\/[a-z0-9\D.]+)+$")
            if p.search(struct.get('value')) is not None:
                correct_format = True
        return correct_format

    def check_chained_run_command(self):
        """
        Function checks if Dockerfile does not contain more RUN commands in two or more rows.
        BAD examples:
             FROM fedora
             RUN ls /
             RUN cd /
        GOOD example:
             FROM fedora
             RUN ls / && cd /
        :return: True if Dockerfile does not contain RUN instructions in rows
                False if Dockerfile contains more RUN instructions in rows
        """
        value = 0
        for struct in self.dfp_structure:
            if struct.get(INSTRUCT) == RUN:
                value += 1
        if int(value) > 1:
            return False
        return True

    def check_helpmd_is_present(self):
        """
        Function checks if helpmd. is present in COPY or ADD directives
        :return: True if help.md is present
                 False if help.md is not specified in Dockerfile
        """
        helpmd_present = False
        for c in self.docker_dict[COPY]:
            if "help.md" in c:
                helpmd_present = True
        for a in self.docker_dict[ADD]:
            if "help.md" in a:
                helpmd_present = True
        return helpmd_present
