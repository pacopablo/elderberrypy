#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 John Hampton <pacopablo@pacopablo.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: John Hampton <pacopablo@pacopablo.com>
VERSION='1.0.0'

import sys
import os
from optparse import OptionParser

def parse_args(argv):
    """ Parse the command line options and return an OptionParser instance """
    global VERSION
    usage = """
usage: %prog [--major|--minor|--patch]

Bumps the version of the setup.py and prebake scripts.  The portion of the
version number to bump can be controlled through command line switches.
"""[1:]
    parser = OptionParser(usage=usage, version=VERSION)
    parser.add_option('', '--major', dest="major", action="store_true",
                      default=False, help="Bump the major version number")
    parser.add_option('', '--minor', dest="minor", action="store_true",
                      default=False, help="Bump the minor version number")
    parser.add_option('', '--patch', dest="patch", action="store_true",
                      default=False, help="Bump the patch version number")
    options, args = parser.parse_args(argv)
    options.args = args
    return options

def verify_args(args):
    """ Verify the arguments that were parsed """
    rc = 0
    files = os.listdir('.')
    wrong_base_path = False
    args.prebake = 'prebake'
    args.setuppy = 'setup.py'
    if args.prebake in files:
        args.setuppy = '../setup.py'
        if not os.path.isfile(args.setuppy):
            wrong_base_path = True
    elif args.setuppy in files:
        args.prebake = 'scripts/prebake'
        if not os.path.isfile(args.prebake):
            wrong_base_path = True
    if wrong_base_path:
        rc = 1
        print("Can not find the setup.py and/or the prebake scripts. Please run")
        print("from the source root containing setup.py or the scripts directory")
        print("containing prebake.")
    return rc


def bump_version_number(path, bump_major=False, bump_minor=False, bump_patch=True):
    """ Bump the ``VERSION`` number """

    src = open(path, 'r').readlines()
    version_index = -1
    for i, l in enumerate(src):
        if l.strip().startswith('VERSION'):
            major, minor, patch = l.split('=')[-1].strip().strip('"\'').split('.')
            major = int(major)
            minor = int(minor)
            patch = int(patch)
            if bump_major:
                major += 1
            if bump_minor:
                minor += 1
            if bump_patch:
                patch += 1
            version_index = i
        continue
    if version_index >= 0:
        src[version_index] = 'VERSION = "%d.%d.%d"\n' % (major, minor, patch)
        print("Bumped %s to VERSION: %d.%d.%d" % (path, major, minor, patch))
    dest = open(path, 'w').writelines(src)
    return version_index


def main(args):
    """ Do Stuff """
    rc = bump_version_number(args.prebake, args.major, args.minor, args.patch)
    if rc == -1:
        print("Unable to bump version for %s" % args.prebake)
    rc = bump_version_number(args.setuppy, args.major, args.minor, args.patch)
    if rc == -1:
        print("Unable to bump version for %s" % args.setuppy)
    return rc

if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    rc = verify_args(args)
    if rc == 0:
        rc = main(args)
    sys.exit(rc)
