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
import glob

from elderberrypy.errors import NonExistentUser, NonExistentGroup, RestrictedPath
from elderberrypy.accounts import get_uid, get_gid

log = logging.getLogger('elderberrypy.fs')

__all__ = [
    'check_dir',
    'chown',
    'chmod',
    'copy',
    'PKG_BASE',
    'DevNull',
#    'touch',
]

PKG_BASE = os.path.dirname(__file__)

class DevNull(object):
    """ Throw away everything written to the object """
    def write(data):
        pass


def chown(path, uid, gid, recursive=False):
    """ Chown's the path to the given uid:gid.

    If recursive is True, then all files and directories below `path`
    are chown'd as well.

    If either the uid or gid should remain the same, then specify -1
    """
    os.chown(path, uid, gid)
    if recursive:
        for d, dirs, files in os.walk(path):
            for f in files:
                os.chown(os.path.join(d, f), uid, gid)
                continue
            continue

def chmod(path, mode, recursive=False):
    """ Chmod's the path to the given mode.

    If recursive is True, then all files and directories below `path`
    are chmod'd as well.

    The mode must be specified in octal, or be a bitwise OR of any of the
    stat.S_* values
    """
    try:
        rc = True
        os.chmod(path, mode)
        if recursive:
            for d, dirs, files in os.walk(path):
                for f in files:
                    os.chmod(os.path.join(d, f), mode)
                    continue
                continue
    except:
        rc = False
    return rc


def check_dir(path='', uid=None, gid=None, mode=None, path_env={}):
    """ Verifies the path exists and is set to the given uid:gid and mode

    If the path does not exist, it is created and the given permissions are
    set.  Additionally, it will adjust any permissions that are off.

    The `uid` and `gid` can be the numeric value or the name.  The `mode`
    must be provided in octal
    """
    log.debug('check_dir(path=%s, uid=%s, gid=%s, mode=%s, path_env=%s)' %
              (str(path), str(uid), str(gid), str(mode), str(path_env)))
    success = False
    if not path:
        log.warning("Trying to create an empty path is a NOOP")
        return True
    path = path % path_env
    try:
        if not os.path.isdir(path):
            os.makedirs(path)
        if uid or gid:
            chown(path, get_uid(uid), get_gid(gid))
        if not (mode is None):
            os.chmod(path, mode)
        success = True
    except NonExistentUser, e:
        log.error('Cannot check_path(%s, %s, %s, %o):  The user %s does not '
                  'exist.' % (path, uid, gid, mode, e.uid))
    except NonExistentGroup, e:
        log.error('Cannot check_path(%s, %s, %s, %o):  The group %s does not '
                  'exist.' % (path, uid, gid, mode, e.gid))
    except os.error, e:
        log.error('Cannot check_path(%s, %s, %s, %o):  Err#: %d - Message: %s '
                  '- Filename: %s' % (path, uid, gid, mode, e.errno, e.strerror,
                  getattr(e, 'filename', '')))
    return success


def copy(source=None, dest=None, uid=None, gid=None, mode=None, transform=lambda x,y:y.read(), path_env={}):
    """ Copy source to destination """
    success = True
    if not source:
        log.warning("Trying to copy an empty source is a NOOP")
        return True
    sources = glob.glob(source % path_env)
    num_sources = len(sources)
    dst = dest % path_env
    dst_isdir = os.path.isdir(dst) or dst.endswith(os.path.sep) or (num_sources > 1)
    if sources:
        if dst_isdir:
            try:
                os.makedirs(dst)
            except os.error, e:
                # if the directory already exists, ignore the error.
                # Otherwise, propagate the error up.
                if e.errno != 17:
                    raise e
            pass
        for src in sources:
            if os.path.isfile(src):
                try:
                    if dst_isdir:
                        final_dest = os.path.join(dst, os.path.basename(src))
                    else:
                        final_dest = dst
                    open(final_dest, 'wb').write(transform(path_env, open(src, 'rb')))
                    if uid or gid:
                        chown(final_dest, get_uid(uid), get_gid(gid))
                    if not (mode is None):
                        os.chmod(final_dest, mode)
                except os.error, e:
                    success = False
                    log.error('Cannot copy(%s, %s, %s, %o):  Err#: %d - Message: %s '
                              '- Filename: %s' % (path, uid, gid, mode, e.errno, e.strerror,
                              getattr(e, 'filename', '')))
            else:
                success = False
                log.error("The source does not exist or is not a file: %s" % str(src))
            continue

    return success


RESTRICTED_PATHS = {
    'explicit': [
        '/',
        '/bin',
        '/boot',
        '/home',
        '/lib',
        '/lib64',
        '/lost+found',
        '/media',
        '/mnt',
        '/opt',
        '/root',
        '/sbin',
        '/selinux',
        '/srv',
        '/tmp',
        '/usr',
        '/usr/bin',
        '/usr/local',
        '/usr/local/bin',
        '/var/spool',
        '/var/run',
        '/var/tmp',
    ],
    'tree': [
        '/dev',
        '/sys',
        '/etc',
        '/proc',
    ],
}



def count_files(path):
    """ Return the number of files in a given path.

    Count does not include directories, just files contained within the directories. """
    n = 0
    if os.path.isfile(path):
        n = 1
    else:
        for root, dirs, files in os.walk(path):
            n += len(files)
    return n


#def cleanup_files(opts, path, progress_update=lambda x: x):
#    """ Recusively remove the list of files given."""
#
#    if not isinstance(filelist, list):
#        filelist = [filelist,]
#    errors = 0
#    for f in filelist:
#        status = OKProgress(opts.term, "Removing ElderberryPy environment files for %s" % f)
#        protected = f in RESTRICTED_PATHS['explicit']
#        for base in RESTRICTED_PATHS['tree']:
#            if f.startswith(base):
#                protected = True
#                break
#        if protected:
#            status.update(-1)
#            continue
#        status_len = count_files(f) + 1
#        step_count = 0
#        try:
#            if os.path.isdir(f):
#                if os.path.islink(f):
##                    os.remove(f)
#                    log.debug('cleanup_files: removed %s' % str(f))
#                    step_count += 1
#                else:
#                    for root, dirs, files in os.walk(f):
#                        for name in files:
#                            fpath = os.path.join(root, name)
##                            os.remove(fpath)
#                            log.debug('cleanup_files: removed %s' % fpath)
#                            step_count += 1
#                            status.update(float(step_count)/float(status_len))
#                        continue
##                    os.removedirs(f)
#                    log.debug('cleanup_files: removed %s' % str(f))
#                    step_count += 1
#            if os.path.isfile(f):
##                os.remove(f)
#                log.debug('cleanup_files: removed %s' % str(f))
#                step_count += 1
#            status.update(float(step_count)/float(status_len))
#        except Exception, e:
#            log.debug('cleanup_filess: %s' % str(e))
#            errors += 1
#        if errors:
#            status.update(-1)
#        continue
#    return errors


def cleanup_files(path):
    """ Recusively remove the path given.

    The method yields the number of files removed, after each iteration.
    This assists in being able to use the function with progress bars.

    If the function tries to remove a path in the RESTRICTED_PATHS list, it
    will raise a RestrictedPath exception.

    For example:

    progress = OKProgress(opts.term, "Removing path: /some/path")
    for file_count in cleanup_files('/some/path'):
        progress.update(percent(num_files, file_count))
        continue

    """

    errors = 0
    fullpath = os.path.abspath(f)

    # Verify that we aren't trying to remove a critical system path.
    protected = fullpath in RESTRICTED_PATHS['explicit']
    for base in RESTRICTED_PATHS['tree']:
        if fullpath.startswith(base):
            protected = True
            break
    if protected:
        raise RestrictedPath(fullpath)


    file_count = 0
    try:
        if os.path.isdir(f):
            if os.path.islink(f):
#                    os.remove(f)
                log.debug('cleanup_files: removed %s' % str(f))
                step_count += 1
                yield step_count
            else:
                for root, dirs, files in os.walk(f):
                    for name in files:
                        fpath = os.path.join(root, name)
#                            os.remove(fpath)
                        log.debug('cleanup_files: removed %s' % fpath)
                        step_count += 1
                        yield step_count
                    continue
#                    os.removedirs(f)
                log.debug('cleanup_files: removed %s' % str(f))
                step_count += 1
                yield step_count
        if os.path.isfile(f):
#            os.remove(f)
            log.debug('cleanup_files: removed %s' % str(f))
            step_count += 1
            yield step_count
    except Exception, e:
        log.debug('cleanup_filess: %s' % str(e))
        errors += 1
        raise
    return
