#!/bin/bash

function compilation () {
        make -j $(grep -c ^processor /proc/cpuinfo) && sudo make install >/dev/null
}

function build () {
        if [ -e build ]; then
                cd build
                make clean
        else
                mkdir build && cd build && cmake .. -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug
        fi
        #echo `pwd`
        compilation
}

function restart () {
	dbus-send --session --dest=org.cairodock.CairoDock /org/cairodock/CairoDock org.cairodock.CairoDock.Quit &&
	cairo-dock -l warning -A &
}

function reload_plugin () {
	dbus-send --session --dest=org.cairodock.CairoDock /org/cairodock/CairoDock org.cairodock.CairoDock.ActivateModule string:"$1" boolean:false;
	dbus-send --session --dest=org.cairodock.CairoDock /org/cairodock/CairoDock org.cairodock.CairoDock.ActivateModule string:"$1" boolean:true;
}

echo "Compile $1"
gksudo -g -m "Root password required for installation" date
case "$1" in
   "core") cd cairo-dock-core;build && restart;;
   "plug-ins") cd cairo-dock-plug-ins && build && restart;;
   *) cd cairo-dock-plug-ins/build/"$1" && make clean && compilation && reload_plugin "$1";;
esac

