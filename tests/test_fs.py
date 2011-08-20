# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 John Hampton <pacopablo@pacopablo.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: John Hampton <pacopablo@pacopablo.com>

from elderberrypy.fs import remove_path, count_files
from elderberrypy.errors import RestrictedPath

import os
import random
import string
import time

from nose.tools import with_setup, assert_false

BASE_PATH = ''

def setup_files():
    """ Setup a directory tree with files to test ``count_files`` and
    ``remove_path`` methods.

    ``count_files`` only counts the number of files, not any directories.
    Per ``count_files`` this function creates 9 files.
    """
    global BASE_PATH
    tmpdir = "TMPDIR" in os.environ and os.environ['TMPDIR'] or '/tmp'
    BASE_PATH = os.path.join(tmpdir, "ebpy_tests_%s_%s" %
                             (str(os.getpid()), str(time.time())))
    os.mkdir(BASE_PATH)
    dir = os.path.join(BASE_PATH, 'one')
    os.mkdir(dir)
    open(os.path.join(dir, 'foo.txt'), 'w').write("test file\n")
    open(os.path.join(dir, 'bar.txt'), 'w').write("test file\n")
    open(os.path.join(dir, 'baz.txt'), 'w').write("test file\n")
    dir = os.path.join(BASE_PATH, 'one', 'point')
    os.mkdir(dir)
    open(os.path.join(dir, 'bunko.txt'), 'w').write("test file\n")
    dir = os.path.join(BASE_PATH, 'one', 'point', 'five')
    os.mkdir(dir)
    open(os.path.join(dir, 'bucko.txt'), 'w').write("test file\n")
    open(os.path.join(dir, 'craps.txt'), 'w').write("test file\n")
    dir = os.path.join(BASE_PATH, 'two')
    os.mkdir(dir)
    open(os.path.join(dir, 'roulete.txt'), 'w').write("test file\n")
    open(os.path.join(dir, 'poker.txt'), 'w').write("test file\n")
    open(os.path.join(dir, 'face.txt'), 'w').write("test file\n")


def teardown_files():
    """ Make sure that the test isn't leaving junk around in the temp dir.

    WARNING: This method is succeptible to nefarious behavior.  A few checks
    are performed to make sure it doesn't nuke one's system.  However, it does
    call out to ``rm``.  There should be little worry about undesireable
    consequesnces ona normal system.  To be ulta cautious, though, don't run
    the tests as root or any other super-user. """
    global BASE_PATH

    if os.path.isdir(BASE_PATH) and (not os.path.islink(BASE_PATH)):
        if os.path.abspath(BASE_PATH) not in ['/', '/etc', '/bin', '/sbin']:
            os.system('rm -rf "%s"' % BASE_PATH)
            pass


@with_setup(setup_files, teardown_files)
def test_count_files():
    global BASE_PATH
    assert(count_files(BASE_PATH) == 9)

def test_remove_path():
    global BASE_PATH

    for num_files in remove_path(BASE_PATH):
        continue
    assert_false(os.path.exists(BASE_PATH))

