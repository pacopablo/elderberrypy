# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 John Hampton <pacopablo@pacopablo.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: John Hampton <pacopablo@pacopablo.com>

from elderberrypy.fs import remove_path, count-files
from elderberrypy.errors import RetrictedPath

import os
import random
import string


def setup_files():
    tmpdir
#    'get_gid',
#    'check_uid',
#    'check_gid',
@with_setup(setup_files)
def test_count_files():
    assert(get_uid(0) == 0)
    assert(get_uid('root') == 0)
    try:
        rand_uname = "".join([random.choice(string.ascii_letters + string.digits + ".-")
            for i in xrange(21)])

        get_uid(rand_uname)
        # We shouldn't have said random user in the system
        raise AssertionError('NonExistentUser')
    except NonExistentUser:
        # We expect this
        pass

