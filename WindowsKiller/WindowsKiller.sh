#!/bin/bash

# This is a part of the external applet Calendar for Cairo-Dock
#
# Copyright : (C) 2009 by Royohboy & Matttbe
#                         Thanks to Nochka85 for his demo
# E-mail : werbungfuerroy@googlemail.com and matttbe@gmail.com
#
#
# This program is free software; you can redistribute it and/or
# modify it under the term -fs of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# http://www.gnu.org/licenses/licenses.html#GPL

## Rev : 09/10/18

DBUS_NAME="org.cairodock.CairoDock"
DBUS_PATH="/org/cairodock/CairoDock"
DBUS_INTERFACE="org.cairodock.CairoDock"
COMMAND=$0
SCRIPT_NAME=`basename $COMMAND`
APP_NAME="`echo $SCRIPT_NAME | cut -f1 -d '.' `"
ACTION=$1
DROP_DATA=$2
MENU_SELECT=$2
SCROLL_UP=$2
APPLET_RP="$HOME/.config/cairo-dock/current_theme/plug-ins/$APP_NAME"
CONF_FILE="$HOME/.config/cairo-dock/current_theme/plug-ins/$APP_NAME/$APP_NAME.conf"


DESCRIPTION="WindowsKiller is able to kill problematic windows easily.
Left Click on its icon and simply select window that cause trouble to kill it.
 (select the dock in order to cancel)
Middle Click will give you some informations like the pid,
 the command to launch this application, the uptime and the class(es) of this window."
AUTHOR="Matttbe"
VERSION="0.0.1"
CATEGORY="2"
APP_FOLDER=$(pwd)

#############################################################################################################
register_the_applet() {
	dbus-send --session --dest=$DBUS_NAME $DBUS_PATH $DBUS_INTERFACE.RegisterNewModule string:"$APP_NAME" string:"$DESCRIPTION" string:"$AUTHOR" string:"$VERSION" int32:$CATEGORY string:"$APP_FOLDER"
	exit
}

#############################################################################################################
get_conf_param() {
	LIGNE=`cat $CONF_FILE | grep "$1"`
	PARAM="`echo $LIGNE | cut -f2 -d '=' `"
}

#############################################################################################################
get_ALL_conf_params() {
	get_conf_param "icon"
	ICON_PATH="$PARAM"
}

#############################################################################################################
action_on_click() {
	dbus-send --session --dest=$DBUS_NAME $DBUS_PATH/$APP_NAME $DBUS_INTERFACE.applet.ShowDialog string:"Select a window in order to kill it.
	Select the dock in order to cancel." int32:5
	xprop > $APPLET_RP/.xprop # we have to export it into a file to keep all lines...
	if [ `cat $APPLET_RP/.xprop | grep -c 'cairo-dock'` -ge 1 ]; then
		dbus-send --session --dest=$DBUS_NAME $DBUS_PATH/$APP_NAME $DBUS_INTERFACE.applet.ShowDialog string:" ** Cancelled ** " int32:2
	else
		kill `cat $APPLET_RP/.xprop | grep ^_NET_WM_PID | cut -d= -f2`
	fi
	rm -f $APPLET_RP/.xprop
	exit
}

#############################################################################################################
action_on_middle_click() {
	dbus-send --session --dest=$DBUS_NAME $DBUS_PATH/$APP_NAME $DBUS_INTERFACE.applet.ShowDialog string:"Select a window in order to show some informations" int32:3
	sleep 0.5 # to not have "xprop: error: Can't grab the mouse"
	xprop > $APPLET_RP/.xprop
	dbus-send --session --dest=$DBUS_NAME $DBUS_PATH/$APP_NAME $DBUS_INTERFACE.applet.ShowDialog string:"$(ps -p `cat $APPLET_RP/.xprop | grep _NET_WM_PID | cut -d= -f2`)
Window name : `cat $APPLET_RP/.xprop | grep ^WM_NAME | cut -d= -f2`
Window class : `cat $APPLET_RP/.xprop | grep ^WM_CLASS | cut -d= -f2`" int32:10
	rm -f $APPLET_RP/.xprop
	exit
}

#############################################################################################################
action_on_init() {
	exit
}

#############################################################################################################
action_on_stop() {
	echo "$APP_NAME applet -> Script Name : $SCRIPT_NAME -> Stop"
	rm -f $APPLET_RP/.xprop
	exit
}

#############################################################################################################
action_on_reload() {
	exit
}


#############################################################################################################
# START ### DO NOT CHANGE THIS SECTION
#############################################################################################################

if [ "`echo $ACTION |grep 'register_the_applet'`" != "" ]; then
	register_the_applet
elif [ "`echo $ACTION |grep 'action_on_click'`" != "" ]; then
	action_on_click
elif [ "`echo $ACTION |grep 'action_on_middle_click'`" != "" ]; then
	action_on_middle_click
elif [ "`echo $ACTION |grep 'action_on_init'`" != "" ]; then
	action_on_init
elif [ "`echo $ACTION |grep 'action_on_stop'`" != "" ]; then
	action_on_stop
elif [ "`echo $ACTION |grep 'action_on_reload'`" != "" ]; then
	action_on_reload
fi

exit

