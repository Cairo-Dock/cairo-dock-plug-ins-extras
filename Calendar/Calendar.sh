#!/bin/bash

# This is a part of the external applet Calendar for Cairo-Dock
#
# Copyright : (C) 2009 by Royohboy & Matttbe
#                 2009-2012 by Matttbe
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

## Rev : 21/01/2010

. /usr/share/cairo-dock/plug-ins/Dbus/CDBashApplet.sh $*

COMMAND=$0
SCRIPT_NAME=`basename $COMMAND`
DROP_DATA=$1

#############################################################################################################
get_ALL_conf_params() {

calendar_command=`get_conf_param "calendar_command"`

import_command=`get_conf_param "import_command"`

icon_command=`get_conf_param "icon_script"`

time_dialog_cal=`get_conf_param "time_dialog_cal_today"`

time_dialog_ev=`get_conf_param "time_dialog_ev"`

time_dialog_cal_next=`get_conf_param "time_dialog_cal_next"`

}

#############################################################################################################
on_click() {

time_dialog_cal_today=`get_conf_param "time_dialog_cal_today"`
which cal > /dev/null
if [ $? -eq 0 ]; then
	dbus-send --session --dest=$DBUS_NAME $DBUS_PATH $DBUS_INTERFACE.applet.ShowDialog  string:"`cal -h`" int32:$time_dialog_cal_today
else
	echo "$APP_NAME applet -> Script Name : $SCRIPT_NAME -> 'cal' isn't installed"
	call ShowDialog "string:\"ERROR: 'cal' isn't installed\"" "int32:5"
fi
#echo "$APP_NAME applet -> Script Name : $SCRIPT_NAME -> Left clic !"
exit
}

#############################################################################################################
on_middle_click() {
calendar_command=`get_conf_param "calendar_command"`

$calendar_command

#echo "$APP_NAME applet -> Script Name : $SCRIPT_NAME -> Middle clic !"
exit
}

#############################################################################################################
on_scroll_icon() {

date_TD=`date +%Y%m%d%H%M%S`

if [ $1 -eq 1 ]; then
	# Scroll UP

	time_dialog_cal_next=`get_conf_param "time_dialog_cal_next"`

	if test -e .wait; then
		date_WAIT=`head -n 1 .wait`
		if [ $date_TD -ge $(($date_WAIT+4)) ];then
			rm -f .wait_month .wait_year .wait1 # we wait for 4 sec
		fi
	fi

	which cal > /dev/null
	if [ $? -eq 0 ]; then
	MONTH_NEXT=1
	YEAR_NEXT=1
		if test -e ".wait_month" -a -e ".wait_year"; then
			MONTH_NEXT_READ=`head -n 1 .wait_month`
			YEAR_NEXT_READ=`head -n 1 .wait_year`
			MONTH_NEXT=$(($MONTH_NEXT_READ+1))
			if [ $MONTH_NEXT -eq 13 ]; then
				MONTH_NEXT=1
				YEAR_NEXT=$(($YEAR_NEXT_READ+1))
			else
				YEAR_NEXT=$YEAR_NEXT_READ
			fi
			echo $MONTH_NEXT > .wait_month
			echo $YEAR_NEXT > .wait_year
		else
			MONTH_NEXT=$((`date +%m`+1))
			if [ $MONTH_NEXT -eq 13 ]; then
				MONTH_NEXT=1
				date_YEAR=`date +%Y`
				YEAR_NEXT=$(($date_YEAR+1))
			else
				YEAR_NEXT=`date +%Y`
			fi
			echo $MONTH_NEXT > .wait_month
			echo $YEAR_NEXT > .wait_year
		fi
		dbus-send --session --dest=$DBUS_NAME $DBUS_PATH $DBUS_INTERFACE.applet.ShowDialog  string:" Next month :
`cal -h $MONTH_NEXT $YEAR_NEXT`" int32:$time_dialog_cal_next
		echo $date_TD > .wait
	else
		echo "$APP_NAME applet -> Script Name : $SCRIPT_NAME -> 'cal' isn't installed"
		call ShowDialog "string:\"ERROR: 'cal' isn't installed\"" "int32:5"
	fi

else
	# Scroll DOWN

	time_dialog_ev=`get_conf_param "time_dialog_ev"`

	which calendar > /dev/null
	if [ $? -nq 0 ]; then
		echo "$APP_NAME applet -> Script Name : $SCRIPT_NAME -> 'calendar' isn't installed"
		call ShowDialog "string:\"ERROR: 'calendar' isn't installed\"" "int32:5"
		exit
	fi

	if test -e .wait1; then
		date_WAIT=`head -n 1 .wait1`
		if [ $date_TD -ge $(($date_WAIT+3)) ];then
			# we wait for 3 sec
			calendar -f /usr/share/calendar/calendar.all > /dev/null # The loading takes some time :-/
			sleep 0.5
			dbus-send --session --dest=$DBUS_NAME $DBUS_PATH $DBUS_INTERFACE.applet.ShowDialog  string:"`calendar -f /usr/share/calendar/calendar.all`" int32:$time_dialog_ev
		else
			exit
		fi
	else
		dbus-send --session --dest=$DBUS_NAME $DBUS_PATH $DBUS_INTERFACE.applet.ShowDialog  string:"`calendar`" int32:$time_dialog_ev
	fi

	echo $date_TD > .wait1
fi

exit
}

#############################################################################################################
on_drop_data() {
import_command=`get_conf_param "import_command"`

if [ "`echo $DROP_DATA |grep 'file://'`" != "" ]; then 	# It's a file !
	DROP_DATA="`echo $DROP_DATA | cut -c 8-`"  # we remove 'file://' before the location
	$import_command $DROP_DATA
fi

exit
}

#############################################################################################################
begin() {
cp $CONF_FILE $CONF_FILE.bak
# Generate fresh calendar icon
get_ALL_conf_params
rm -f .wait .wait1 .wait_month .wait_year .day
if test `ps aux | grep -c "update_calendar"` -gt 1; then
	killall update_calendar.sh
fi
(bash update_calendar.sh "$icon_command" &)

exit
}

#############################################################################################################
end() {
rm -f .wait .wait1 .wait_month .wait_year .day
if test `ps aux | grep -c "update_calendar"` -gt 1; then
	killall update_calendar.sh
fi
}

#############################################################################################################
reload() {
diff $CONF_FILE $CONF_FILE.bak >/dev/null
if [ $? -eq 1 ]; then
	cp $CONF_FILE $CONF_FILE.bak
	get_ALL_conf_params
	rm -f .wait .wait1 .wait_month .wait_year .day
	if test `ps aux | grep -c "update_calendar"` -gt 1; then
		killall update_calendar.sh
	fi
	(bash update_calendar.sh "$icon_command" &)
fi
exit
}

#############################################################################################################

run $*

exit 0

