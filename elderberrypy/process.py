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
import logging
from subprocess import call, STDOUT, PIPE, Popen

from elderberrypy.errors import NonExistentUser, NonExistentGroup
from elderberrypy.accounts import get_uid, get_gid

log = logging.getLogger('elderberrypy.process')

__all__ = [
    'run_prog',
]

def run_prog(env, cmd, user='su', group='srvadmins'):
    """ Run the cmd as a subprocess as the given user/group """
    run_env = {
        'PATH' : '%(opt)s/bin:/usr/bin:/bin' % env,
        'EBPY_SRV_ROOT' : '%(base)s' % env,
    }
    method = []
    if isinstance(cmd, basestring):
        method.append(cmd)
    else:
        method.extend(cmd)
    cureuid = os.geteuid()
    curegid = os.getegid()
    # Set new ids
    success = False
    try:
        os.setegid(get_gid(group))
        os.seteuid(get_uid(user))
        p = Popen(method, stdout=PIPE, stderr=STDOUT, env=run_env)
        output = p.communicate()[0]
        rc = p.returncode
        success = rc == 0
        log.debug("run_prog: %s returned %s" % (str(method), str(rc)))
        if not success:
            log.debug("run_prog: %s:\n%s" % (str(method), str(output)))
    except NonExistentUser:
        log.error("Can not run program as non-existent user: %s" % str(user))
    except NonExistentGroup:
        log.error("Can not run program as non-existent group: %s" % str(group))
    except Exception, e:
        log.error("Unable to run program: %s" % str(cmd), exc_info=True)
    # Reset ids
    os.seteuid(cureuid)
    os.setegid(curegid)
    return success
