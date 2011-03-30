#!/bin/bash

# Available variables:
#  ${LOGDIR}
#  ${LOGFILE}

# Available functions:
#  into
#  outof

# Git info
IODBC_VER=3.52.7
IODBC_URL=http://www.iodbc.org/downloads/iODBC/libiodbc-${IODBC_VER}.tar.gz

function pkg_install(){
    # Download
    wget ${IODBC_URL} >> ${LOGFILE} 2>&1
    RVAL=$?;
    if [ $? -ne 0 ]; then
        return $RVAL
    fi

    # Unpack
    tar xf libiodbc-${IODBC_VER}.tar.gz >> ${LOGFILE} 2>&1
    RVAL=$?;
    if [ $? -ne 0 ]; then
        return $RVAL
    fi
    into libiodbc-${IODBC_VER}

    # Configure
    ./configure --prefix=${EBPY_SRV_ROOT}/opt --with-iodbc-inidir=${EBPY_SRV_ROOT}/opt/etc >> ${LOGFILE} 2>&1
    RVAL=$?;
    if [ $? -ne 0 ]; then
        return $RVAL
    fi
    
    # Patch Makefile 
#    sed -i  "/755 '\$(DESTDIR_SQ)\$(bindir_SQ)'/d" Makefile >> ${LOGFILE} 2>&1
#    RVAL=$?;
#    if [ $? -ne 0 ]; then
#        return $RVAL
#    fi

    # Make and Make install
    make >> ${LOGFILE} 2>&1
    RVAL=$?;
    if [ $? -ne 0 ]; then
        return $RVAL
    fi
    make install >> ${LOGFILE} 2>&1
}

