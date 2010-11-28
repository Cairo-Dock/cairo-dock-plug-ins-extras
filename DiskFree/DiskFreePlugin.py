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

from CairoDockPlugin import CairoDockPlugin
import os
import gobject
from Configuration import Configuration

class DiskFreePlugin(CairoDockPlugin):
	"""
	I print the available file system's space on my label.
	You can choose to view the result in Go or Mo. You can set the ellapsed
	time between two checks.
	"""
	def __init__(self):
		super(DiskFreePlugin, self).__init__()
		self.__interval = 60000 # 1 minute (in millisecondes)
		self.__isGiga = True # else mega-octet
		self.__config = Configuration(self.name())
		self.__timerId = None
	
	def getFreeSpace(self):
		"""
		I return the available space (in octet) at the root of the file system's.
		"""
		stats = os.statvfs('/')
		return stats.f_bsize * stats.f_bavail
		
	def onClick(self, iState):
		"""
		I set my label to the available space.
		"""
		super(DiskFreePlugin, self).onClick(iState)
		if self.__isGiga:
			gigaOctets = self.getFreeSpace() / (1024.0 * 1024 * 1024)
			label = "%.1f Go" % (gigaOctets)
		else:
			megaOctets = self.getFreeSpace() / (1024 * 1024)
			label = "%d Mo" % (megaOctets)
		self.setLabel(label)
		return True
	
	def onReload(self, bConfigHasChanged):
		"""
		Je recharge la configuration si besoin.
		"""
		super(DiskFreePlugin, self).onReload(bConfigHasChanged)
		if bConfigHasChanged:
			self.__setConfiguration()
		
	def __setConfiguration(self):
		"""
		I relaod the configuration.
		"""
		self.__config.refresh()
		interval = int(self.__config.get('Configuration', 'interval'))
		self.__interval = interval * 60000 # convert in millisecondes.
		self.__setTimer()
		self.__isGiga = self.__config.getboolean('Configuration', 'gigaView')
		self.setLabel(self.__config.get('Icon', 'name'))
	
	def __setTimer(self):
		"""
		I set the time between two checks.
		"""
		self.__removeTimer()
		self.__timerId = gobject.timeout_add(self.__interval, self.onClick, 0)
		
	def __removeTimer(self):
		"""
		I properly remove the timer.
		"""
		if self.__timerId != None:
			gobject.source_remove(self.__timerId)

	def run(self):
		"""
		Call me when you are ready 'to launch' the plugin's loop.
		"""
		self.__setConfiguration()
		self.onClick(0)
		super(DiskFreePlugin, self).run()
		self.__removeTimer()
