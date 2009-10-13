# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 John Hampton <pacopablo@pacopablo.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: John Hampton <pacopablo@pacopablo.com>

import unittest

from elderberrypy.accounts import get_uid, check_uid, get_gid, check_gid

import random
import string

class UidTest(unittest.TestCase):

#    'get_gid',
#    'check_uid',
#    'check_gid',
    def setup(self):
        self.rand_uname = "".join([random.choice(string.ascii_letters + string.digits + ".-")
            for i in xrange(21)])

    def test_get_uid(self):
        assert(get_uid(0) == 0)
        assert(get_uid('root') == 0)
        try:
            get_uid(self.rand_uname)
        except NonExistentUser:
            raise AssertionError('NonExistentUser')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UidTest, 'test'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')

