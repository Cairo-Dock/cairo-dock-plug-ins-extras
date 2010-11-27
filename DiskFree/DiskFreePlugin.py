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

from CairoDockPlugin import CairoDockPlugin
import os
import gobject
from Configuration import Configuration

class DiskFreePlugin(CairoDockPlugin):
	"""
	J'affiche l'espace disque disponible au dessus de mon icône. Vous pouvez
	choisir de voir le résultat en giga-octets ou en méga-octets. Vous pouvez
	aussi définir l'intervalle, en minutes, entre deux sondages du disque.
	"""
	def __init__(self):
		super(DiskFreePlugin, self).__init__()
		self.__interval = 60000 # 1 minute (en millisecondes)
		self.__isGiga = True # sinon mega-octet
		self.__config = Configuration(self.name())
		self.__timerId = None
	
	def getFreeSpace(self):
		"""
		Je retourne l'espace disque disponible (le nombre d'octets) à la 
		racine du système de fichier. 
		"""
		stats = os.statvfs('/')
		return stats.f_bsize * stats.f_bavail
		
	def onClick(self, iState):
		"""
		Je modifie mon label pour qu'il reflète l'espace disque disponible.
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
		Je recharge la configuration.
		"""
		self.__config.refresh()
		interval = int(self.__config.get('Configuration', 'intervalle'))
		self.__interval = interval * 60000 # obtenir en millisecondes.
		self.__setTimer()
		self.__isGiga = self.__config.getboolean('Configuration', 'vueEnGiga')
		self.setLabel(self.__config.get('Icon', 'name'))
	
	def __setTimer(self):
		"""
		Je programme l'intervalle entre deux sondages du disque.
		"""
		self.__removeTimer()
		self.__timerId = gobject.timeout_add(self.__interval, self.onClick, 0)
		
	def __removeTimer(self):
		"""
		J'enlève proprement le timer.
		"""
		if self.__timerId != None:
			gobject.source_remove(self.__timerId)

	def run(self):
		"""
		On m'appelle pour 'lancer' le plugin.
		"""
		self.__setConfiguration()
		self.onClick(0)
		super(DiskFreePlugin, self).run()
		self.__removeTimer()
