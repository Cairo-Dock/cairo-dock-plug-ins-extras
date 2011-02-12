#!/bin/bash

# This is a part of the external applet Calendar for Cairo-Dock
#
# Copyright : (C) 2009 by Royohboy & atttbe
#			2011 ported to the bash interface by Fabounet
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
# ERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# http://www.gnu.org/licenses/licenses.html#GPL

## Rev : 2011/02/09

. /usr/share/cairo-dock/plug-ins/Dbus/CDBashApplet.sh $*

#############################################################################################################

on_click()
{
	call ShowDialog "string:\"Select a window in order to kill it.\r
	Select the dock in order to cancel.\"" "int32:5"
	
	p=`xprop`
	if [ `echo "$p" | grep -c 'cairo-dock'` -ge 1 ]; then
		call ShowDialog "string:\" == Cancelled == \"" "int32:2"
	else
		kill `echo "$p" | grep ^_NET_WM_PID | cut -d= -f2`
	fi
	exit
}

on_middle_click()
{
	call ShowDialog "string:\"Select a window in order to show some informations\"" "int32:3"
	sleep 0.5 # to not have "xprop: error: Can't grab the mouse"
	p=`xprop`
	pid=`echo "$p" | grep _NET_WM_PID | cut -d= -f2`
	info=`ps -p $pid | sed "s/CMD/CMD\r/g"`  # we loose the layout later in the 'call' :-/
	
	call ShowDialog "string:\"`echo "${info}"`\r
Window name : "`echo "$p" | grep ^WM_NAME | cut -d= -f2`"\r
Window class : "`echo "$p" | grep ^WM_CLASS | cut -d= -f2`"\"" "int32:10"
	exit
}

#############################################################################################################

run $*

exit 0
