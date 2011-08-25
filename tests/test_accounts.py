# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 John Hampton <pacopablo@pacopablo.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: John Hampton <pacopablo@pacopablo.com>

import elderberrypy.accounts
from elderberrypy.errors import NonExistentUser

import random
import string
import pwd
import grp
import logging
log = logging.getLogger('elderberrypy.test.accounts')

from nose.tools import with_setup, assert_false, raises

remove_user = elderberrypy.accounts.remove_user
remove_group = elderberrypy.accounts.remove_group

class MockPopen(object):
    def __init__(self, cmd, stdout=None, stderr=None):
        self.cmd = cmd
        self.returncode = 0

    def communicate(self):
        return ('', '')


class MockPopenUser(MockPopen):
    def communicate(self):
        cmd = self.cmd
        self.returncode = -1
        log.debug("MockPopenUser.communicate: %s" % str(cmd))
        if len(cmd) == 3 and (cmd[0] == 'userdel') and (cmd[1] == '-r'):
            users = set([p.pw_name for p in pwd.getpwall()])
            users.add('su')
            log.debug("su added to users")
            if cmd[2] in users:
                log.debug("su found in users")
                self.returncode = 0
        return ('', '')

class MockPopenGroup(MockPopen):
    def communicate(self):
        cmd = self.cmd
        self.returncode = -1
        if len(cmd) == 2 and (cmd[0] == 'groupdel'):
            groups = set([g.gr_name for g in grp.getgrall()])
            groups.add('su')
            groups.add('ftw')
            groups.add('srvadmins')
            if cmd[1] in groups:
                self.returncode = 0
        return ('', '')


POPEN = None

def mock_popen_remove_user():
    """ Mock out Popen and setup test for remove user """
    global POPEN

    log.debug('mock_popen_remove_user')
    POPEN = elderberrypy.accounts.Popen
    elderberrypy.accounts.Popen = MockPopenUser
    return


def mock_popen_remove_group():
    """ Mock out Popen and setup test for remove user """
    global POPEN

    POPEN = elderberrypy.accounts.Popen
    elderberrypy.accounts.Popen = MockPopenGroup
    return


def restore_popen():
    global POPEN

    elderberrypy.accounts.Popen = POPEN
    return


#    'get_gid',
#    'check_uid',
#    'check_gid',
def test_get_uid():
    get_uid = elderberrypy.accounts.get_uid
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



@with_setup(mock_popen_remove_user, restore_popen)
def test_remove_user():
    assert not remove_user('root')
    assert remove_user('su')
    assert not remove_user('alkjdfl;askjdf;laksj')
    pass


@with_setup(mock_popen_remove_group, restore_popen)
def test_remove_group():
    assert not remove_group('root')
    assert not remove_group('wheel')
    assert remove_group('ftw')
    assert remove_group('su')
    assert remove_group('srvadmins')

    pass

