#!/bin/bash

# Copyright (c) 2009, John Hampton <pacopablo.com>

# libcurl info
LIBCURL_VER=7.19.0
LIBCURL_URL=http://pycurl.sourceforge.net/download/pycurl-${LIBCURL_VER}.tar.gz

function pkg_install(){
    # Download
    wget ${LIBCURL_URL} >> ${LOGFILE} 2>&1
    RVAL=$?;
    if [ $? -ne 0 ]; then
        return $RVAL
    fi

    # Unpack
    tar xf git-${LIBCURL_VER}.tar.gz >> ${LOGFILE} 2>&1
    RVAL=$?;
    if [ $? -ne 0 ]; then
        return $RVAL
    fi
    into git-${LIBCURL_VER}

    # Configure
    ./configure --prefix=${EBPY_SRV_ROOT}/opt --with-ssl >> ${LOGFILE} 2>&1
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

