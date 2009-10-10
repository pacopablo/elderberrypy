#!/bin/bash

# Copyright (C) 2009 John Hampton <pacopablo@pacopablo.com>
#
# Script for installing a "service" pytho install 

SRV_PREFIX="${EBPY_SRV_ROOT}/opt"

function pkg_install(){
    VERSION="${1}"
    if [ -z "${1}" ]; then
        VERSION="2.6.2"
    fi
    PY_VERSION="Python-${VERSION}"
    PY_TARBALL="${PY_VERSION}.tar.bz2"
    PYTHON="http://python.org/ftp/python/2.6.3/${PY_TARBALL}"
    guess_distro
    case ${DISTRO} in
        gentoo)
            PREREQ_PKGS="sys-libs/readline dev-libs/openssl dev-libs/libxslt dev-libs/libxml2 dev-db/sqlite-3 app-arch/bzip2 sys-libs/ncurses sys-libs/gdbm sys-libs/db-4"
            PKG_INSTALL="emerge -av"
            ;;
        redhat)
            PREREQ_PKGS="gcc readline-devel openssl-devel libxslt-devel libxml2-devel sqlite-devel ncurses-devel bzip2-devel gdbm-devel db4-devel"
            PKG_INSTALL="yum install -y"
            ;;
    esac
    # Check pre-requisite libraries
    for pkg in ${PREREQ_PKGS}; do
        check_package ${pkg}
    done
    if [ ! -z "${MISSING_PKGS}" ]; then
        cat << EOF

        Some of the pre-requisite packages are not installed.  
        Please run the following as root:

          ${PKG_INSTALL} ${MISSING_PKGS}

EOF
        exit 1
    fi

    # fetch Pyton source
    message "Fetching Python (${VERSION})"
    wget "${PYTHON}" >> "${LOGFILE}" 2>&1; ok fail;
    message "Unpacking Python";
    tar xf "${PY_TARBALL}" >> "${LOGFILE}" 2>&1; ok fail;
    message "Configuring Python";
    into "${PY_VERSION}";
    ./configure --prefix=${SRV_PREFIX} >> "${LOGFILE}" 2>&1; ok fail;
    message "Building Python";
    make >> "${LOGFILE}" 2>&1 || die "Unable to build Python.  Please check the log ${LOGFILE}"
    make altinstall >> "${LOGFILE}" 2>&1; ok fail;
    outof
}

function pkg_start(){
    VAR=NOOP
}

function pkg_done(){
    VAR=NOOP
}
