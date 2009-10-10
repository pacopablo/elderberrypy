#!/bin/bash

# Available variables:
#  ${LOGDIR}
#  ${LOGFILE}

# Available functions:
#  into
#  outof

# Git info
GIT_VER=1.6.4.2
GIT_URL=http://kernel.org/pub/software/scm/git/git-${GIT_VER}.tar.gz

function pkg_install(){
    # Download
    wget ${GIT_URL} >> ${LOGFILE} 2>&1
    RVAL=$?;
    if [ $? -ne 0 ]; then
        return $RVAL
    fi

    # Unpack
    tar xf git-${GIT_VER}.tar.gz >> ${LOGFILE} 2>&1
    RVAL=$?;
    if [ $? -ne 0 ]; then
        return $RVAL
    fi
    into git-${GIT_VER}

    # Configure
    ./configure --prefix=${EBPY_SRV_ROOT}/opt --without-tcltk >> ${LOGFILE} 2>&1
    RVAL=$?;
    if [ $? -ne 0 ]; then
        return $RVAL
    fi
    
    # Patch Makefile 
    sed -i  "/755 '\$(DESTDIR_SQ)\$(bindir_SQ)'/d" Makefile >> ${LOGFILE} 2>&1
    RVAL=$?;
    if [ $? -ne 0 ]; then
        return $RVAL
    fi

    # Make and Make install
    make >> ${LOGFILE} 2>&1
    RVAL=$?;
    if [ $? -ne 0 ]; then
        return $RVAL
    fi
    make install >> ${LOGFILE} 2>&1
}

