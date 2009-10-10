#!python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 John Hampton <pacopablo@pacopablo.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: John Hampton <pacopablo@pacopablo.com>

import os
import os.path
import pwd
import grp
import logging
from subprocess import call, STDOUT, PIPE, Popen

from elderberrypy.errors import UnknownDistro
from elderberrypy.fs import DevNull

log = logging.getLogger('elderberrypy.distro')

__all__ = [
    'guess_distro',
    'DISTROS',
]

DISTROS = {
    'redhat': {
        'init.d': '/etc/rc.d/init.d/',
        'srvcmd': ['chkconfig', '%(init_script)s', 'on'],
        'detect': os.path.isfile('/etc/redhat-release'),
    },
    'gentoo': {
        'init.d': '/etc/init.d/',
        'conf.d': '/etc/conf.d',
        'srvcmd': ['rc-update', 'add', '%(init_script)s', 'default'],
        'detect': ['which', 'emerge'],
    },
}


def guess_distro():
    """ Attempts to figure out which distro is being used.

    Currently can only differenciate between redhat baseed distros and gentoo.
    If the distro is unknown, then `UnknownDistro` is raised
    """
    global DISTROS

    known = False
    distro = ''
    try:
        for d, v in DISTROS.items():
            method = v.get('detect')
            if isinstance(method, list):
                known = call(method, stdout=open(os.devnull, 'w'), stderr=STDOUT) == 0
            elif callable(method):
                known = method()
            elif isinstance(method, bool):
                known = method
            if known:
                distro = d
                break
            continue
    except:
        log.error("Error while trying to guess distro", exc_info=True)

    if not known:
        raise UnknownDistro
    return distro

