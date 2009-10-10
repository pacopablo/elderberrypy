# .bashrc


# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

EBPY_SRV_ETC="/srv/opt/etc"
if [ -f "${EBPY_SRV_ETC}/bashrc" ]; then
	. "${EBPY_SRV_ETC}/bashrc"
fi

# User specific aliases and functions
