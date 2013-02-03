# -*- coding: utf-8 -*-

# DiskFree, plugin for Cairo-Dock. View the available disk space.
# Copyright 2010 Xavier Nayrac
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import print_function

try:
	import ConfigParser # python 2
except:
	import configparser # python 3
from os.path import isfile
from os.path import expanduser
import sys

CAIRO_CONF_PATH = "~/.config/cairo-dock/current_theme/plug-ins"

class Configuration(RawConfigParser):
	"""
	I manage the configuration's file of a Cairo-Dock plugin.
	"""
	def __init__(self, nameOfPlugin):
		RawConfigParser.__init__(self)
		self.nameOfPlugin = ''
		self.__setFile(nameOfPlugin)

	def __setFile(self, nameOfPlugin):
		"""
		I set the name of the configuration's file, with the help of plugin's name.
		Then I read the configuration.
		"""
		nameOfPlugin = "%s/%s/%s.conf" % (CAIRO_CONF_PATH, nameOfPlugin, nameOfPlugin)
		nameOfPlugin = expanduser(nameOfPlugin)
		if isfile(nameOfPlugin):
			self.nameOfPlugin = nameOfPlugin
			self.refresh()
		else:
			print("%s n'existe pas ! Fin du programme." % (nameOfPlugin))
			sys.exit(1)
	
	def refresh(self):
		"""
		I read the configuration's file.
		"""
		self.readfp(open(self.nameOfPlugin))
