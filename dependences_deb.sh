#!/bin/bash

NEEDED_EXTRAS="python libxslt-dev libxml2-dev xclip valac"

LOG_CD=../log.txt

install_pkg() {
	sudo apt-get install -qq -y --force-yes $NEEDED_EXTRAS  >> $LOG_CD
}

install_pkg >> $LOG_CD

# written in vala, we have to use valac.
if test -d 'CairoBzr'; then
	cd CairoBzr
	./compile.sh >> $LOG_CD 2>> ../$LOG_CD
	cd ..
fi
