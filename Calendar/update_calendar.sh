#!/bin/bash

# This is a part of the external applet Calendar for Cairo-Dock
#
# Copyright : (C) 2009-2012 by Matttbe
# E-mail : matttbe@gmail.com
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# http://www.gnu.org/licenses/licenses.html#GPL


icon_command="$1"
icon_dir="$2"

if test "$icon_command" = "" -o "$icon_command" = " " -o "$icon_command" = "icon_script="; then
	icon_command="icon.sh"
fi

ARG=120
bash "$icon_command" "$icon_dir" 1
date_OLD=`date '+%Y%m%d'`

while [ 1 ]; do
	sleep $ARG
	date_NOW=`date '+%Y%m%d'`
	if [ "$date_NOW" != "$date_OLD" ]; then
		date_OLD=`date '+%Y%m%d'`
		bash "$icon_command" "$icon_dir"
	fi
done

