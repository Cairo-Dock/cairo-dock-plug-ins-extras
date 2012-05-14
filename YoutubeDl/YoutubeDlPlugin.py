# -*- coding: utf-8 -*-

# YoutubeDl, plugin for Cairo-Dock. Download videos from Youtube.
# Copyright 2012 Brian Whitelock
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from CairoDockPlugin import CairoDockPlugin
import gobject
from Configuration import Configuration
from CDApplet import CDApplet, _
import os, subprocess
import multiprocessing, Queue, random

# if pynotify is available use it otherwise use popup messages.
import userAlerts as alerts

# if tkinter is available use it otherwise use popup messages.
import fileDialogs as dialogs

# all constant types are placed in one file and used as needed.
from constantTypes import PopupTypes
from constantTypes import menuEntries

# import the help messages used in the right click context menu
from helpInfo import helpMessages

class YoutubeDlPlugin(CairoDockPlugin):

	def __init__(self, work_queue, result_queue):
		super(YoutubeDlPlugin, self).__init__()
		self.__interval = 60000 # 1 minute (in millisecondes)
		self.__config = Configuration(self.name())
		self.__timerId = None
                self.work_queue = work_queue
                self.result_queue = result_queue
                self.result = ['Idle','Idle','Idle','Idle']
                self.activeDownload = False
                self.urlList = list()
                self.currentDialog = PopupTypes.infoDialog
                self.resultSummary = 'No Data'
                self.listAltered = False


        def begin(self):

            """
                First method ran by CairoDock when applet is launched.
            """
            if self.__showProgressOnIcon:
	        self.setQuickInfo(str(self.result[0]))
            else:
	        self.setQuickInfo('')
            if self.__showStatusOnIcon:
                self.setLabel(self.resultSummary)
	    self.__setTimer()
	
	def onClick(self, iState):

		super(YoutubeDlPlugin, self).onClick(iState)
                tempString = '          Current Download;'
                if self.activeDownload:
                    tempString = tempString + '\n      -> '.join(self.urlList[0]) + ';'
                    rangeStart = 1
                else:
                    tempString = tempString + '    -> None;'
                    rangeStart = 0
                tempString = tempString + '\n          Current URL List;'
                if len(self.urlList) > 0:
                    tempList = list()
                    for item in range(rangeStart,len(self.urlList)):
                        #tempList.append('\n      -> '.join(self.urlList[item]))
                        tempList.append('\n      -> '.join(self.urlList[item]))
                    self.messageDebug(tempString)
                    #tempString = tempString + '\n'.join(tempList)
                    tempString = tempString + ';'.join(tempList)
                    self.messageDebug(tempString)
                    self.messageDebug(tempString)
                else:
                    tempString = tempString + '    -> Empty'
                    self.messageDebug(tempString)
                self.PopupDialog( {"message" : "Youtube Download URL List",
                "buttons" : "ok",  
                "icon" : "gtk-stock-edit"},
                {"visible" : True,
                 "widget-type" : "list",
                 "multi-lines" : True,
                 "editable" : False,
                 "values" : tempString})
                self.currentDialog = PopupTypes.infoDialog
		return True

	def onMiddleClick(self):
		"""
		I set my icon always vissible flag
		"""
		super(YoutubeDlPlugin, self).onMiddleClick()
                if self.__actionOnMiddleClick == 'Open Video Folder':
                    subprocess.call(['xdg-open','/home/brian/Videos'], shell=False)
                else:
                    alerts.doUserAlert(self,self.resultSummary,4)
                    
                return True
	
	def onReload(self, bConfigHasChanged):
		"""
		Je recharge la configuration si besoin.
		"""
		super(YoutubeDlPlugin, self).onReload(bConfigHasChanged)
		if bConfigHasChanged:
			self.__setConfiguration()
                if self.__showStatusOnIcon:
                    self.setLabel(self.resultSummary)
                if self.__showProgressOnIcon:
	            self.setQuickInfo(str(self.result[0]))
                else:
	            self.setQuickInfo('')
	
	def doUpdate(self):
		"""
		Update the current status for downloads.
		"""
                if self.activeDownload:
                    self.messageDebug("doUpdate: active downloads is true")
                    try:
                        queueContents = self.result_queue.get_nowait()
                        if queueContents == 'DownloadComplete':
                            self.result = ['Idle','Idle','Idle','Idle']
		            #self.setQuickInfo(str(self.result[0]))
                            self.activeDownload = False
                            if self.__showAlertDownloadComplete:
                                #alerts.doUserAlert(self,"Download " + self.currentFilename + " is Complete",4)
                                alerts.doUserAlert(self,"Download " + self.urlList[0][1] + " is Complete",4)
                            #self.currentFilename = 'None'
                            del self.urlList[0]
                            self.messageDebug("doUpdate: result_queue reports DownloadComplete")
                            #del self.filenameList[0]
                        elif queueContents == 'DownloadAborted':
                            self.result = ['Idle','Idle','Idle','Idle']
		            #self.setQuickInfo(str(self.result[0]))
                            self.activeDownload = False
                            if self.__showAlertDownloadAbort:
                                #alerts.doUserAlert(self,"Download " + self.currentFilename + " has been aborted",4)
                                alerts.doUserAlert(self,"Download " + self.urlList[0][1] + " has been aborted",4)
                            #self.currentFilename = 'None'
                            del self.urlList[0]
                            #del self.filenameList[0]
                            self.messageDebug("the length of url list is: " + str(len(self.urlList)))
                            self.messageDebug("doUpdate: result_queue reports DownloadAborted")
                        else:
                            self.result = queueContents.split(';')
                            #self.resultSummary = "%s\n%s of %s @ %s eta: %s" % (self.currentFilename,self.result[0],self.result[1],self.result[2],self.result[3])
                            self.resultSummary = "%s\n%s of %s @ %s eta: %s" % (self.urlList[0][1],self.result[0],self.result[1],self.result[2],self.result[3])
		            #self.setQuickInfo(str(self.result[0]))
                            self.messageDebug("doUpdate: result summary:\n"+self.resultSummary)
                    except Queue.Empty:
                        self.result = ['Empty','Empty','Empty','Empty']
                        self.messageDebug("doUpdate: Queue is empty")
                else:
                    self.messageDebug("doUpdate: Active Downloads is false")
                    self.resultSummary = "No Active Downloads"
                    if (len(self.urlList) > 0):
                        self.messageDebug("doUpdate: "+str(len(self.urlList))+" tems in url list")
                        if self.__startDownloads:
                            self.messageDebug("doUpdate: start Downloads is true")
                            self.messageDebug("doUpdate: Start Download:\n"+self.urlList[0][0])
                            self.startDownload(self.urlList[0][0])
                        else:
                            self.messageDebug("doUpdate: start Downloads is false")
                    else:
                        self.listAltered = False
                if self.__showStatusOnIcon:
                    self.setLabel(self.resultSummary)
                #update the quickinfo on Icon
                if self.__showProgressOnIcon:
	            self.setQuickInfo(str(self.result[0]))
                #Reset timer after doing update
	        self.__setTimer()

        def onDropData(self,cReceivedData): 
                #self.urlList.append(cReceivedData)
                if self.__showAlertAddURL:
                    alerts.doUserAlert(self,"Added to queue list: "+cReceivedData,4)
                if (not self.activeDownload) and self.__startDownloads:
                    self.messageDebug("onDropData: download immediately:\n"+str(cReceivedData))
                    self.startDownload(cReceivedData)
                if cReceivedData.find('watch?v=') == (-1):
                    fileName = "no filename maybe it is a playlist"
                    self.messageDebug("onDropData: Found watch?v= in url")
                else:
                    self.messageDebug("onDropData: didn't find watch?v= in url")
                    p = subprocess.Popen(["./youtubedl.py","--get-filename","-itf","18",cReceivedData],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
                    fileName, errors = p.communicate()
                    fileName=fileName.rstrip()
                self.urlList.append([str(cReceivedData),fileName])
                #self.filenameList.append(fileName)
                self.messageDebug("onDropData: New URL List:\n"+str(self.urlList))
                self.listAltered = True

        def startDownload(self, url):
            try:
                self.work_queue.put(url)
                self.messageDebug("startDownload: put url on work queue:\n"+url)
                if self.__showAlertStartDownloads:
                    alerts.doUserAlert(self,"Starting Download: "+url,4)
                self.activeDownload = True
                self.result = ['Starting','Starting','Starting','Starting']
	        self.setQuickInfo(str(self.result[0]))
            except Queue.Full:
                self.messageDebug("startDownload: work queue is full:\n"+url)
                alerts.doUserAlert(self,"Can't Download: Queue is Full",4)

        def onBuildMenu(self):
            self.messageDebug("onBuildMenu: context menu called")
            items = []
            if self.activeDownload:
                items.append(
                {"label": "Abort current download",
                 "icon" : "gtk-cancel",
                 "id"   : menuEntries.abortDownload })
            if len(self.urlList) > 0:
                items.append(
                {"label": "Save current URL list", 
                 "icon" : "gtk-save",
                 "id"   : menuEntries.saveURLs })
                items.append(
                {"label": "Clear current URL list", 
                 "icon" : "gtk-delete",
                 "id"   : menuEntries.clearURLs })
            if len(self.urlList) == 0:
                items.append(
                {"label": "Load URL list from file", 
                 "icon" : "gtk-open", 
                 "id"   : menuEntries.loadURLs })
            if self.__startDownloads:
                items.append(
                {"label": "Pause Downloading", 
                 "icon" : "gtk-media-pause", 
                 "id"   : menuEntries.pauseDownload })
            else:
                items.append(
                {"label": "Enable Downloading", 
                 "icon" : "gtk-media-play", 
                 "id"   : menuEntries.enableDownload })
            items.append(
            {"type":1,
             "label": "Help Menu", 
             "menu":0,
             "icon" : "gtk-help", 
             "id"   : menuEntries.helpSubMenu })
            items.append(
            {"type":0,
             "label": "youtube-dl Help", 
             "menu":menuEntries.helpSubMenu,
             "icon" : "gtk-help", 
             "id"   : menuEntries.downloaderHelp })
            items.append(
            {"type":0,
             "label": "Applet Help", 
             "menu": menuEntries.helpSubMenu,
             "icon" : "gtk-help", 
             "id"   : menuEntries.pluginHelp })
            self.AddMenuItems(items)

        def onMenuSelect(self,iNumEntry):
            self.messageDebug("onSelectMenu: "+str(iNumEntry)+" selected")
            if iNumEntry == menuEntries.abortDownload:
                self.PopupDialog( {"message" : "Are you sure you want to cancel the current download?",  
             "buttons" : "ok;cancel",  
             "icon" : "gtk-cancel"},  
             {"visible" : True } )
                self.currentDialog = PopupTypes.confirmAbort
            elif iNumEntry == menuEntries.clearURLs:
                self.PopupDialog( {"message" : "Are you sure you want to clear the current URL list?",  
             "buttons" : "ok;cancel",  
             "icon" : "gtk-delete"},  
             {"visible" : True } )
                self.currentDialog = PopupTypes.delList
            elif iNumEntry == menuEntries.saveURLs:
                self.saveURLs()
            elif iNumEntry == menuEntries.loadURLs:
                self.loadURLs()
            elif iNumEntry == menuEntries.pauseDownload:
                self.__startDownloads = False
                message = "Downloading Paused"
                if self.activeDownload:
                    message = message+": Current download will complete. To stop it use the Download Abort"
                alerts.doUserAlert(self,message,5)
            elif iNumEntry == menuEntries.enableDownload:
                self.__startDownloads = True
                alerts.doUserAlert(self,"Downloading Enabled",5)
                if not (self.activeDownload):
                    if len(self.urlList) > 0:
                        self.startDownload(self.urlList[0][0])
                    else:
                        self.result = ['Enabling','Enabling','Enabling','Enabling']
	                self.setQuickInfo(str(self.result[0]))
            elif iNumEntry == menuEntries.downloaderHelp:
                helpMessage = helpMessages.downloaderHelp
                self.PopupDialog( {"message" :helpMessage,  
             "buttons" : "ok",  
             "icon" : "gtk-help"},  
             {"visible" : True } )
                self.currentDialog = PopupTypes.infoDialog
            elif iNumEntry == menuEntries.pluginHelp:
                helpMessage = helpMessages.pluginHelp
                self.PopupDialog( {"message" :helpMessage,  
             "buttons" : "ok",  
             "icon" : "gtk-help"},  
             {"visible" : True } )
                self.currentDialog = PopupTypes.infoDialog
            else:
                self.messageDebug("An unknown menu entry was received")

        def onAnswerDialog(self,button, userResponse): 
            if self.currentDialog == PopupTypes.confirmAbort:
                self.messageDebug("onAnswerDialog: confirm abort: "+str(button)+" "+str(userResponse))
                if button == 0:
                    self.work_queue.put('Abort')
                    self.result = ['Aborting','Aborting','Aborting','Aborting']
	            self.setQuickInfo(str(self.result[0]))
                    self.__startDownloads = False
            elif self.currentDialog == PopupTypes.delList:
                self.messageDebug("onAnswerDialog: confirm delete: "+str(button)+" "+str(userResponse))
                if button == 0:
                    del self.urlList[:]
            elif self.currentDialog == PopupTypes.saveListFilename:
                self.messageDebug("onAnswerDialog: save list filename: "+str(button)+" "+str(userResponse))
            elif self.currentDialog == PopupTypes.getListFilename:
                self.messageDebug("onAnswerDialog: get list filename: "+str(button)+" "+str(userResponse))
            elif self.currentDialog == PopupTypes.infoDialog:
                self.messageDebug("onAnswerDialog: info dialog : "+str(button)+" "+str(userResponse))
            elif self.currentDialog == PopupTypes.showUrlList:
                self.messageDebug("onAnswerDialog: showUrlList : "+str(button)+" "+str(userResponse))
            else:
                self.messageDebug("onAnswerDialog: Unknown dialog : "+str(button)+" "+str(userResponse))

            self.currentDialog = PopupTypes.infoDialog

        def saveURLs(self):
            fileName=dialogs.saveUrlFilename()
            if fileName == None:
                self.messageDebug("returned filename is None")
            elif len(fileName) > 0:
                self.messageDebug("returned filename is: "+fileName)
            else:
                self.messageDebug("returned filename is 0 ")
            if len(fileName) > 0:
                self.ShowDialog("Saving list",4)
                saveFile = open(fileName, 'w')
                for item in range(len(self.urlList)):
                    saveFile.write("{0}::{1}\n".format(self.urlList[item][0],self.urlList[item][1]))
                saveFile.close()
                self.listAltered = False

        def loadURLs(self):
            fileName=dialogs.openUrlFilename(self.__urlList_directory)
            if fileName == None:
                self.messageDebug("returned filename is None")
            elif len(fileName) > 0:
                del self.urlList[:]
                self.urlList = [line.strip().split('::') for line in open(fileName)]
                self.listAltered = False
                self.messageDebug("new list is: ")
                self.messageDebug(self.urlList)
            else:
                self.messageDebug("returned filename is 0 ")

	def __setConfiguration(self):
		"""
		I reload the configuration.
		"""
		self.__config.refresh()
		interval = int(self.__config.get('User Interface', 'interval'))
		self.__interval = interval * 1000 # convert in millisecondes.
		self.__setTimer()
		self.__startDownloads = self.__config.getboolean('User Interface', 'startDownloads')
		self.__showAlertStartDownloads = self.__config.getboolean('User Interface', 'showAlertStartDownloads')
		self.__showAlertDownloadComplete = self.__config.getboolean('User Interface', 'showAlertDownloadComplete')
		self.__showAlertDownloadAbort = self.__config.getboolean('User Interface', 'showAlertDownloadAbort')
		self.__showAlertAddURL = self.__config.getboolean('User Interface', 'showAlertAddURL')
		self.usePynotify = self.__config.getboolean('User Interface', 'usePynotify')
		self.__actionOnMiddleClick = self.__config.get('User Interface', 'actionOnMiddleClick')
		self.__showProgressOnIcon = self.__config.getboolean('User Interface', 'showProgressOnIcon')
		self.__showStatusOnIcon = self.__config.getboolean('User Interface', 'showStatusOnIcon')
		self.__videos_directory = self.__config.get('User Interface', 'videos_directory')
                if not self.__videos_directory:
                    self.__videos_directory = os.path.abspath(os.path.expanduser("~")+"/Videos")
		self.__urlList_directory = self.__config.get('User Interface', 'urlList_directory')
                if not self.__urlList_directory:
                    self.__urlList_directory = os.path.abspath('.')
                if self.__showProgressOnIcon:
	            self.setQuickInfo(str(self.result[0]))
	
	def __setTimer(self):
		"""
		I set the time between two checks.
		"""
		self.__removeTimer()
		self.__timerId = gobject.timeout_add(self.__interval, self.doUpdate)
		
	def __removeTimer(self):
		"""
		I properly remove the timer.
		"""
		if self.__timerId != None:
			gobject.source_remove(self.__timerId)

	def run(self):
		"""
		Call me when you are ready 'to launch' the plugin's loop.
		"""
		self.__setConfiguration()
		self.begin()
		super(YoutubeDlPlugin, self).run()
		self.__removeTimer()
