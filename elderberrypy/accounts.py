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

import pwd
import grp
import logging
from subprocess import Popen, PIPE, STDOUT

from elderberrypy.errors import NonExistentUser, NonExistentGroup

log = logging.getLogger('elderberrypy.accounts')

__all__ = [
    'create_group',
    'create_user',
    'get_uid',
    'get_gid',
    'check_uid',
    'check_gid',
]

RESTRICTED_USERS = [
    'root',
    'bin',
    'daemon',
    'adm',
    'lp',
    'sync',
    'shutdown',
    'halt',
    'mail',
    'uucp',
    'operator',
    'games',
    'gopher',
    'ftp',
    'nobody',
    'dbus',
    'vcsa',
    'saslauth',
    'postfix',
    'haldaemon',
    'sshd',
]

RESTRICTED_GROUPS = [
    'root',
    'bin',
    'daemon',
    'sys',
    'adm',
    'tty',
    'disk',
    'lp',
    'mem',
    'kmem',
    'wheel',
    'mail',
    'uucp',
    'man',
    'games',
    'gopher',
    'video',
    'dip',
    'ftp',
    'lock',
    'audio',
    'nobody',
    'users',
    'dbus',
    'utmp',
    'utempter',
    'floppy',
    'vcsa',
    'cdrom',
    'tape',
    'dialout',
    'saslauth',
    'postdrop',
    'postfix',
    'haldaemon',
    'sshd',
    'screen',
    'stapdev',
    'stapusr',
    'stap-server',
    'tcpdump',
    'slocate',
]




def get_uid(uid):
    """ Returns the UID number of the given user.

    If the `uid` is an int, the `uid` is verified against the password
    database.  If it is a string the uid is looked up in the password database.
    If None is passed in, then -1 is returned.  This can be used by os.chown
    to indicate no change in the uid.  If the uid is not found in the password
    database, or is not a string or int, then a NonExistentUser exception
    is raised
    """
    try:
        if isinstance(uid, basestring):
            uid = pwd.getpwnam(uid)[2]
        elif isinstance(uid, int):
            uid = pwd.getpwuid(uid)[2]
        elif uid is None:
            uid = -1
        else:
            raise NonExistentUser(uid)
    except KeyError:
        raise NonExistentUser(uid)
    return uid


def get_gid(gid):
    """ Returns the GID number of the given group.

    If the `gid` is an int, the `gid` is verified against the group
    database.  If it is a string the gid is looked up in the group database.
    If None is passed in, then -1 is returned.  This can be used by os.chown
    to indicate no change in the gid.  If the gid is not found in the group
    database, or is not a string or int, then a NonExistentGroup exception
    is raised
    """
    try:
        if isinstance(gid, basestring):
            gid = grp.getgrnam(gid)[2]
        elif isinstance(uid, int):
            gid = grp.getgrgid(gid)[2]
        elif gid is None:
            gid = -1
        else:
            log.debug('GID parameter unknown type: %s - Value: %s' %
                      (str(type(gid)), str(gid)))
            raise NonExistentGroup(gid)
    except KeyError:
        raise NonExistentGroup(gid)
    return gid

def check_gid(gid):
    """ Returns whether or not the gid specified exists.

    The gid may be an int or string.
    """
    valid = True
    try:
        get_gid(gid)
    except NonExistentGroup:
        valid = False
    return valid

def check_uid(uid):
    """ Returns whether or not the uid specified exists.

    The uid may be an int or string.
    """
    valid = True
    try:
        get_uid(uid)
    except NonExistentUser:
        valid = False
    return valid

def create_user(username, home=None, groups=None, gecos=None, skel=None,
                shell='/bin/bash', create_home=True):
    """ Create a user account """
    if check_uid(username):
        log.warning('Trying to create a duplicate user: %s' % username)
        return True
    cmd = ['useradd']
    if home:
        cmd.append('-d')
        cmd.append(str(home))
    if create_home:
        cmd.append('-m')
    if gecos:
        cmd.append('-c')
        cmd.append('"%s"' % gecos)
    if groups:
        if isinstance(groups, list):
            primary_grp = groups[0]
            cmd.append('-g')
            cmd.append(str(get_gid(primary_grp)))
            cmd.append('-G')
            cmd.append(','.join(groups))
        if isinstance(groups, basestring):
            cmd.append('-g')
            cmd.append(get_gid(groups))
            cmd.append('-G')
            cmd.append(str(groups))
    if skel:
        cmd.append('-k')
        cmd.append(str(skel))
    cmd.append('-s')
    cmd.append(str(shell))
    cmd.append(str(username))

    p = Popen(cmd, stdout=PIPE, stderr=STDOUT)
    output = p.communicate()[0]
    rc = p.returncode
    if rc == 0:
        a = Popen(['usermod', '-U', username], stdout=PIPE, stderr=STDOUT)
        ouput = a.communicate()[0]
        rc = a.returncode
    return rc == 0


def create_group(groupname):
    """ Create a group """
    if check_gid(groupname):
        log.warning('Trying to create a duplicate group: %s' % groupname)
        return True
    cmd = ['groupadd', groupname]
    p = Popen(cmd, stdout=PIPE, stderr=STDOUT)
    output = p.communicate()[0]
    rc = p.returncode
    return rc == 0


def remove_user(user):
    """ Remove the given user from the system. """
    rc = 1
    if not (user in RESTRICTED_USERS):
        cmd = ['userdel', '-r',  user]
        p = Popen(cmd, stdout=PIPE, stderr=STDOUT)
        output = p.communicate()[0]
        rc = p.returncode
    return rc == 0


def remove_group(group):
    """ Remove the given group from the system. """
    rc = 1
    if not (group in RESTRICTED_GROUPS):
        cmd = ['groupdel', group]
        p = Popen(cmd, stdout=PIPE, stderr=STDOUT)
        output = p.communicate()[0]
        rc = p.returncode
    return rc == 0
