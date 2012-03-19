#!/usr/bin/python

# This is a part of the external Twitter applet for Cairo-Dock
#
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br

# Can be either a Tweet or a Direct Message
class Message:
  def __init__(self, text, sender):
    self.text = text
    self.sender = sender
    
class DirectMessage(Message):
  def __init__(self, text, sender):
    Message.__init__(self, text, sender)

class Tweet(Message):
  def __init__(self, text, sender, uid):
    Message.__init__(self, text, sender)
    self.uid = uid                                                                          # it is going to be used to retweet this Tweet
