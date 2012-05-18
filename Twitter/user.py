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

import os

from util import *

class User:
  def __init__(self, screen_name="", access_key="", access_secret="", network="twitter"):
    self.screen_name = screen_name
    self.access_key = access_key
    self.access_secret = access_secret
    self.network = network
    self.user_file = os.path.abspath(os.path.join(os.getcwd(),'..','..','.%s_users' % self.network))      # ~/.config/cairo-dock/.twitter_users
  
  # TODO: Implement it as a config file using screen_name as section index
  def read(self):
    """Read the users file formated as Screen Name<space>Access Key<space>Access Secret"""
    found = False
    if os.path.exists(self.user_file):
      if os.path.getsize(self.user_file) > 0:
        f = open(self.user_file, "rb")
        data = f.read()
        self.screen_name, self.access_key, self.access_secret = data.split()                              # split the line by space token
        f.close()
        found = True
    return found

  def write(self):
    logp("Writing user data for %s" % self.network)
    f = open(self.user_file, 'w')
    f.write("%s %s %s" % (self.screen_name, self.access_key, self.access_secret))
    f.close()
    
  def exists(self):
    return self.read()

