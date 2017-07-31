#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2014 Red Hat, Inc.
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
# Authors: Jan Scotka <jscotka@redhat.com>
#          Petr Hracek <phracek@redhat.com>

import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

# copy from https://github.com/avocado-framework/avocado/blob/master/setup.py
VIRTUAL_ENV = hasattr(sys, 'real_prefix')


def get_dir(system_path=None, virtual_path=None):
    """
    Retrieve VIRTUAL_ENV friendly path
    :param system_path: Relative system path
    :param virtual_path: Overrides system_path for virtual_env only
    :return: VIRTUAL_ENV friendly path
    """
    if virtual_path is None:
        virtual_path = system_path
    if VIRTUAL_ENV:
        if virtual_path is None:
            virtual_path = []
        return os.path.join(*virtual_path)
    else:
        if system_path is None:
            system_path = []
    return os.path.join(*(['/'] + system_path))

data_files = {}

paths = ['docs', 'examples', 'tools']

for path in paths:
    for root, dirs, files in os.walk(path, followlinks=True):
        data_files[
            get_dir(
                ['usr', 'share', 'moduleframework', root])] = [
            os.path.join(root, f) for f in files]

setup(
    name='modularity-testing-framework',
    version="0.5.19-dev",
    description='Framework for testing modules and containers.',
    keywords='modules,containers,testing,framework',
    author='Jan Scotka',
    author_email='jscotka@redhat.com',
    url='https://pagure.io/modularity-testing-framework',
    license='GPLv2+',
    packages=find_packages(exclude=['docs', 'examples', 'tools']),
    include_package_data=True,
    data_files=data_files.items(),
    entry_points={
        'console_scripts': [
            'moduleframework-cmd = moduleframework.bashhelper:main',
            'modulelint = moduleframework.modulelint:main',
            'mtf-generator = moduleframework.mtf_generator:main',
        ]
    },
    setup_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    install_requires=['avocado-framework',
                      'netifaces',
                      'behave',
                      'PyYAML',
                      'dockerfile-parse',
                      'pdc_client',
                      'modulemd'
                      ]
)
