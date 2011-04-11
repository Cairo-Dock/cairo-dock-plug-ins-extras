#!/bin/sh

# This is a part of the external applet Calendar for Cairo-Dock
#
# Copyright : (C) 2009 by Matttbe
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

if test "$icon_command" = "" -o "$icon_command" = " "; then
	bash icon.sh
else
	bash "$icon_command"
fi
ARG=$1

# sometime there is a bug with: 10-02
if [ "$ARG" = "" ]; then
	MIN=`date +%M`
	case "$MIN" in
		"01")
			MIN=1
		;;
		"02")
			MIN=2
		;;
		"03")
			MIN=3
		;;
		"04")
			MIN=4
		;;
		"05")
			MIN=5
		;;
		"06")
			MIN=6
		;;
		"07")
			MIN=7
		;;
		"08")
			MIN=8
		;;
		"09")
			MIN=9
		;;
	esac

	SEC=`date +%S`
	case "$SEC" in
		"00")
			SEC=0
		;;
		"01")
			SEC=1
		;;
		"02")
			SEC=2
		;;
		"03")
			SEC=3
		;;
		"04")
			SEC=4
		;;
		"05")
			SEC=5
		;;
		"06")
			SEC=6
		;;
		"07")
			SEC=7
		;;
		"08")
			SEC=8
		;;
		"09")
			SEC=9
		;;
	esac

	ARG=$(((23-`date +%k`)*3600+(59-$MIN)*60+60-$SEC)) # 00:00:01
fi
echo "We wait for $ARG sec."

sleep $ARG
rm .day # force the reload
if test "$icon_command" = "" -o "$icon_command" = " "; then
	bash icon.sh
else
	bash "$icon_command"
fi

# updated 24h later
./update_calendar.sh 86400
