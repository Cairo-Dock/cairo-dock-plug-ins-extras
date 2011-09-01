#!/bin/bash

function build () {
        if [ -e build ]; then
                cd build
                make clean
        else
                mkdir build && cd build && cmake .. -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug
        fi
        make -j $(grep -c ^processor /proc/cpuinfo) && gksudo -g -m "Root password required for installation" make install >/dev/null
}

function restart () {
	dbus-send --session --dest=org.cairodock.CairoDock /org/cairodock/CairoDock org.cairodock.CairoDock.Quit &&
	cairo-dock -l warning -A &
}

#gksudo -g -m "Root password required for installation" date &&
build && 
if [ "$1" = "-r" ]; then restart; fi
