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

# Standard set of file transformations to be used by ElderberryPy scripts

import re
import logging


log = logging.getLogger('elderberrypy.transforms')

__all__ = [
    'set_ebpy_root',
    'set_ebpy_etc',
    'set_ebpy_distutils_root',
    'set_supervisor_init_vals',
    'set_supervisor_config',
    'set_sudoers',
]

SRV_ROOT_RE=re.compile(r'SRV_ROOT=.*')
EBPY_SRV_ROOT_RE=re.compile(r'EBPY_SRV_ROOT=.*')
EBPY_ETC_RE=re.compile(r'EBPY_SRV_ETC=.*')
SUPERVISORCTL_RE=re.compile(r'SUPERVISORCTL=.*')
SUPERVISORD_RE=re.compile(r'SUPERVISORD=.*')
CONFIG_RE=re.compile(r'CONFIG=.*')
SUPERVISOR_CONF_LOGFILE_RE=re.compile(r'logfile=.*')
SUPERVISOR_CONF_CHILDLOGDIR_RE=re.compile(r'childlogdir=.*')
SUPERVISOR_CONF_PIDFILE_RE=re.compile(r'pidfile=.*')


# The transform functions all have the same signature:
#
# def transform(env, data):
#
# The `env` paramater is a dictionary containing string replacements.
# The `env` dictionary can be used to get the ElderberryPy root as well
# as other key directory locations
#
# The data is a file like object from which the data to be transformed can be
# read.
#
# The transform function must return a string object which will be written as
# the transformed file.

def set_ebpy_root(env, data):
    """ Set the EBPY_SRV_ROOT variable.

    Looks for the two strings:
        EBPY_SRV_ROOT=
        SRV_ROOT=
    and replaces them with the ElderberryPy root install path
    """
    out = []
    for l in data.readlines():
        t = SRV_ROOT_RE.sub('SRV_ROOT="%(base)s"' % env, l)
        t = EBPY_SRV_ROOT_RE.sub('EBPY_SRV_ROOT="%(base)s"' % env, t)
        out.append(t)
        continue
    return ''.join(out)


def set_ebpy_etc(env, data):
    """ Set the EBPY_SRV_ETC variable. """
    out = []
    for l in data.readlines():
        t = EBPY_ETC_RE.sub('EBPY_SRV_ETC="%(opt)s/etc"' % env, l)
        out.append(t)
        continue
    return ''.join(out)


def set_ebpy_distutils_root(env, data):
    """ Change the prefix in the `su` pydistutils.cfg """
    return '[install]\nprefix=%(opt)s\n' % env


def set_supervisor_init_vals(env, data):
    """ Change the values needed for supervisord init """
    out = []
    for l in data.readlines():
        t = SUPERVISORCTL_RE.sub('SUPERVISORCTL="%(opt)s/bin/supervisorctl"' % env, l)
        t = SUPERVISORD_RE.sub('SUPERVISORD="%(opt)s/bin/supervisord"' % env, t)
        t = CONFIG_RE.sub('CONFIG="%(opt)s/etc/supervisord.conf"' % env, t)
        out.append(t)
        continue
    return ''.join(out)

def set_supervisor_config(env, data):
    """ Set the ElderberryPy root in the supervisord.conf """
    out = []
    for l in data.readlines():
        t = SUPERVISOR_CONF_LOGFILE_RE.sub('logfile=%(opt)s/log/supervisord/supervisord.log' % env, l)
        t = SUPERVISOR_CONF_CHILDLOGDIR_RE.sub('childlogdir=%(opt)s/log/supervisord/child' % env, t)
        t = SUPERVISOR_CONF_PIDFILE_RE.sub('pidfile=%(opt)s/var/run/supervisord/supervisord.pid' % env, t)
        out.append(t)
        continue
    return ''.join(out)

def set_sudoers(env, data):
    """ Allow the su user access to adserv """
    out = []
    exists = False
    for l in data.readlines():
        exists = (l.find('%srvadmins') >= 0) and (l.find('adserv') >= 0)
        out.append(l)
        continue
    if not exists:
        out.append("%%srvadmins ALL = NOPASSWD: %(opt)s/bin/adserv, SETENV: "
                   "%(opt)s/bin/adserv\n" % env)
    return out and ''.join(out) or ''
