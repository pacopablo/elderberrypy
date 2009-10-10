#!/bin/bash

# Available variables:
#  ${LOGDIR}
#  ${LOGFILE}

# Available functions:
#  into
#  outof

# Setuptools crap
DISTRIBUTE_VER=0.6.3
DISTRIBUTE_URL="http://pypi.python.org/packages/source/d/distribute/distribute-${DISTRIBUTE_VER}.tar.gz"

function pkg_install(){
	# Fetch
	wget ${DISTRIBUTE_URL} >> ${LOGFILE} 2>&1
	RVAL=$?;
	if [ $? -ne 0 ]; then
		return $RVAL
	fi

	# unpack
	tar xf distribute-${DISTRIBUTE_VER}.tar.gz >> ${LOGFILE} 2>&1
	RVAL=$?;
	if [ $? -ne 0 ]; then
		return $RVAL
	fi
	into distribute-${DISTRIBUTE_VER}

	# Install	
	python setup.py install >> ${LOGFILE} 2>&1
	outof
}
