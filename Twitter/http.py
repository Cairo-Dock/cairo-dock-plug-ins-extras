#!/usr/bin/python

# This is a part of the external Twitter applet for Cairo-Dock
#
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br

import urllib2

# HTTP GET
def get(url):
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	return response.read()

# HTTP POST
def post(url, post_data):
	return urllib2.urlopen(url, post_data)
