#!/bin/bash

# Copyright (C) 2009 John Hampton <pacopablo@pacopablo.com>

# Bake recipe for installing supervisor

function pkg_install(){
    easy_install supervisor >> ${LOGFILE} 2>&1
}
