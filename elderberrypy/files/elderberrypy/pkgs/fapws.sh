#!/bin/bash

# Available variables:
#  ${LOGDIR}
#  ${LOGFILE}

# Available functions:
#  into
#  outof

# Setuptools crap
FAPWS_VER=0.9.dev
FAPWS_URL="http://pypi.python.org/packages/source/f/fapws3/fapws3-${FAWPS_VER}.tar.gz"

function pkg_install(){
        # Fetch
        wget ${FAPWS_URL} >> ${LOGFILE} 2>&1
        RVAL=$?;
        if [ $? -ne 0 ]; then
                return $RVAL
        fi

        # unpack
        tar xf fapws3-${FAPWS_VER}.tar.gz >> ${LOGFILE} 2>&1
        RVAL=$?;
        if [ $? -ne 0 ]; then
                return $RVAL
        fi
        into fapws3-${FAPWS_VER}

        # Set pyodbc to build against iodbc
#       sed -i "s:libraries.append('odbc'):libraries.append('iodbc'):" setup.py

        # Build the C extension
        python setup.py build -I "${EBPY_SRV_ROOT}"/opt/include/ -L "${EBPY_SRV_ROOT}"/opt/lib -R "${EBPY_SRV_ROOT}"/opt/lib >> ${LOGFILE} 2>&1
        RVAL=$?;
        if [ $? -ne 0 ]; then
                return $RVAL
        fi
        # Install       
        python setup.py install >> ${LOGFILE} 2>&1
        RVAL=$?;
        if [ $? -ne 0 ]; then
                return $RVAL
        fi
        outof
}

