#!/bin/bash

# Available variables:
#  ${LOGDIR}
#  ${LOGFILE}

# Available functions:
#  into
#  outof

# Git info
NGINX_VER=0.8.47
NGINX_URL=http://nginx.org/download/nginx-${NGINX_VER}.tar.gz

function pkg_install(){
    # Download
    wget ${NGINX_URL} >> ${LOGFILE} 2>&1
    RVAL=$?;
    if [ $? -ne 0 ]; then
        return $RVAL
    fi

    # Unpack
    tar xf nginx-${NGINX_VER}.tar.gz >> ${LOGFILE} 2>&1
    RVAL=$?;
    if [ $? -ne 0 ]; then
        return $RVAL
    fi
    into nginx-${NGINX_VER}

    # Configure
    ./configure --prefix=${EBPY_SRV_ROOT}/opt/var \
		--conf-path=${EBPY_SRV_ROOT}/opt/etc/nginx/nginx.conf \
		--error-log-path=${EBPY_SRV_ROOT}/opt/log/nginx/errror.log \
		--http-log-path=${EBPY_SRV_ROOT}/opt/log/nginx/access.log \
		--lock-path=${EBPY_SRV_ROOT}/opt/var/run/nginx/nginx.lock \
		--sbin-path=${EBPY_SRV_ROOT}/opt/bin/nginx \
		--pid-path=${EBPY_SRV_ROOT}/opt/var/run/nginx/nginx.pid \
		--with-http_ssl_module \
		--with-http_realip_module \
		--with-http_gzip_static_module \
		--http-proxy-temp-path=${EBPY_SRV_ROOT}/opt/var/tmp/nginx/proxy_temp \
		--http-fastcgi-temp-path=${EBPY_SRV_ROOT}/opt/var/tmp/nginx/fastcgi_temp \
		--http-uwsgi-temp-path=${EBPY_SRV_ROOT}/opt/var/tmp/nginx/uwsgi_temp \
		--http-client-body-temp-path=${EBPY_SRV_ROOT}/opt/var/tmp/nginx/client_body_temp \
		--http-scgi-temp-path=${EBPY_SRV_ROOT}/opt/var/tmp/nginx/scgi_temp >> ${LOGFILE} 2>&1
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

