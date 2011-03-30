#!/bin/bash

# Copyright (c) 2011, John Hampton <pacopablo.com>

# libcurl info
LIBEV_VER=4.04
LIBEV_URL=http://dist.schmorp.de/libev/libev-${LIBEV_VER}.tar.gz

function pkg_install(){
    # Download
    wget ${LIBEV_URL} >> ${LOGFILE} 2>&1
    RVAL=$?;
    if [ $? -ne 0 ]; then
        return $RVAL
    fi

    # Unpack
    tar xf libev-${LIBEV_VER}.tar.gz >> ${LOGFILE} 2>&1
    RVAL=$?;
    if [ $? -ne 0 ]; then
        return $RVAL
    fi
    into libev-${LIBEV_VER}

    # Configure
    ./configure --prefix=${EBPY_SRV_ROOT}/opt >> ${LOGFILE} 2>&1
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
