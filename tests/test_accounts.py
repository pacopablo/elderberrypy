# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 John Hampton <pacopablo@pacopablo.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: John Hampton <pacopablo@pacopablo.com>

from elderberrypy.accounts import get_uid, check_uid, get_gid, check_gid
from elderberrypy.errors import NonExistentUser

import random
import string


#    'get_gid',
#    'check_uid',
#    'check_gid',
def test_get_uid():
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

