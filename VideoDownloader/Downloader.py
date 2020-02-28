#!/usr/bin/python

# This is a part of the external applets for Cairo-Dock
# Copyright : (C) 2017 by Fabounet
# E-mail : fabounet@glx-dock.org
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
#

####################
### dependancies ###
####################
from __future__ import print_function  # must be on the first line
from CDApplet import CDApplet, _

import os
import subprocess
import threading
import re

########################
### Downloader class ###
########################
class Downloader():
	def __init__(self, url, id, applet, dl_list):
		self.url      = url
		self.id       = id
		self.title    = ''
		self.filename = ''
		self.thread   = None
		self.process  = None
		self.progress = 0.0
		self.size     = ''
		self.cancelled= False
		self.applet   = applet
		self.dl_list  = dl_list
	
	def set_label(self):
		if self.title:
			if self.size:
				self.applet.icon.SetLabel((_("downloading %s") % self.title) + ("(%s)" % self.size))
			else:
				self.applet.icon.SetLabel(_("downloading %s") % self.title)
	
	def set_progress(self):
		self.applet.icon.RenderValues([self.progress])
		self.applet.icon.SetQuickInfo("%d%%" % int(self.progress*100))
	
	def init(self):
		if self.title and self.filename:
			print ("title and filename already known")
			return
		# give the user an immediate feedback by making the icon "busy", the time we get the title
		self.applet.icon.Animate('busy',99)
		
		# get the title, and display it
		p = subprocess.Popen([self.applet.cShareDataDir+"/youtube-dl","--get-title","--get-filename","-o",self.applet.config['option_naming'],self.url],
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			shell=False)
		title_name, errors = p.communicate()
		title_name=title_name.rstrip()
		title_name_s = title_name.split("\n")
		if len(title_name_s) < 2:
			# failed, do something ...
			print ("couldn't retrieve info")
			pass
		self.title = title_name_s[0]
		self.filename = title_name_s[1]
		print ("downloading %s into %s" % (self.title, self.filename))
		self.set_label()
		
	def start(self):
		if self.thread:
			print ("thread already running")
			return
		# launch the download in a new process
		options = self.applet.config['option_download'].split(' ')
		self.process = subprocess.Popen([self.applet.cShareDataDir+"/youtube-dl","--newline"] + options + ["-o",self.applet.config['option_naming'],self.url],
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			shell=False)
		# download video in a new thread
		self.thread = threading.Thread(target=self.download_url_thread)
		self.thread.start()
		
	def cancel(self):
		self.cancelled = True  # mark the Downloader as 'cancelled', so that it knows it was intentional
		p = self.process
		if p:
			p.terminate()  # send a SIGTERM; the thread will terminate by itself
			p.wait()  # avoid zombi (might result in a lock if the process doesn't terminate; use 'poll' in that case)
	
	def restart(self):
		self.cancelled = False
		self.set_label()
		self.start()
	
	def download_url_thread(self):
		url = self.url
		id = self.id
		p = self.process
		
		# prepare the display of progress on the icon
		self.applet.icon.Animate('',0)  # stop the "busy" animation
		self.applet.icon.AddDataRenderer("progressbar", 1, "")  # set a "progressbar" renderer for 1 value
		self.set_progress()  # display something immediately
		
		# read the output of the downloader to get the progress
		expr = re.compile(".* ([0-9\.,]*)% .*")
		for line in iter(p.stdout.readline,''):
			result = re.sub(expr, "\\1", line)  # extract the percentage
			if result != line:  # skip any other line
				self.progress = float(result)/100.
				# extract the size once and for all
				if not self.size:
					expr2 = re.compile(".* of ([^ ]*).*")
					size = re.sub(expr2, "\\1", line)
					if size != line:
						self.size = size.rstrip()
						self.set_label()
				if id == self.applet.current_id:  # our task is the most recent one
					self.set_progress()
				
		self.process = None  # process has finished
		self.thread = None
		
		# clean the icon
		if id == self.applet.current_id:
			# look for a running download
			new_current_id = 0
			for key, value in self.dl_list.iteritems():
				if value.process:  # this is a running download
					new_current_id = max(new_current_id, value.id)
			# make it the current one
			self.applet.current_id = new_current_id
			if new_current_id == 0:  # no other active tasks
				self.applet.icon.SetLabel(self.applet.config['original_name'])
				self.applet.icon.AddDataRenderer("", 0, "")  # remove the "progressbar" renderer
				self.applet.icon.SetQuickInfo('')  # remove quick-info
			else:
				downloader = self.dl_list[new_current_id]
				downloader.set_label()
				downloader.set_progress()
				
		# inform the user in a light way
		if not self.cancelled:
			if int(self.progress) == 1:  # 100% completed => success
				self.applet.icon.ShowDialog(_("Download finished"), 3)
			else:  # for instance wrong URL, or timeout before completion
				self.applet.icon.ShowDialog(_("Download failed"), 3)
			self.applet.icon.Animate('rotate',3)
		
