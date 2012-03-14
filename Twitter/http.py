#!/usr/bin/python

# This is a part of the external Twitter applet for Cairo-Dock
#
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br

import urllib2, urllib
from util import logp, logm

# HTTP GET
def get(url, tries = 0):
  while True:
    try:
      logp("GET: Trying to connect to %s" % url)
      request = urllib2.Request(url)
      response = urllib2.urlopen(request)
      return response.read()
    except urllib2.HTTPError:
      tries += 1
      if tries > 3:
        raise

# HTTP POST
def post(url, params, header, tries = 0):
  while True:
    try:
      logp("POST: Trying to connect to %s" % url)
      data = urllib.urlencode(params)
      request = urllib2.Request(url, data, headers=header)
      response = urllib2.urlopen(request)
      return response.read()
    except urllib2.HTTPError:
      tries += 1
      if tries > 3:
        raise
        
#def stream(url):
#  req = urllib2.urlopen(url)
#  buffer = ''
#  while True:
#    chunk = req.read(1)
#    if not chunk:
#      print buffer
#      break
#    
#    chunk = unicode(chunk)
#    buffer += chunk
#    
#    tweets = buffer.split("\n",1)
#    if len(tweets) > 1:
#      print tweets[0]
#      #return json.loads(tweets[0])
#      buffer = tweets[1]
#      #return tweety
