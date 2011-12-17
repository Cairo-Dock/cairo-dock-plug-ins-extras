#!/usr/bin/python

# This is a part of the external Twitter applet for Cairo-Dock
#
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br

def logp (string):
    print "[+] Twitter: %s" % string

def logm (string):
    print "[-] Twitter: %s" % string

# Read the user's consumer key and secret necessary for the requests
def read_consumer_key_and_secret():
		try:
			f = open('.keys')
			data = f.read()
			f.close()
		except IOError:
			logm("It was not possible to read the consumer key and secret, check the .keys file")
		else:
			return data.split()
