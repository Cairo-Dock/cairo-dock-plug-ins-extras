#!/bin/bash

NEEDED_EXTRAS="python libxslt1-dev libxml2-dev xclip valac"

LOG_CD=../log.txt

install_pkg() {
	for tested in $NEEDED_EXTRAS
	do
		dpkg -s $tested |grep installed |grep "install ok" > /dev/null
		if [ $? -eq 1 ]; then
			echo -e "This package $tested isn't installed : Installation"
			paquetsPresent="$paquetsPresent $tested"
			# sudo apt-get install -qq $tested  >> $LOG_CAIRO_DOCK
		fi
	done

	for testPkg in $paquetsPresent; do
		sudo apt-get install -s $testPkg > /dev/null 2>&1
		if [ $? -eq 0 ]; then
			paquetsOK="$paquetsOK $testPkg"
		else
			echo -e "This package $testPkg isn't available"
		fi
	done

	sudo apt-get install -y --force-yes -m -qq $paquetsOK >> $LOG_CD
	if [ $? -ne 0 ]; then ERROR=1; fi
}

install_pkg 2> /dev/null

if test -n "$ERROR"; then exit 1; fi
