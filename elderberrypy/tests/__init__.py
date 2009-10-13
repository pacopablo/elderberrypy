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

def suite():
    suite = unittest.TestSuite()
    try:
        import elderberrypy.tests.accounts
        suite.addTest(elderberrypy.tests.accounts.suite())
    except ImportError:
        print("\nSKIPPING - ElderberryPy Account Test Suite\n")
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
