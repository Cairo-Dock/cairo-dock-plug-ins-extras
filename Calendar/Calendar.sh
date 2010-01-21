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

## Rev : 21/01/2010

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
CONF_FILE="/home/$USER/.config/cairo-dock/current_theme/plug-ins/$APP_NAME/$APP_NAME.conf"

#############################################################################################################
get_conf_param() {
LIGNE=`cat $CONF_FILE | grep "$1"`
PARAM="`echo $LIGNE | cut -f2 -d '=' `"
}

#############################################################################################################
get_ALL_conf_params() {

get_conf_param "calendar_command"
calendar_command="$PARAM"

get_conf_param "import_command"
import_command="$PARAM"

#get_conf_param "reload_message"
#reload_message="$PARAM"

get_conf_param "time_dialog_cal_today"
time_dialog_cal="$PARAM"

get_conf_param "time_dialog_ev"
time_dialog_ev="$PARAM"

get_conf_param "time_dialog_cal_next"
time_dialog_cal_next="$PARAM"

}

#############################################################################################################
action_on_click() {
get_conf_param "time_dialog_cal_today"
time_dialog_cal_today="$PARAM"
which cal > /dev/null
if [ $? -eq 0 ]; then
	dbus-send --session --dest=$DBUS_NAME $DBUS_PATH/$APP_NAME $DBUS_INTERFACE.applet.ShowDialog string:"`cal`" int32:$time_dialog_cal_today
else
	echo "$APP_NAME applet -> Script Name : $SCRIPT_NAME -> 'cal' isn't installed"
	dbus-send --session --dest=$DBUS_NAME $DBUS_PATH/$APP_NAME $DBUS_INTERFACE.applet.ShowDialog string:"ERROR: 'cal' isn't installed" int32:5
fi
#echo "$APP_NAME applet -> Script Name : $SCRIPT_NAME -> Left clic !"
exit
}

#############################################################################################################
action_on_middle_click() {
get_conf_param "calendar_command"
calendar_command="$PARAM"

$calendar_command

#echo "$APP_NAME applet -> Script Name : $SCRIPT_NAME -> Middle clic !"
exit
}

#############################################################################################################
action_on_scroll_icon() {

date_TD=`date +%Y%m%d%H%M%S`

if [ $SCROLL_UP -eq "0" ]; then
	# Scroll UP

	get_conf_param "time_dialog_cal_next"
	time_dialog_cal_next="$PARAM"

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
		dbus-send --session --dest=$DBUS_NAME $DBUS_PATH/$APP_NAME $DBUS_INTERFACE.applet.ShowDialog string:" Next month :
`cal $MONTH_NEXT $YEAR_NEXT`" int32:$time_dialog_cal_next
		echo $date_TD > .wait
	else
		echo "$APP_NAME applet -> Script Name : $SCRIPT_NAME -> 'cal' isn't installed"
		dbus-send --session --dest=$DBUS_NAME $DBUS_PATH/$APP_NAME $DBUS_INTERFACE.applet.ShowDialog string:"ERROR: 'cal' isn't installed" int32:5
	fi

else
	# Scroll DOWN

	get_conf_param "time_dialog_ev"
	time_dialog_ev="$PARAM"

	which calendar > /dev/null
	if [ $? -nq 0 ]; then
		echo "$APP_NAME applet -> Script Name : $SCRIPT_NAME -> 'calendar' isn't installed"
		dbus-send --session --dest=$DBUS_NAME $DBUS_PATH/$APP_NAME $DBUS_INTERFACE.applet.ShowDialog string:"ERROR: 'calendar' isn't installed" int32:5
		exit
	fi

	if test -e .wait1; then
		date_WAIT=`head -n 1 .wait1`
		if [ $date_TD -ge $(($date_WAIT+3)) ];then
			# we wait for 3 sec
			calendar -f /usr/share/calendar/calendar.all > /dev/null # The loading takes some time :-/
			dbus-send --session --dest=$DBUS_NAME $DBUS_PATH/$APP_NAME $DBUS_INTERFACE.applet.ShowDialog string:"`calendar -f /usr/share/calendar/calendar.all`" int32:$time_dialog_ev
		else
			exit
		fi
	else
		dbus-send --session --dest=$DBUS_NAME $DBUS_PATH/$APP_NAME $DBUS_INTERFACE.applet.ShowDialog string:"`calendar`" int32:$time_dialog_ev
	fi

	echo $date_TD > .wait1
fi

exit
}

#############################################################################################################
action_on_drop_data() {
get_conf_param "import_command"
import_command="$PARAM"
echo "$APP_NAME applet -> Script Name : $SCRIPT_NAME -> $DROP_DATA has been dropped on applet !"

if [ "`echo $DROP_DATA |grep 'file://'`" != "" ]; then 	# It's a file !
	DROP_DATA="`echo $DROP_DATA | cut -c 8-`"  # we remove 'file://' before the location
	#dbus-send --session --dest=$DBUS_NAME $DBUS_PATH/$APP_NAME $DBUS_INTERFACE.applet.ShowDialog string:"FILE : $DROP_DATA has been dropped on applet" int32:4
	$import_command $DROP_DATA
fi

exit
}

#############################################################################################################
action_on_init() {
# Generate fresh calendar icon
./icon.sh
rm -f .wait .wait1 .wait_month .wait_year
get_ALL_conf_params

#echo "$APP_NAME applet -> Script Name : $SCRIPT_NAME -> The calendar_command in config is : $calendar_command"
#echo "$APP_NAME applet -> Script Name : $SCRIPT_NAME -> The import_command in config is : $import_command"
#echo "$APP_NAME applet -> Script Name : $SCRIPT_NAME -> The time_dialog_cal_today in config is : '$time_dialog_cal_today'"
#echo "$APP_NAME applet -> Script Name : $SCRIPT_NAME -> The time_dialog_ev in config is : '$time_dialog_ev'"
#echo "$APP_NAME applet -> Script Name : $SCRIPT_NAME -> The time_dialog_cal_next in config is : '$time_dialog_cal_next'"
#echo "$APP_NAME applet -> Script Name : $SCRIPT_NAME -> Our module is started"

exit
}

#############################################################################################################
action_on_stop() {
echo "$APP_NAME applet -> Script Name : $SCRIPT_NAME -> Stop"
rm -f .wait .wait1 .wait_month .wait_year .day
killall update_calendar.sh
}

#############################################################################################################
action_on_reload() {
get_ALL_conf_params
rm -f .wait .wait1 .wait_month .wait_year
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
elif [ "`echo $ACTION |grep 'action_on_scroll_icon'`" != "" ]; then
	action_on_scroll_icon
elif [ "`echo $ACTION |grep 'action_on_drop_data'`" != "" ]; then
	action_on_drop_data
elif [ "`echo $ACTION |grep 'action_on_init'`" != "" ]; then
	action_on_init
elif [ "`echo $ACTION |grep 'action_on_stop'`" != "" ]; then
	action_on_stop
elif [ "`echo $ACTION |grep 'action_on_reload'`" != "" ]; then
	action_on_reload
elif [ "`echo $ACTION |grep 'action_on_build_menu'`" != "" ]; then
	action_on_build_menu
elif [ "`echo $ACTION |grep 'action_on_menu_select'`" != "" ]; then
	action_on_menu_select
fi

exit

