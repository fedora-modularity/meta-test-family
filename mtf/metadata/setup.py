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


setup(
    name='tmet',
    version="0.0.1",
    description='Test METadata for tests (filter, agregate metadata)',
    keywords='metadata,test',
    author='Jan Scotka',
    author_email='jscotka@redhat.com',
    url='https://None',
    license='GPLv2+',
    packages=find_packages(),
    include_package_data=True,
    data_files=data_files.items(),
    entry_points={
        'console_scripts': [
            'tmet-filter = tmet.filter:main',
            'tmet-agregator = tmet.agregator:main',
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
    install_requires=open('requirements.txt').read().splitlines()
)
