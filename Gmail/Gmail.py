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

from CDApplet import CDApplet, _

import glib # used for timer
import base64 # used to encrypt and decrypt messaging accounts' passwords
import urllib2 # used to connect to Gmail
import re # used to read Gmail headers at authentication
import libxml2 # used to parse XML content from Gmail inbox
import os # used to find paths and to launch 'aplay'
import sys # used to find relative paths
import webbrowser

import SVGmaker # home-made module to edit SVG counter emblem
import gtk # used for Menu class displaying inbox

class Menu(gtk.Menu):

    def __init__(self, inbox):
        gtk.Menu.__init__(self)

        # get all mail from inbox
        for mail in inbox:
            # check if mail has subject / title
            if len(mail['title']) == 0:
                mail['title'] = '<i>(No Subject)</i>'
            # create markups
            string = '<b>'+mail['author']+':</b>\n'+mail['title']
            menu_item = gtk.ImageMenuItem()
            # the true label is set after with set_markup()
            menu_item.set_label('')
            menu_item.set_image(gtk.image_new_from_file('./img/menu-gmail.png'))
            menu_item.get_children()[0].set_markup(string)
            menu_item.url = mail['link']
            menu_item.connect('activate', self.open_mail, mail)
            self.append(menu_item)
            menu_item.show()
            # add a separator if mail is not last in list
            if inbox.index(mail) != len(inbox) - 1:
                sep = gtk.SeparatorMenuItem()
                self.append(sep)
                sep.show()

        self.show()

    def open_mail(self, menu, mail=None):

        """ Opens the mail URL """
        try:
          link = mail['link']
          webbrowser.open(link)
        except webbrowser.Error:
          os.popen('x-www-browser https://mail.google.com/mail')

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
        self.subpath = self.path+'../../../.Gmail_subscription' # file containing Gmail account details
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
            message = _("There is no subscription to any Gmail account.")
            self.error(message)
            return

        # check if there was any data
        if len(sub) < 1:
            message = _("There is no subscription to any Gmail account.")
            self.error(message)
            return

        # if so process the data
        account = base64.b64decode(sub.strip('\n')).split('\n')

        # check if the data is correct
        if len(account) != 2:
            message = _("There is no subscription to any Gmail account.")
            self.error(message)
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
            message = _("Please, enter your Gmail username:")
            self.icon.PopupDialog({"message" : message, "buttons" : "ok;cancel"},
                    {"widget-type" : "text-entry"})
        # if requesting new password:
        elif request == 'password':
            # set dialogue flag to 'password'
            self.flag = 'password'
            # prompt for password
            message = _("Please, enter your Gmail password:")
            self.icon.PopupDialog({"message" : message, "buttons" : "ok;cancel"},
                    {"widget-type" : "text-entry", "visible" : False})
        # default request is to encrypt username and password
        else:
            # open, encode and write to subscription file
            file = open(self.subpath, 'w')
            file.write(base64.b64encode(str(self.account['username']+ \
            '\n'+self.account['password'])))
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

        # unpack and store XML
        xml = data.read()

        # reading inbox
        self.account['inbox'] = self.get_inbox(xml)

        # check if mail count could be retrieved
        if self.account['inbox'] == None:
            return True

        # parse inbox content to find number of new mails
        count = len(self.account['inbox'])

        # update account information
        self.account['diff'] = count - self.account['count']
        self.account['count'] = count

        # update display
        self.update_display()

        # send notifications if there is new mail
        if self.account['count'] > 0:
            self.send_alert()

        return True

    def get_inbox(self, xml_data):

        """
            Counts the unreade messages from the XML inbox content.
        """

        inbox = []

        try:
            tree = libxml2.parseDoc(xml_data)
            path = tree.xpathNewContext()
            path.xpathRegisterNs('purl', 'http://purl.org/atom/ns#')
            entries = path.xpathEval('//purl:entry')
            if len(entries) > 0:
                for entry in entries:
                    path.setContextNode(entry)
                    mail = {}
                    mail['title'] = path.xpathEval('purl:title')[0].content
                    mail['summary'] = path.xpathEval('purl:summary')[0].content
                    mail['link'] = path.xpathEval('purl:link')[0].prop('href')
                    mail['author'] = path.xpathEval('purl:author/purl:name')[0].content
                    inbox.append(mail)
            return inbox
        except:
            message = _("WARNING: there was an error reading XML content.")
            self.error(message)
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
            message = _("WARNING: Gmail applet failed to connect to Gmail atom feed.")
            self.error(message)
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
            message = _("WARNING: Gmail atom feed is badly formed: ")
            m = message + authline
            self.error(m)
            return None

        # check what scheme we have
        scheme = matchobject.group(1)
        if scheme.lower() != 'basic':
            message = _("WARNING: Gmail Applet is not equipped for authentication other than BASIC.")
            return self.error(message)

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
            message = _("WARNING: Gmail username or password may be wrong.")
            self.error(message)
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
            message = _("You have %s new email%s") % (str(self.account['count']), s)
            self.icon.ShowDialog(message, 3)

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

        # check user pressed the first button (OK) or Enter
        if key == 0 or key == CDApplet.DIALOG_KEY_ENTER:
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
                message = _("Sorry, there was no input!")
                self.error(message)

    def on_build_menu(self):

        """
            Appends items to right-click menu.
        """

        message_add_label = _("Add or change subscription")
        message_add_tooltip = _("Use this to add or change your Gmail account details.")
        message_middle_click = _("middle-click")
        message_check_label = _("Check inbox now")
        message_check_tooltip = _("Check Gmail inbox now if you can't wait.")
        self.icon.AddMenuItems([{"widget-type" : CDApplet.MENU_ENTRY,
        "label": message_add_label,
        "icon" : "gtk-add",
        "menu" : CDApplet.MAIN_MENU_ID,
        "id" : 1,
        "tooltip" : message_add_tooltip},
        {"widget-type" : CDApplet.MENU_ENTRY,
        "label": message_check_label + " (" + message_middle_click + ")",
        "icon" : "gtk-refresh",
        "menu" : CDApplet.MAIN_MENU_ID,
        "id" : 2,
        "tooltip" : message_check_tooltip}])

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
            m = Menu(self.account['inbox'])
            m.popup(parent_menu_shell=None, parent_menu_item=None, func=self.get_xy, data=(400, 400),
                    button=1, activate_time=0)

    def on_middle_click(self):
    
        """
            Check for new mails now.
        """
        
        self.check_mail()

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

if __name__ == "__main__":
    gmail = Gmail()
    gmail.run()
