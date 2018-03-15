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


def test_docker_volume_more():
    volume = """VOLUME ["/etc", "/bin", "/var"]"""
    dfl = prepare_linter(volume)
    assert ["/etc", "/bin", "/var"] == dfl.get_docker_volume()
    os.unlink(os.environ.get('DOCKERFILE'))


def test_docker_volume_one_field():
    volume = """VOLUME ["/etc"]"""
    dfl = prepare_linter(volume)
    assert ["/etc"] == dfl.get_docker_volume()
    os.unlink(os.environ.get('DOCKERFILE'))


def test_docker_volume_one_string():
    volume = """VOLUME /etc"""
    dfl = prepare_linter(volume)
    assert ["/etc"] == dfl.get_docker_volume()
    os.unlink(os.environ.get('DOCKERFILE'))


def test_docker_volume_one_string_quote():
    volume = """VOLUME \"/etc\""""
    dfl = prepare_linter(volume)
    assert ["/etc"] == dfl.get_docker_volume()
    os.unlink(os.environ.get('DOCKERFILE'))


def test_docker_volume_one_string_single_quote():
    volume = """VOLUME '/etc'"""
    dfl = prepare_linter(volume)
    assert ["/etc"] == dfl.get_docker_volume()
    os.unlink(os.environ.get('DOCKERFILE'))
