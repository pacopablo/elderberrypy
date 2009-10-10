#!/bin/bash

# Available variables:
#  ${LOGDIR}
#  ${LOGFILE}

# Available functions:
#  into
#  outof

# Setuptools crap
SETUPTOOLS_REV=74552
SETUPTOOLS_PATCH="http://bugs.python.org/setuptools/file55/svn_versioning_4.patch"

function pkg_install(){
    svn export -r${SETUPTOOLS_REV} http://svn.python.org/projects/sandbox/trunk/setuptools >> ${LOGFILE} 2>&1
    RVAL=$?;
    if [ $? -ne 0 ]; then
        return $RVAL
    fi
    wget ${SETUPTOOLS_PATCH} -O svn_1.6.patch >> ${LOGFILE} 2>&1
    RVAL=$?;
    if [ $? -ne 0 ]; then
        return $RVAL
    fi
    into setuptools
    patch -p0  >> ${LOGFILE} 2>&1 < svn_1.6.patch
    RVAL=$?;
    if [ $? -ne 0 ]; then
        return $RVAL
    fi
    python setup.py install >> ${LOGFILE} 2>&1
}

