#!/usr/bin/python

# This is a part of the external Twitter applet for Cairo-Dock
#
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br

try:  # python 3
  import urllib.request, urllib.error, urllib.parse
  urllib_request = urllib.request
  urllib_error = urllib.error
  urllib_parse = urllib.parse
except:  # python 2
  import urllib2, urllib
  urllib_request = urllib2
  urllib_error = urllib2
  urllib_parse = urllib
from util import logp, logm
from time import sleep

# HTTP GET
def get(url, tries = 0):
  while True:
    try:
      logp("GET: Trying to connect to %s" % url)
      request = urllib_request.Request(url)
      response = urllib_request.urlopen(request)
      return response.read()
    except:  # urllib_error.HTTPError or urllib_error.URLError
      tries += 1
      sleep(.33)
      if tries > 3:
        raise

# HTTP POST
def post(url, params, header, tries = 0):
  while True:
    try:
      logp("POST: Trying to connect to %s" % url)
      data = urllib_parse.urlencode(params)
      request = urllib_request.Request(url, data, headers=header)
      response = urllib_request.urlopen(request)
      return response.read()
    except:  # urllib_error.HTTPError or urllib_error.URLError
      tries += 1
      sleep(.33)
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
