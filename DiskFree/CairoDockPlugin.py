# -*- coding: utf-8 -*-

# DiskFree, plugin pour Cairo-Dock.
# Copyright 2010 Xavier Nayrac
#
# Ce programme est un logiciel libre ; vous pouvez le redistribuer ou le
# modifier suivant les termes de la “GNU General Public License” telle que
# publiée par la Free Software Foundation : soit la version 3 de cette
# licence, soit (à votre gré) toute version ultérieure.
#
# Ce programme est distribué dans l’espoir qu’il vous sera utile, mais SANS
# AUCUNE GARANTIE : sans même la garantie implicite de COMMERCIALISABILITÉ
# ni d’ADÉQUATION À UN OBJECTIF PARTICULIER. Consultez la Licence Générale
# Publique GNU pour plus de détails.
#
# Vous devriez avoir reçu une copie de la Licence Générale Publique GNU avec
# ce programme ; si ce n’est pas le cas, consultez :
# <http://www.gnu.org/licenses/>.

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
	Je suis un plugin basique pour Cairo-Dock.
	Je m'occupe principalement de la connexion avec D-bus.
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
		self.__plugin.connect_to_signal("on_stop_module", self.onStop)
		self.__plugin.connect_to_signal("on_reload_module", self.onReload)
	
	def __initLoop(self):
		self.__programLoop = gobject.MainLoop()
	
	def name(self):
		return self.__name
		
	def run(self):
		"""
		Je me connecte à la boucle de programme de Cairo-Dock. Appelez moi une fois
		les initialisations faites, pour 'lancer' le plugin.
		"""
		self.__messageDebug('run')
		self.__programLoop.run()

	def debug(self):
		"""
		Appelez une fois au début de votre programme. Si vous avez lancé Cairo-Dock 
		depuis une console, vous saurez quelles actions j'effectue.
		"""
		self.__debugMode = True
	
	def onClick(self, iState):
		"""
		Je réagis au clic gauche de la souris sur mon icône.
		"""
		self.__messageDebug('left clic %d' % iState)
		
	def onStop(self):
		"""
		Je réagis quand on met fin à mon execution.
		"""
		self.__messageDebug('stop')
		self.__programLoop.quit()
	
	def onReload(self, bConfigHasChanged):
		"""
		J'ai été rechargé, peut-être à cause d'une nouvelle configuration.
		"""
		self.__messageDebug('reloaded')
		if bConfigHasChanged:
			self.__messageDebug('new configuration')

	def __messageDebug(self, message):
		"""
		J'écris le message sur la console, si j'ai la permission.
		"""
		if self.__debugMode:
			print '<%s : %s>' % (self.__name, message)

	def setLabel(self, label):
		"""
		Je met à jour le label de mon icône.
		"""
		self.__plugin.SetLabel(label)
