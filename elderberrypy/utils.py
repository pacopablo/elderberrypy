#!python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 John Hampton <pacopablo@pacopablo.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: John Hampton <pacopablo@pacopablo.com>
import logging

log = logging.getLogger('elderberrypy.utils')

__all__ = [
    'percent',
    'PKG_BASE',
]

PKG_BASE = os.path.dirname(__file__)

def percent(total, count):
    """ Returns the percent done represented as a float """

    return float(count) / float(total)
