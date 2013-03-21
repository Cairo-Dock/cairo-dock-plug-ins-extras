#!/usr/bin/python

# This is a part of the third-party applets for Cairo-Dock
#
# Copyright : (C) 2010 by ppmt and Tofe
# E-mail : ppmt@glx-dock.org and chris.chapuis@gmail.com
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# http://www.gnu.org/licenses/licenses.html#GPL

from __future__ import print_function

#### transparent gtk window with text
try:
	import gtk
	from gtk import gdk
	import cairo
	import pango
except:
	from gi.repository import Gtk as gtk
	from gi.repository import Gdk as gdk
	from gi.repository import cairo
	from gi.repository import Pango as pango

# translations
from CDApplet import _

class TransparentPostIt(gtk.Window):
	def __init__(self):
		super(TransparentPostIt, self).__init__()

		self.set_title(_('GTG PostIt'))
		self.resize(200, 100)
		# Tell GTK+ that we want to draw the windows background ourself.
		# If we don't do this then GTK+ will clear the window to the
		# opaque theme default color, which isn't what we want.
		self.set_app_paintable(True)
		# The X server sends us an expose event when the window becomes
		# visible on screen. It means we need to draw the contents.	On a
		# composited desktop expose is normally only sent when the window
		# is put on the screen. On a non-composited desktop it can be
		# sent whenever the window is uncovered by another.
		#
		# The screen-changed event means the display to which we are
		# drawing changed. GTK+ supports migration of running
		# applications between X servers, which might not support the
		# same features, so we need to check each time.		 
		self.connect('expose-event', self.expose)
		self.connect('screen-changed', self.screen_changed)
		# toggle title bar on click - we add the mask to tell 
		# X we are interested in this event
		self.set_decorated(False)
		self.add_events(gdk.BUTTON_PRESS_MASK)
		self.connect('button-press-event', self.clicked)

		self.supports_alpha = False
		
		# initialize for the current display
		self.screen_changed(self)

		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		self.textview = gtk.TextView()
		self.textview.set_wrap_mode(gtk.WRAP_WORD)
		self.textview.set_editable(False)
		self.textbuffer = self.textview.get_buffer()
		sw.add(self.textview)

		# to make it transparent:
		# 1 - be called when the textview widget gets realized:
		#      textview.connect("expose-event", textview_expose)
		self.textview.connect("expose-event", self.textview_expose)
		# 2 - in the expose callback, get the window corresponding to the drawing:
		#      textview_window = textview.get_window(gtk.TEXT_WINDOW_WIDGET) or
		#      textview_window = textview.get_window(gtk.TEXT_WINDOW_TEXT)
		# 3 - use cairo (like in expose) to draw the background of the gdk.Window

		self.add(sw)
		self.show_all()

	def clicked(self, widget, event):
			# toggle window manager frames
			widget.set_decorated(not widget.get_decorated())

	# This is called when we need to draw the windows contents
	def expose(self, widget, event):
		cr = widget.window.cairo_create()

		if self.supports_alpha == True:
				cr.set_source_rgba(1.0, 1.0, 0.0, 0.2) # Transparent
		else:
				cr.set_source_rgb(1.0, 1.0, 0.0) # Opaque yellow

		# Draw the background
		cr.set_operator(cairo.OPERATOR_SOURCE)
		cr.paint()

		return False

	# This is called when we need to draw the windows contents
	def textview_expose(self, widget, event):
		# print "-- GTG applet -- textview_expose called --"
		self.textview_window_text = self.textview.get_window(gtk.TEXT_WINDOW_TEXT)
		cr = self.textview_window_text.cairo_create()

		if self.supports_alpha == True:
				cr.set_source_rgba(1.0, 1.0, 0.0, 0.5) # Yellow Transparent
		else:
				cr.set_source_rgb(1.0, 1.0, 0.0) # Opaque yellow

		# Draw the background
		cr.set_operator(cairo.OPERATOR_SOURCE)
		cr.paint()

		return False

	def screen_changed(self, widget, old_screen=None):
			
			# To check if the display supports alpha channels, get the colormap
			screen = widget.get_screen()
			colormap = screen.get_rgba_colormap()
			if colormap == None:
					print('Your screen does not support alpha channels!')
					colormap = screen.get_rgb_colormap()
					self.supports_alpha = False
			else:
					print('Your screen supports alpha channels!')
					self.supports_alpha = True
			
			# Now we have a colormap appropriate for the screen, use it
			widget.set_colormap(colormap)
			
			return False
	
	def set_text(self,task_text):
		self.textbuffer.set_text(task_text)
