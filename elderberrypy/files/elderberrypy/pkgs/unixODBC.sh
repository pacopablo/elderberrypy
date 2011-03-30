#!/bin/bash

# Available variables:
#  ${LOGDIR}
#  ${LOGFILE}

# Available functions:
#  into
#  outof

# Git info
UNIXODBC_VER=2.3.0
UNIXODBC_URL=http://www.unixodbc.org/unixODBC-${UNIXODBC_VER}.tar.gz

function pkg_install(){
    # Download
    wget ${UNIXODBC_URL} >> ${LOGFILE} 2>&1
    RVAL=$?;
    if [ $? -ne 0 ]; then
        return $RVAL
    fi

    # Unpack
    tar xf unixODBC-${UNIXODBC_VER}.tar.gz >> ${LOGFILE} 2>&1
    RVAL=$?;
    if [ $? -ne 0 ]; then
        return $RVAL
    fi
    into unixODBC-${UNIXODBC_VER}

    # Configure
    ./configure --prefix=${EBPY_SRV_ROOT}/opt >> ${LOGFILE} 2>&1
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

