#!python

# Copyright (c) 2009 John Hampton <pacopablo@pacopablo.com>
#
# Script to checksum a file and verify said checksum
#
# usage:
#  checksum -m md5.hash -s sha1.hash filename
#
# Exits with a 0 return status if both hashes match.  Otherwise it exits
# with a return status of 1

VERSION='1.0.0'

try:
    import hashlib
    md5 = lambda : hashlib.md5()
    sha = lambda : hashlib.sha1()
except ImportError:
    import md5, sha
    md5 = lambda : md5.new()
    sha = lambda : sha.new()

import pickle
import os
import os.path
import sys
import gzip
from optparse import OptionParser

def load_hashes(hash_path):
    """ Load the hashes from the pickle """

    data = {}
    try:
        data = pickle.load(gzip.open(hash_path, 'r'))
    except IOError, e:
        # Check the exception for presence of gzip error.  If it's a gzip error
        # try loading the pickle without gzip.  Otherwise it means  that it's
        # either not there or we don't have access.  Either way, returning
        # an empty dict is sufficient
        if isinstance(e.args[0], basetring) and (e.errno is None) and \
           (e.strerror is None):
            try:
                data = pickle.load(open(hash_path, 'rb'))
            except IOError:
                pass
            except (pickle.UnpicklingError, AttributeError, EOFError,
                    ImportError, IndexError):
                pass
        pass
    except (pickle.UnpicklingError, AttributeError, EOFError, ImportError, IndexError):
        # OK, What should be behavior be?  If we can't load the pickle, should
        # we bomb and mention the manifest is corrupt?  Or do we simply ignore
        # it and the checksum fails?  In the case of creating a checksum, a
        # fail and ignore would sipmly end up in the file being re-written
        # with the new data
        pass
    return data

def checksum(filename, md5_hashes, sha_hashes, verbose=False):
    s = sha()
    m = md5()
    m.update(file(filename, 'r').read())
    fname = os.path.basename(filename)
    rc = 1
    if (fname in md5_hashes) and md5_hashes[fname] == m.hexdigest():
        s.update(file(filename, 'r').read())
        if (fname in sha_hashes) and sha_hashes[fname] == s.hexdigest():
            rc = 0
    if verbose:
        print("File: %s" % fname)
        print("  MD5 : %s" % m.hexdigest())
        print("  SHA1: %s" % s.hexdigest())
        print("Recipies:")
        print("  MD5 : %s" % (fname in md5_hashes and md5_hashes[fname] or 'Not Found'))
        print("  SHA1: %s" % (fname in sha_hashes and sha_hashes[fname] or 'Not Found'))
        if rc == 0:
            print("FOR THE WIN!")
        else:
            print("FAIL")
    return rc

def create_checksum(filename, directory, md5file, shafile, verbose=False):
    md5_hashes = load_hashes(md5file)
    sha_hashes = load_hashes(shafile)
    if directory:
        abspath = os.path.abspath(directory)
        files = [(f, os.path.join(abspath, f)) for f in os.listdir(abspath) \
                if not f.startswith('.') and \
                   os.path.isfile(os.path.join(abspath, f))]
    else:
        abspath = os.path.abspath(filename)
        files = [(os.path.basename(baspath), abspath)]

    for f, fpath in files:
        if os.path.isfile(fpath) and \
           not f.startswith('.'):
            # Create the MD5 Hash
            m = md5()
            m.update(open(fpath, 'rb').read())
            md5_hashes[f] = m.hexdigest()
            # Create the SHA Hash
            s = sha()
            s.update(open(fpath, 'rb').read())
            sha_hashes[f] = s.hexdigest()
            if verbose:
                print("File: %s" % f)
                print("  MD5 : %s" % md5_hashes[f])
                print("  SHA1: %s" % sha_hashes[f])
        continue
    # Save pickle files
    mfile = gzip.open(md5file, 'wb')
    sfile = gzip.open(shafile, 'wb')
    pickle.dump(md5_hashes, mfile, pickle.HIGHEST_PROTOCOL)
    pickle.dump(sha_hashes, sfile, pickle.HIGHEST_PROTOCOL)
    mfile.close()
    sfile.close()
    return 0


def verify_args(args):
    """ Verify that the files referenced actually exist and stuff """
    args.directory = None
    if args.create:
        try:
            f = open(args.md5, 'a+')
            os.utime(args.md5, None)
            f.close()
            f = open(args.sha, 'a+')
            os.utime(args.sha, None)
            f.close()
        except IOError, err:
            sys.stderr.write("Unable to write to %s.  Please "
                             "verify the file is writable.\n" % err.filename)
            return 1
        if len(args.args) < 1:
            sys.stderr.write("A file or directory to checksum must be "
                             "specified\n")
            return 1
        args.filename = args.args[0]
        if os.path.isdir(args.filename):
            args.directory = args.filename
        elif not os.path.isfile(args.filename):
            sys.stderr.write("A file or directory to checksum must be "
                             "specified\n")
            return 1
    else:
        if not os.path.isfile(args.md5):
            sys.stderr.write("The file containing the MD5 hashes does not exists."
                             "  Please verify the file\nexists and can be read.\n")
            return 1
        if not os.path.isfile(args.sha):
            sys.stderr.write("The file containing the SHA hashes does not exists."
                             "  Please verify the file\nexists and can be read.\n")
            return 1
        if len(args.args) < 1:
            sys.stderr.write("A file to checksum must be specified\n")
            return 1
        args.filename = args.args[0]
        if not os.path.isfile(args.filename):
            sys.stderr.write("The file to checksum does not exists."
                             "  Please verify the file\nexists and can be read.\n")
            return 1

    return 0


def parseargs(argv):
    """ Return a parsed optparse OptionParser object """
    global VERSION
    usage = "usage: %prog [options] file"
    parser = OptionParser(usage=usage, version=VERSION)
    parser.add_option('-m', '--md5', dest='md5',
                    help='File containing the package md5 hashes',
                    metavar='FILE', default='recipies.md5.gz')
    parser.add_option('-s', '--sha', dest='sha',
                    help='File containing the package sha hashes',
                    metavar='FILE', default='recipies.sha.gz')
    parser.add_option('-c', '--create', dest='create', action='store_true',
                    help='Create hash files', default=False)
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
                    help='Produce a verbose output.',  default=False)
    options, args = parser.parse_args(argv)
    options.args = args
    return options


def main(argv):
    args = parseargs(argv)
    rc = verify_args(args)
    if rc == 0:
        if not args.create:
            md5_hashes = load_hashes(args.md5)
            sha_hashes = load_hashes(args.sha)
            rc = checksum(args.filename, md5_hashes, sha_hashes, args.verbose)
        else:
            rc = create_checksum(args.filename, args.directory,
                                 args.md5, args.sha, args.verbose)
    return rc


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
