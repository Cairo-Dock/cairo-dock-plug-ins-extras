#!/bin/bash

NEEDED_EXTRAS="ruby1.8-dev ruby1.8 ri1.8 rdoc1.8 libruby1.8 rubygems1.8 acpi python libxslt-dev libxml2-dev ruby python-xlib xclip"

NORMAL="\\033[0;39m"
BLEU="\\033[1;34m"
VERT="\\033[1;32m" 
ROUGE="\\033[1;31m"

LOG_CD=../log.txt

install_pkg() {
#	for tested in $NEEDED_EXTRAS; do
#		dpkg -s $tested |grep installed |grep "install ok" > /dev/null
#		if [ $? -eq 1 ]; then
#			sudo apt-get install -qq $tested  >> $LOG_CD
#		fi
#	done
	sudo apt-get install -qq -y --force-yes $NEEDED_EXTRAS  >> $LOG_CD
}

install_pkg >> $LOG_CD

	# RubyBattery
if ! test -e '../.gem'; then
	sudo gem install rbus
	sudo gem install parseconfig
	touch '../.gem'
fi
if ! test -e '../.gem2'; then
	sudo gem install nokogiri
	sudo gem install launchy
	touch '../.gem2'
fi
if ! test -e '../.rubydbus'; then
	wget http://github.com/downloads/mvidner/ruby-dbus/ruby-dbus-0.3.0.tgz
	tar -xzf ruby-dbus-0.3.0.tgz
	cd ruby-dbus-0.3.0/
	ruby setup.rb config
	ruby setup.rb setup
	sudo ruby setup.rb install
	cd ..
	sudo rm -rf ruby-dbus-0.3.0/ ruby-dbus-0.3.0.tgz
	touch '../.rubydbus'
fi
if ! test -e '../.cpan'; then
	xterm -e "sh -c 'echo Installation of two CPan modules for ShortURL applet, please write your password and answer «yes» if it is asked && sudo cpan -i LWP Clipboard'"
	touch '../.cpan'
fi
