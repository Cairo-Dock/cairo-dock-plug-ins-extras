# -*- coding: utf-8 -*-

# YoutubeDl, plugin for Cairo-Dock. View the available disk space.
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

import os.path
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import sys
import gobject

CAIRO_SERVICE = 'org.cairodock.CairoDock'
CAIRO_APPLET = 'org.cairodock.CairoDock.applet'
CAIRO_PATH = '/org/cairodock/CairoDock/'

class CairoDockPlugin(object):
	"""
	I'm a basic Cairo-Dock plugin.
	I mainly set the D-bus stuff.
	"""
	def __init__(self):
		self.__debugMode = False
		self.__name = os.path.basename(os.path.abspath("."))
		self.__path = CAIRO_PATH + self.__name
		self.__plugin = None # Je sert d'interface avec D-bus.
		self.__programLoop = None
		self.__initPlugin()
		
	def __initPlugin(self):
		self.__initDbus()
		self.__initCallbacks()
		self.__initLoop()
	
	def __initDbus(self):
		DBusGMainLoop(set_as_default = True)
		bus = dbus.SessionBus()
		try:
			dbusObject = bus.get_object(CAIRO_SERVICE, self.__path)
		except dbus.DBusException:
			print "<%s can't be found on the bus, exit>" % (self.__name)
			sys.exit(1)
		self.__plugin = dbus.Interface(dbusObject, CAIRO_APPLET)
	
	def __initCallbacks(self):
		self.__plugin.connect_to_signal("on_click", self.onClick)
		self.__plugin.connect_to_signal("on_middle_click", self.onMiddleClick)
		self.__plugin.connect_to_signal("on_stop_module", self.onStop)
		self.__plugin.connect_to_signal("on_reload_module", self.onReload)
		self.__plugin.connect_to_signal("on_drop_data", self.onDropData)
		self.__plugin.connect_to_signal("on_build_menu", self.onBuildMenu)
		self.__plugin.connect_to_signal("on_menu_select", self.onMenuSelect)
		self.__plugin.connect_to_signal("on_answer_dialog", self.onAnswerDialog)
	
	def __initLoop(self):
		self.__programLoop = gobject.MainLoop()
	
	def name(self):
		return self.__name
		
	def run(self):
		"""
		I'm connecting to the Cairo-Dock's program loop. 
		To 'run' the plugin, call me when all initializations are done.
		"""
		self.messageDebug('run')
		self.__programLoop.run()

	def debug(self):
		"""
		Call me one time in the beginning of your script. If you are running Cairo-Dock
		from a console window, you'll be able to see what I'm doing.
		"""
		self.__debugMode = True
	
	def onClick(self, iState):
		"""
		I react to left click on my icon.
		"""
		self.messageDebug('left clic %d' % iState)
	
	def onMiddleClick(self):
		"""
		I react to left click on my icon.
		"""
		self.messageDebug('middle clic ')
		
	def onStop(self):
		"""
		Time to quit.
		"""
		self.messageDebug('stop')
		self.__programLoop.quit()
	
	def onReload(self, bConfigHasChanged):
		"""
		I just was reloaded. Check for a new configuration.
		"""
		self.messageDebug('reloaded')
		if bConfigHasChanged:
			self.messageDebug('new configuration')

	def messageDebug(self, message):
		"""
		I write message to console if I have permission to do this.
		"""
		if self.__debugMode:
			print '<%s : %s>' % (self.__name, message)

	def setLabel(self, label):
		"""
		I update my icon's label.
		"""
		self.__plugin.SetLabel(label)

	def setQuickInfo(self, info):
		"""
		I update my icon's QuickInfo.
		"""
		self.__plugin.SetQuickInfo(info)

	def SetIcon(self, label):
		"""
		I update my icon's icon.
		"""
		self.__plugin.SetIcon(label)

	def ShowDialog(self, message, time):
		"""
		I update my icon's Show Dialog.
		"""
		self.__plugin.ShowDialog(message, time)

	def PopupDialog(self, dialog_attributes, widget_attributes):
		"""
		I update my icon's Show Dialog.
		"""
		self.__plugin.PopupDialog(dialog_attributes, widget_attributes)

	def DemandsAttention(self, flag, effect):
		"""
		I update my icon's Demands Attention.
		"""
		self.__plugin.DemandsAttention(flag, effect)

	def AddMenuItems(self, items):
		"""
		I update my icon's AddMenuItems.
		"""
		self.__plugin.AddMenuItems(items)
