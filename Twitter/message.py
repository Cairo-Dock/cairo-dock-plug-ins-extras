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

# Can be either a Tweet or a Direct Message
class Message:
  def __init__(self, text, sender, network):
    self.text = text
    self.sender = sender
    self.network = network
    
class DirectMessage(Message):
  def __init__(self, text, sender, network):
    Message.__init__(self, text, sender, network)

class Tweet(Message):
  def __init__(self, text, sender, uid, network):
    Message.__init__(self, text, sender, network)
    self.uid = uid                                                                          # it is going to be used to retweet this Tweet
