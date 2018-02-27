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

from setuptools import setup, find_packages

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

paths = ['man']

for path in paths:
    for root, dirs, files in os.walk(path, followlinks=True):
        data_files[
            get_dir(
                ['usr', 'share', 'man', 'man1'])] = [
            os.path.join(root, f) for f in files]

setup(
    name='meta-test-family',
    version="0.8.1",
    description='Tool to test components for a modular Fedora.',
    keywords='modules,containers,testing,framework',
    author='Jan Scotka',
    author_email='jscotka@redhat.com',
    url='https://github.com/fedora-modularity/meta-test-family',
    license='GPLv2+',
    packages=find_packages(exclude=['docs', 'examples', 'tools']),
    include_package_data=True,
    data_files=data_files.items(),
    scripts=[],
    entry_points={
        'console_scripts': [
            'mtf-cmd = moduleframework.bashhelper:main',
            'mtf-generator = moduleframework.mtf_generator:main',
            'mtf-env-set = moduleframework.mtf_environment:mtfenvset',
            'mtf-env-clean = moduleframework.mtf_environment:mtfenvclean',
            'mtf-init = moduleframework.mtf_init:main',
            'mtf = moduleframework.mtf_scheduler:main',
            'mtf-pdc-module-info-reader = moduleframework.pdc_msg_module_info_reader:main',
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
    install_requires=open('requirements.txt').read().splitlines(),
    zip_safe=True
)
