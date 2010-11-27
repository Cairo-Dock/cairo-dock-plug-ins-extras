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

from ConfigParser import RawConfigParser
from os.path import isfile
from os.path import expanduser
import sys

CAIRO_CONF_PATH = "~/.config/cairo-dock/current_theme/plug-ins"

class Configuration(RawConfigParser):
	"""
	Je gère le fichier de configuration d'un plugin Cairo-Dock.
	"""
	def __init__(self, nameOfPlugin):
		RawConfigParser.__init__(self)
		self.nameOfPlugin = ''
		self.__setFile(nameOfPlugin)

	def __setFile(self, nameOfPlugin):
		"""
		Je trouve le nom du fichier de configuration grâce au nom du plugin,
		puis je lis la configuration.
		"""
		nameOfPlugin = "%s/%s/%s.conf" % (CAIRO_CONF_PATH, nameOfPlugin, nameOfPlugin)
		nameOfPlugin = expanduser(nameOfPlugin)
		if isfile(nameOfPlugin):
			self.nameOfPlugin = nameOfPlugin
			self.refresh()
		else:
			print "%s n'existe pas ! Fin du programme." % (nameOfPlugin)
			sys.exit(1)
	
	def refresh(self):
		"""
		Je lis le fichier de configuration.
		"""
		self.readfp(open(self.nameOfPlugin))
