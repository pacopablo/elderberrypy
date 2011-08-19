#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 John Hampton <pacopablo@pacopablo.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: John Hampton <pacopablo@pacopablo.com>

import glob
import os
import sys
from setuptools import setup, find_packages

VERSION = "0.1.13"

data_files=[
    ('share/docs/elderberrypy', glob.glob('COPYING*')),
    ('share/docs/elderberrypy', glob.glob('docs/*')),
]

package_data=[
    'files/bin/*',
    'files/etc/bashrc',
    'files/etc/supervisord.conf',
    'files/etc/nginx/*.conf',
    'files/etc/nginx/vhosts.d/.keep',
    'files/etc/skel/.bash_logout',
    'files/etc/skel/.bash_profile',
    'files/etc/skel/.bashrc',
    'files/etc/skel/.gitconfig',
    'files/etc/skel/.pydistutils.cfg',
    'files/etc/skel/.pystartup',
    'files/etc/skel/.vimrc',
    'files/etc/skel/.profile.d/*',
    'files/etc/skel/.ssh/authorized_keys',
    'files/etc/skel/.egg_cache/.keep',
    'files/etc/skel/.vim/ftplugin/*',
    'files/etc/skel/etc/*',
    'files/etc/ssl/.keep',
    'files/etc/ssl/private/.keep',
    'files/elderberrypy/bash/*',
    'files/elderberrypy/pkgs/*',
    'files/redhat/init.d/*',
    'files/gentoo/conf.d/*',
    'files/gentoo/init.d/*',
]

scripts = [
    'scripts/prebake',
]

setup(
    name='elderberrypy',
    version=VERSION,
    author='John Hampton',
    author_email='pacopablo@pacopablo.com',
    description='Python service installation and execution layout',
    url='http://elderberrypy.org',
    packages=['elderberrypy'],
    package_data={'elderberrypy': package_data,},
    scripts=scripts,
    long_description="""
ElderberryPy creates a Python "service" environment and installs tools to
manage the installation, configuration, and execution of Python services.
"""[1:],
    download_url="http://elderberrypy.org/downloads/",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Systems Administration',
        'Topic :: System :: Installation/Setup',
    ],
    test_suite='elderberrypy.tests.suite',
    data_files=data_files,
)

