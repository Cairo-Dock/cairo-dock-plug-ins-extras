#!/usr/bin/python

# This is a part of the external Twitter applet for Cairo-Dock
#
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br

import os

try:
	import gtk
except:
	from gi.repository import Gtk as gtk

from message import DirectMessage, Tweet

class Menu(gtk.Menu):

  def __init__(self, icon, callback=None):
    gtk.Menu.__init__(self)
    
    self.messages = []
    self.icon = icon
    self.callback = callback
      
  def add(self, message):
    self.messages.append(message)
  
  def pop_up(self):
    for message in self.messages:
      item = gtk.ImageMenuItem()
      # the true label is set after with set_markup()
      if isinstance(message, DirectMessage):
        item.set_label(message.sender)                                                # used to track who sent the message in order to reply it.
      elif isinstance(message, Tweet):
        item.set_label(message.uid)                                                   # used to retweet the tweet
      item.set_image(gtk.image_new_from_file(os.path.abspath("./data/message_%s.png" % message.network)))
      text = "<b>%s</b>\n%s" % (message.sender, message.text)
      item.get_children()[0].set_markup(text)
      if self.callback:                                                               # for tweets posted by the user, there is not callback to be set
        item.connect('activate', self.callback)
      self.append(item)
      # add a separator if mail is not last in list
      if self.messages.index(message) != len(self.messages) - 1:
        separator = gtk.SeparatorMenuItem()
        self.append(separator)

    self.show_all()
    self.popup(parent_menu_shell=None, parent_menu_item=None, func=self.get_xy, data=(400, 400), button=1, activate_time=0)

  def get_xy(self, m, data):
    # fetch icon geometry
    icondata = self.icon.GetAll()
    iconContainer  = icondata['container']
    iconOrientation = icondata['orientation']
    iconWidth = icondata['width']
    iconHeight = icondata['height']
    iconPosX = icondata['x']
    iconPosY = icondata['y']

    # get menu geometry
    menuWidth, menuHeight = m.size_request()

    # adapt to container and orientation
    if iconContainer == 1:  # Then it's a desklet, always oriented in a bottom-like way.
      if iconPosY['y'] < (gtk.gdk.screen_height() / 2):
        iconOrientation = 1
      else:
        iconOrientation = 0

    if iconOrientation == 0:
      # compute position of menu
      x = iconPosX - (menuWidth / 2)
      y = iconPosY - (iconHeight / 2) - menuHeight

    else:
      x = iconPosX - (menuWidth / 2)
      y = iconPosY + (iconHeight / 2)

    return (x, y, True)
