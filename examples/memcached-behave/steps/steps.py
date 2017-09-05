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
# Authors: Lukas Zachar <lzachar@redhat.com>
#

from behave import *
import socket


@given(u'connected to module')
def step_impl(context):
    context.backend.start()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', context.backend.config['service']['port']))
    s.settimeout(4)
    context.socket = s


@when(u"send data '{text}'")
def step_impl(context, text):
    context.socket.sendall(text)
    # context.socket.close()


@when(u"send '{query}'")
def step_imp(context, query):
    context.socket.sendall(query.decode('string_escape'))


@then(u"receive '{expected_reply}'")
def step_impl(context, expected_reply):
    data = context.socket.recv(1024)
    expected = expected_reply.decode('string_escape')
    print("got '{0}' expected '{1}'".format(repr(data), repr(expected)))
    assert data == expected


@when(u"run '{text}'")
def step_impl(context, text):
    print(context.backend.docker_id)
    print(context.backend.run(text))
