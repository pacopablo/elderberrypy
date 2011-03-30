#!/bin/bash

# Available variables:
#  ${LOGDIR}
#  ${LOGFILE}

# Available functions:
#  into
#  outof

# FreeTDS info
FREETDS_VER=0.82
FREETDS_URL=ftp://ftp.ibiblio.org/pub/Linux/ALPHA/freetds/stable/freetds-stable.tgz

function pkg_install(){
    # Download
    wget ${FREETDS_URL} >> ${LOGFILE} 2>&1
    RVAL=$?;
    if [ $? -ne 0 ]; then
        return $RVAL
    fi

    # Unpack
    tar xf freetds-stable.tgz >> ${LOGFILE} 2>&1
    RVAL=$?;
    if [ $? -ne 0 ]; then
        return $RVAL
    fi
    into freetds-${FREETDS_VER}

    # Configure
    # UnixODBC
#    ./configure --prefix=${EBPY_SRV_ROOT}/opt --with-gnu-ld --with-tdsver=8.0 --with-unixodbc=${EBPY_SRV_ROOT}/opt --enable-msdblib >> ${LOGFILE} 2>&1
    # iODBC
    ./configure --prefix=${EBPY_SRV_ROOT}/opt --with-gnu-ld --with-tdsver=8.0 --with-iodbc=${EBPY_SRV_ROOT}/opt --enable-msdblib >> ${LOGFILE} 2>&1
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

