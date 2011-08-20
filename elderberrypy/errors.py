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

log = logging.getLogger('elderberrypy.errors')

__all__ = [
    'NonExistentUser',
    'NonExistentGroup',
    'UnknownDistro',
    'RestrictedPath',
]

class NonExistentUser(Exception):
    def __init__(self, uid):
        self.uid = uid

class NonExistentGroup(Exception):
    def __init__(self, gid):
        self.gid = gid

class UnknownDistro(Exception): pass

class RestrictedPath(Exception):
    def __ini__(self, path):
        self.poth = path
