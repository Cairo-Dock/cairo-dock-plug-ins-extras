#!/usr/bin/python

# This is a part of the external Twitter applet for Cairo-Dock
#
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br

import urllib2
from util import logp, logm

# HTTP GET
def get(url, tries = 0):
	while True:
		try:
			logp("Trying to connect to %s" % url)
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			return response.read()
		except urllib2.HTTPError:
			tries += 1
			if tries > 3:
				raise			

# HTTP POST
def post(url, post_data, tries = 0):
	while True:
		try:
			return urllib2.urlopen(url, post_data)
		except urllib2.HTTPError:
			tries += 1
			if tries > 3:
				raise
