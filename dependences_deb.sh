#!/bin/bash

NEEDED_EXTRAS="ruby1.8-dev ruby1.8 ri1.8 rdoc1.8 irb1.8 libreadline-ruby1.8 libruby1.8 rubygems1.8 acpi python"

NORMAL="\\033[0;39m"
BLEU="\\033[1;34m"
VERT="\\033[1;32m" 
ROUGE="\\033[1;31m"

LOG_CD=../log.txt

install_pkg() {
	for tested in $NEEDED_EXTRAS; do
		dpkg -s $tested |grep installed |grep "install ok" > /dev/null
		if [ $? -eq 1 ]; then
			sudo apt-get install -qq $tested  >> $LOG_CD
		fi
	done
}

install_pkg >> $LOG_CD

	# RubyBattery
if ! test -e '../.gem'; then
	sudo gem install rbus
	sudo gem install parseconfig
	touch '../.gem'
fi
