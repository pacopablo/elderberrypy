#!/bin/bash

# Copyright (C) 2009 John Hampton <pacopablo@pacopablo.com>
#
# ElderberryPy Global Bash Functions
trap 'echo; exit 1' INT

blue='\E[01;34m'
red='\E[01;31m'
green='\E[01;32m'
white='\E[01;37m'
endcolor='\E[0m'

function position_cursor() {
    COLS=$((${_WINDOW_X} - 10))
    tput cuf ${COLS}
#    tput cuu1
}

function message() {
    tput sc
    echo -n "           ${1}"
    tput rc
}

function ok() {
#    position_cursor
    RETVAL=${?}
    if [ ${RETVAL} -eq 0 ]; then
        echo -e "${blue}[ ${green}OK${blue} ]${endcolor}"
    else
        echo -e "${blue}[ ${red}FAILED${blue} ]${endcolor}";
        if [ ! -z ${1} ]; then
            if [ ${1} == "fail" ]; then
                die "Unable to continue.  Please check the log ${LOGFILE}"
            fi
        fi
    fi
}

function die(){
    echo "${1}"
    exit 1
}

function into(){
    if [ -z ${1} ]; then
        pushd . > /dev/null 2>&1;
    else
        pushd ${1} > /dev/null 2>&1;
    fi
}

function outof(){
    popd > /dev/null 2>&1;
}


function die(){
    echo "${1}"
    exit 1
}

function into(){
    if [ -z ${1} ]; then
        pushd . > /dev/null 2>&1;
    else
        pushd ${1} > /dev/null 2>&1;
    fi
}

function outof(){
    popd > /dev/null 2>&1;
}

function guess_distro(){
    DISTRO='unknown'
    which emerge > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        DISTRO='gentoo'
    else
        ls /etc/redhat-release > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            DISTRO="redhat"
        fi
    fi

}

MISSING_PKGS=""
function check_package(){
    guess_distro
	PKGNAME="${1}"
	if [ -z "${PKGNAME}" ]; then
		"A package must be specified"
		exit 1
	fi
	message "Checking for ${PKGNAME}"
    case ${DISTRO} in
        gentoo)
            check_gentoo_pkg "${PKGNAME}"; ok
            ;;
        redhat)
            check_redhat_pkg "${PKGNAME}"; ok
            ;;
        *)
            ;;
    esac
	if [ ${RETVAL} -eq 1 ]; then
		MISSING_PKGS="${MISSING_PKGS} ${PKGNAME}"
	fi
}

function check_redhat_pkg(){
    PKGNAME="${1}"
	rpm -q ${PKGNAME} | grep -v 'not installed' > /dev/null 2>&1
}

function check_gentoo_pkg(){
    PKGNAME="${1}"
    equery -C -N l ${PKGNAME} | grep I > /dev/null 2>&1
}

function set_colors(){
    COLORS=/etc/DIR_COLORS
    [ -e "/etc/DIR_COLORS.$TERM" ] && COLORS="/etc/DIR_COLORS.$TERM"
    [ -e "$HOME/.dircolors" ] && COLORS="$HOME/.dircolors"
    [ -e "$HOME/.dir_colors" ] && COLORS="$HOME/.dir_colors"
    [ -e "$HOME/.dircolors.$TERM" ] && COLORS="$HOME/.dircolors.$TERM"
    [ -e "$HOME/.dir_colors.$TERM" ] && COLORS="$HOME/.dir_colors.$TERM"
    [ -e "$COLORS" ] || return
}

function rval(){
    return ${1}
}
