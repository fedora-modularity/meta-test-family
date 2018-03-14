# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import print_function

import os
import tempfile

from moduleframework.dockerlinter import DockerfileLinter


def save_docker_file(content):
    temp = tempfile.NamedTemporaryFile(delete=False)
    try:
        temp.write(content)
        temp.seek(0)
    finally:
        temp.close()
    return temp.name


def prepare_linter(content):
    filename = save_docker_file(content)
    os.environ['DOCKERFILE'] = filename
    dfl = DockerfileLinter()
    return dfl


def test_docker_from_etcd():
    Dockerfile_FROM = """FROM registry.fedoraproject.org/f26/etcd"""
    dfl = prepare_linter(Dockerfile_FROM)
    assert dfl.check_from_directive_is_valid()
    os.unlink(os.environ.get('DOCKERFILE'))


def test_docker_from_nginx():
    Dockerfile_FROM = """FROM registry.access.redhat.com/rhscl/nginx-18-rhel7"""
    dfl = prepare_linter(Dockerfile_FROM)
    assert dfl.check_from_directive_is_valid()
    os.unlink(os.environ.get('DOCKERFILE'))


def test_docker_from_dash():
    Dockerfile_FROM = """FROM rhel7:7.5-175"""
    dfl = prepare_linter(Dockerfile_FROM)
    assert dfl.check_from_directive_is_valid()
    os.unlink(os.environ.get('DOCKERFILE'))


def test_docker_from_first():
    Dockerfile_FROM = """FROM rhel7:7.5-175"""
    dfl = prepare_linter(Dockerfile_FROM)
    assert dfl.check_from_is_first()
    os.unlink(os.environ.get('DOCKERFILE'))


def test_docker_from_is_not_first():
    Dockerfile_FROM = """LABEL name=test\nFROM rhel7:7.5-175"""
    dfl = prepare_linter(Dockerfile_FROM)
    assert dfl.check_from_is_first() is False
    os.unlink(os.environ.get('DOCKERFILE'))
