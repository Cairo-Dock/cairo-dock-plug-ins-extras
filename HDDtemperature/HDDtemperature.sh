#!/bin/bash

# This is a part of the external applets for Cairo-Dock
#
# Copyright : (C) 2010-2011 by Nochka85
#                      modified by matttbe for the new API
#                      modified by Fabounet for the new interface
# E-mail : nochka85@glx-dock.org
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# ERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# http://www.gnu.org/licenses/licenses.html#GPL

### This is a part of the external applet HDDtemperature for cairo-dock
### Author : Reali$t
### Rev : 14 sep 2011

. /usr/share/cairo-dock/plug-ins/Dbus/CDBashApplet.sh $*

#############################################################################################################

is_daemon()
{
if [ -z `pidof hddtemp` ]; then
  call ShowDialog "string:\"'hddtemp' daemon is not running!\r Type in terminal to run it:\r service hddtemp start\"" "int32:0"
  call SetQuickInfo "string:"
  return 1
fi
}

#############################################################################################################

on_click()
{

is_daemon
ret_val=$?
if [ "$ret_val" -ne "0" ]; then
  exit
fi

DURATION=`get_conf_param "para_dur"`

FULL_INFO=`cat store | tr '\n' "\r "`

call ShowDialog "string:'$FULL_INFO'" "int32:$DURATION"
}

#############################################################################################################

begin()
{
  is_daemon
  ret_val=$?
  if [ "$ret_val" -ne "0" ]; then
    exit
  fi

HDDS=`get_conf_param "para_hdds"`
SHOW_ICON=`get_conf_param "para_show"`
TIME_INT=`get_conf_param "para_time"`
ALERT_LEVEL=`get_conf_param "para_alert"`
HDDT_port=`get_conf_param "para_port"`
SEPARATOR=`get_conf_param "para_sep"`
SEPARATOR=${SEPARATOR:0:1}

  HDTEMP=$(ncat localhost $HDDT_port | awk -F $SEPARATOR -v HDDS_awk="$HDDS" '{
    if (NF<5) exit;                # 5 fields per device
    T=0
    for(i=0;(i<=NF-5);i+=5) {
      if (HDDS_awk ~ $(i+2)) {
        string_awk=string_awk $(i+2) " ("$(i+3)"): " $(i+4) "°" $(5) FS
        if (T<$(i+4)) T=$(i+4)      # max temperature will be shown
      }
    }
    string_awk=string_awk T
    print string_awk
  }')

  set -- "$HDTEMP"
  IFS="$SEPARATOR"
  declare -a Array=($*)
  len_Array=${#Array[@]}
  let "len_Array-=1"           # numbering from 0
  unset IFS

  if [ $SHOW_ICON = "true" ]; then
    call SetQuickInfo "string:'${Array[len_Array]}''°'"
  fi

  if [ ${Array[len_Array]} -ge $ALERT_LEVEL ]; then
    call Animate "string:fire" "int32:900"
  else
    call Animate "string:fire" "int32:0"
  fi

  cp /dev/null store
  for i in "${Array[@]:0:$len_Array}"; do         # to last-but-one (before temperature)
    echo "$i" >> store
  done

  echo  "dbus-send --session --dest=org.cairodock.CairoDock /org/cairodock/CairoDock
         org.cairodock.CairoDock.ReloadModule string:HDDtemperature" \
        | at now + $TIME_INT min                  # refresh in background
}

#############################################################################################################

end()
{
rm -f store
}

#############################################################################################################

reload()
{

SHOW_ICON=`get_conf_param "para_show"`

if [ $SHOW_ICON = "false" ]; then
  call SetQuickInfo "string:"
fi

begin
}

#############################################################################################################

run $*

exit 0
