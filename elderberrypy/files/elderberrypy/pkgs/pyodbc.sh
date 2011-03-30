#!/bin/bash

# Available variables:
#  ${LOGDIR}
#  ${LOGFILE}

# Available functions:
#  into
#  outof

# Setuptools crap
PYODBC_VER=2.1.7
PYODBC_URL="http://pyodbc.googlecode.com/files/pyodbc-${PYODBC_VER}.zip"

function pkg_install(){
	# Fetch
	wget ${PYODBC_URL} >> ${LOGFILE} 2>&1
	RVAL=$?;
	if [ $? -ne 0 ]; then
		return $RVAL
	fi

	# unpack
	unzip pyodbc-${PYODBC_VER}.zip >> ${LOGFILE} 2>&1
	RVAL=$?;
	if [ $? -ne 0 ]; then
		return $RVAL
	fi
	into pyodbc-${PYODBC_VER}

	# Set pyodbc to build against iodbc
	sed -i "s:libraries.append('odbc'):libraries.append('iodbc'):" setup.py

        # Build the C extension
        python setup.py build_ext -I "${EBPY_SRV_ROOT}"/opt/include/ -L "${EBPY_SRV_ROOT}"/opt/lib -R "${EBPY_SRV_ROOT}"/opt/lib >> ${LOGFILE} 2>&1
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
