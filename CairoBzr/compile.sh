#!/bin/sh
MODULE="CairoBzr"

valac --pkg CDApplet -o $MODULE $MODULE.vala &&

#if [ $@ > 0 ] && [ "$1" = "-r" ]; then
if [ "$1" = "-r" ]; then
	dbus-send --session --dest=org.cairodock.CairoDock /org/cairodock/CairoDock org.cairodock.CairoDock.ActivateModule string:$MODULE boolean:false;
	dbus-send --session --dest=org.cairodock.CairoDock /org/cairodock/CairoDock org.cairodock.CairoDock.ActivateModule string:$MODULE boolean:true;
fi

# Compile it with (you may have to install valac) :
# valac --pkg CDApplet -o demo_vala demo_vala.vala
# or
# valac -q -C --disable-warnings --pkg CDApplet demo_vala.vala
# gcc -o demo_vala $(pkg-config --cflags --libs CDApplet) demo_vala.c

