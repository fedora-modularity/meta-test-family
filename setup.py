#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This tool helps you to rebase package to the latest version
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
# Authors: Petr Hracek <phracek@redhat.com>
#          Tomas Hozza <thozza@redhat.com>

import os
from moduleframework.version import VERSION

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


data_files = {}

paths = ['docs', 'examples', 'tools']

for path in paths:
    for root, dirs, files in os.walk(path):
        data_files[
            os.path.join(
                '/usr/share/moduleframework',
                root)] = [
            os.path.join(
                root,
                f) for f in files]

setup(
    name='modularity-testing-framework',
    version=VERSION,
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
            'generator = moduleframework.generator:main',
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
    ]
)
