#!/usr/bin/env python

# This is a part of the external applets for Cairo-Dock
# Copyright : (C) 2011 by Benjamin
# E-mail : jesuisbenjamin@gmail.com
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



from CDApplet import CDApplet

import glib # used for timer
import base64 # used to encrypt and decrypt messaging accounts' passwords
import urllib2 # used to connect to Gmail
import re # used to read Gmail headers at authentication
import libxml2 # used to parse XML content from Gmail inbox
import os # used to find paths and to launch 'aplay'
import sys # used to find relative paths

import SVGmaker # home-made module to edit SVG counter emblem

from menu import Menu # home-made module for left-click menu


class Gmail(CDApplet):

    """
        Main applet calling other agents to verify messages and sending signal
        to Cairo-Dock's icon.
    """

    def __init__(self):

        self.account = {} # accounts to which user subscribed
        self.config = {} # user configuration
        self.flag = None # used to check current status (especially with dialogues)
        self.path = sys.argv[3][0:-10] # relative path to config file's folder
        self.subpath = self.path+'subscription' # file containing Gmail account details
        self.svgpath = self.path+'emblem.svg' # SVG emblem file
        self.wav = os.path.abspath("./snd/pop.wav")
        self.rep = False # used not to run more than one loop
        CDApplet.__init__(self)


    def get_config(self, keyfile):
        
        """
            Gets configuration from configuration file.
        """

        self.config['notify'] = keyfile.getboolean('Configuration', 'NOTIFY')
        self.config['when'] = keyfile.get('Configuration', 'WHEN')
        self.config['anim'] = keyfile.getboolean('Configuration', 'ANIM')
        self.config['how'] = keyfile.get('Configuration', 'HOW')
        self.config['dia'] = keyfile.getboolean('Configuration', 'DIA')
        self.config['sound'] = keyfile.getboolean('Configuration', 'SOUND')
        self.config['update'] = keyfile.getint('Configuration', 'UPDATE') * 60000
        self.config['count'] = keyfile.getboolean('Configuration', 'COUNT')
        self.config['info'] = keyfile.get('Configuration', 'INFO')
        wav = keyfile.get('Configuration', 'WAV')
        # set default sound
        if len(wav) > 0:
            self.wav = os.path.abspath(wav)
        # set default animation
        if len(self.config['how']) == 0:
            self.config['how'] = 'default'

        # in case user switched between emblem/quickinfo while count > 0
        if self.account.get('count', 0) > 0:
            self.update_display()
        if self.flag == 'error':
            self.error('')

    def check_subscription(self):

        """
            Checks which accounts the user subsribed to, gets usernames and
            passwords as well as how often the account should be checked.
        """

        # reset flag in case of prior error:
        self.flag = None

        # open subscription file and read data
        try:
            file = open(self.subpath, 'r')
            sub = file.read()
            file.close()
        except:
            self.error("There is no subscription to any Gmail account.")
            return

        # check if there was any data
        if len(sub) < 1:
            self.error("There is no subscription to any Gmail account.")
            return

        # if so process the data
        account = base64.b64decode(sub.strip('\n')).split()

        # check if the data is correct
        if len(account) != 2:
            self.error("There is no subscription to any Gmail account.")
            return

        # then process the data into account
        self.account = {'username': account[0],
            'password': account[1],
            'count': 0,
            'diff': 0}

        if self.rep == True:
            pass
        else:
            self.check_mail()
            self.repeat()


    def add_subscription(self, request=None):

        """
            Prompts user to add subscription details.
        """

        # if requesting new username:
        if request == 'username':
            # set dialogue flag to 'username'
            self.flag = 'username'
            # prompt for username
            self.icon.PopupDialog({"message" : "Please, enter your Gmail username:", "buttons" : "ok;cancel"},
			{"widget-type" : "text-entry"})
        # if requesting new password:
        elif request == 'password':
            # set dialogue flag to 'password'
            self.flag = 'password'
            # prompt for password
            self.icon.PopupDialog({"message" : "Please, enter your Gmail password:", "buttons" : "ok;cancel"},
			{"widget-type" : "text-entry", "visible" : False})
        # default request is to encrypt username and password
        else:
            # open, encode and write to subscription file
            file = open(self.subpath, 'w')
            file.write(base64.b64encode(str(self.account['username']+ \
            ' '+self.account['password'])))
            file.close()
            # run subscription check as double check
            self.check_subscription()


    def check_mail(self):

        """
            Checks for new mail and requests notifications.
        """

        # fetch inbox content from Gmail
        data = self.request_gmail()

        # check if there is any content
        if data == None:
            return True

        # parse content to find number of new mails
        count = self.count_mail(data.read())

        # check if mail count could be retrieved
        if count == None:
            return True

        # update account information
        self.account['diff'] = count - self.account['count']
        self.account['count'] = count

        # update display
        self.update_display()

        # send notifications if there is new mail
        if self.account['count'] > 0:
            self.send_alert()

        return True


    def count_mail(self, xml_data):

        """
            Counts the "fullcount" value of the XML inbox content.
        """
        
        try:
            tree = libxml2.parseDoc(xml_data)
            path = tree.xpathNewContext()
            path.xpathRegisterNs('purl', 'http://purl.org/atom/ns#')
            return int(path.xpathEval('//purl:fullcount')[0].content)
        except:
            self.error("WARNING: there was an erro reading XML content.")
            return None

    def request_gmail(self):

        """
            Authenticates and requests inbox content from Gmail.
        """
        
        gmailfeed = 'https://mail.google.com/mail/feed/atom/'
        request = urllib2.Request(gmailfeed)

        # connect to Gmail
        try:
	    handle = urllib2.urlopen(request)
	except IOError, error:
	    # here we will need "fail" as we receive a 401 error to get access
	    pass

        if not hasattr(error, 'code') or error.code != 401:
	    # we got an error - but not a 401 error
	    self.error("WARNING: Gmail applet failed to connect to Gmail atom feed.")
            return None

        # get the www-authenticate line from the headers
        authline = error.headers['www-authenticate']

        # from this header we extract scheme and realm
        authobject = re.compile(
                                r'''(?:\s*www-authenticate\s*:)?\s*(\w*)\s+realm=['"]([^'"]+)['"]''',
                                re.IGNORECASE)
	matchobject = authobject.match(authline)

        # make sure scheme and realm was found
        if not matchobject:
	    m = "WARNING: Gmail atom feed is badly formed: " + authline
            self.error(m)
            return None

        # check what scheme we have
        scheme = matchobject.group(1)
        if scheme.lower() != 'basic':
	    return self.error('WARNING: Gmail Applet is not equiped for authentication \
        other than BASIC.')

        # authenticate and get inbox content
        username = self.account['username']
        password = self.account['password']
        base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
	authheader = "Basic %s" % base64string
	request.add_header("Authorization", authheader)
	try:
	    handle = urllib2.urlopen(request)
	except IOError, error:
	    # here we shouldn't fail if the username/password is right
	    self.error("WARNING: Gmail username or password may be wrong.")
            return None

        return handle


    def update_display(self):

        """
        Updates applet icon either with quickinfo or svg emblem.
        Only if new mail count is superior to 0.
        """
        
        # if user does not want any counter on the icon
        if self.config['count'] == False:
            # clean up quick-info
            self.icon.SetQuickInfo(format(''))
            # clean up icon
            self.icon.SetIcon(os.path.abspath('./icon'))
            return
        
        # otherwise
        if self.config['info'] == 'quickinfo':
            # clean up icon
            self.icon.SetIcon(os.path.abspath('./icon'))
            if self.account['count'] == 0:
                # reset quick-info
                self.icon.SetQuickInfo(format(''))
            else:
                self.icon.SetQuickInfo(format(self.account['count']))

        else:
            # reset quick-info (in case displayed before)
            self.icon.SetQuickInfo(format(''))
            # check if emblem is necessary
            if self.account['count'] == 0:
                # reset icon
                self.icon.SetIcon(os.path.abspath("./icon"))
            else:
                # get size out of config
                size = self.config['info'].split()[0]
                # make icon with external module SVGmaker
                SVG = SVGmaker.add_counter(self.account['count'], size)
                svg = open(self.svgpath, 'w')
                svg.write(SVG)
                svg.close()
                # set icon with emblem
                self.icon.SetIcon(self.svgpath)

    def error(self, message):

        """
            Warns the user if an error occured.
        """

        if self.config['info'] != 'quickinfo':
            # remove previous quickinfo if needed:
            self.icon.SetQuickInfo(format(''))
            # get size from config:
            size = self.config['info'].split()[0]
            # pass size to filename:
            file = './img/gmail-error-'+size+'.svg'
            # set icon with error emblem
            self.icon.SetIcon(os.path.abspath(file))

        else:
            # reset icon in case needed
            self.icon.SetIcon(os.path.abspath('./icon'))
            # set quickinfo:
            self.icon.SetQuickInfo(format('Error!'))
        # check if any error is already known
        # or if the user is changing subscription details
        if self.flag != None:
            return
        # set error flag
        self.flag = 'error'
        # show dialogue
        self.icon.ShowDialog(message, 4)
        

    def send_alert(self):
        
        """
            Notifies user according to requirements.
        """

        # check if user wants notifications
        if self.config['notify'] == False:
            return

        # check whether conditions are met
        if self.config['when'] == 'always':
            pass
        elif self.config['when'] == 'different' and self.account['diff'] != 0:
            pass
        elif self.config['when'] == 'superior' and self.account['diff'] > 0:
            pass
        else:
            return

        # check whether user wants an effect on the icon
        if self.config['anim'] == True:
            self.icon.DemandsAttention(True, self.config['how'])

        # check whether user wants a dialogue
        if self.config['dia'] == True:
            # checking our grammar ;)
            if self.account['count'] > 1:
                    s = 's'
            else:
                    s = ''
            self.icon.ShowDialog("You have "+str(self.account['count'])+" new email%s." % s, 3)

        # check whether user wants a sound
        if self.config['sound'] == True:
            try:
                os.popen('aplay ' + self.wav)
            except:
                # restore default sound file if custom is corrupted
                self.wav = os.path.abspath("./snd/pop.wav")


    def repeat(self):
        
        """
           Timer for postman to check messages.
           Will continue as long as check_messages returns True
        """

        # set flag to tell the loop is running
        self.rep = True
        # start timer loop
        glib.timeout_add(self.config['update'], self.check_mail)


    def begin(self):
        
        """
            First method ran by CairoDock when applet is launched.
        """

        self.icon.SetLabel("Gmail")
        # the applet will not enter the loop until a subscription is found
        self.check_subscription()
        

    def on_answer_dialog(self, key, content):

        """
            Processes dialogue input for username and password.
        """

        # check user pressed OK
        if key == 0 or key == -1:
            # check user entered something
            if len(content) > 0:
                # check if requesting username
                if self.flag == 'username':
                    # append account with username
                    self.account['username'] = format(content)
                    # request password
                    self.add_subscription('password')
                # check if requesting password
                elif self.flag == 'password':
                    # append account with password
                    self.account['password'] = format(content)
                    # finish up registration process
                    self.add_subscription()
                else:
                    # should not happen (kept in case another dialogue needs
                    # to be made in future).
                    pass
            else:
                self.error("Sorry, there was no input!")

    def on_build_menu(self):

        """
            Appends items to right-click menu.
        """

        self.icon.AddMenuItems([{"widget-type" : 0,
        "label": "Add or change subscription",
        "icon" : "gtk-add",
        "menu" : 1,
        "id" : 1,
        "tooltip" : "Use this to add or change your Gmail account details."},
        {"widget-type" : 0,
        "label": "Check inbox now",
        "icon" : "gtk-refresh",
        "menu" : 1,
        "id" : 2,
        "tooltip" : "Check Gmail inbox now if you can't wait."}])
        

    def on_menu_select(self, iNumEntry):

        """
            Launches methods according to menu selection.
        """

        if iNumEntry == 1:
            self.add_subscription('username')
        elif iNumEntry == 2:
            self.check_mail()
        else:
            #should not happen. Kept in case more menu-items need be appended.
            pass


    def on_click(self, iState):

        """
            Launches Gmail in default browser or application.
        """
        if self.account['count'] < 1:
            self.check_mail()
        else:
            os.popen('x-www-browser https://mail.google.com/mail')

if __name__ == "__main__":
    gmail = Gmail()
    gmail.run()