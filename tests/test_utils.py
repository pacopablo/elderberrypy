# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 John Hampton <pacopablo@pacopablo.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: John Hampton <pacopablo@pacopablo.com>

from elderberrypy.utils import percent

import os
import logging
log = logging.getLogger('elderberrypy.tests.utils')

from nose.tools import with_setup, assert_false, raises

def test_percent():
    assert(percent(1, 1) == 1)
    assert(percent(2, 1) == 0.5)

