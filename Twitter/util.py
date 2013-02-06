#!/usr/bin/python

# This is a part of the external Twitter applet for Cairo-Dock
#
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br
#
# This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

# This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.

from __future__ import print_function

try:
  import configparser as ConfigParser
except:
  import ConfigParser

def logp (string):
  print("[+] Twitter: %s" % string)

def logm (string):
  print("[-] Twitter: %s" % string)

def camelcase(string):
  """ capitalizes only first character of a string """
  return string[0].capitalize() + string[1:]

# Read the user's consumer key and secret necessary for the requests
def read_consumer_key_and_secret(network="twitter"):
  try:
    config = ConfigParser.ConfigParser()
    config.read('.keys.cfg')
    logp("%s: Consumer key: %s\nConsumer secret: %s" % (network, config.get(network, 'consumer_key'), config.get(network, 'consumer_secret')) )
    return config.get(network, 'consumer_key'), config.get(network, 'consumer_secret')
  except configparser.Error:
    logm("It was not possible to read the consumer key and secret for '%s', check the .keys.cgf file" % network)
