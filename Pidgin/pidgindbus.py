#!/usr/bin/python

# This is a part of the external applet Pidgin-dock for Cairo-Dock
#
# Copyright : (C) 2009 by darvin
# E-mail : nbdarvin@gmail.com
# www: http://code.google.com/p/pidgin-cairo-dock 
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


import gobject
import os, sys, dbus
from dbus.mainloop.glib import DBusGMainLoop


def MessageRecieve(**args):
    print "flap,hi!!!!"
    print args
    print ">>>>>>message from %s, '%s', total unread messages: %d" %(args['sender'], args['message'], \
                args['unread'][0])

def StatusChanged(**args):
    print ">>status changed"
    print args
    print "new status: %s %s %s" % STATUS_TYPES[p.GetStatus()]


def MessageReaded(**args):
    print ">>Message readed!"
    print args

def Connecting(**args):
    print ">>Connecting!"

    print args


"""constants:"""
if __name__ == '__main__':
    STATUS_TYPES =(('__this status not exist__', 'This icon do not exist', 'This icon do not exist'), \
                ('offline', 'Asleep.png', 'This icon do not exist'), \
                ('online', 'Awake.png', 'Flap.png'), \
                ('unavailable', 'Invisible.png', 'InvisibleFlap.png'), \
                ('invisible', 'Invisible.png', 'InvisibleFlap.png'), \
                ('away', 'Invisible.png', 'InvisibleFlap.png'), \
                ('extended away', 'Invisible.png', 'InvisibleFlap.png'), \
                ('mobile', 'Awake.png', 'Flap.png'), \
                ('tune', 'Awake.png', 'Flap.png') )

class Pidgin(object):
    """Class to communicate pidgin"""
    STATUS={'_notconnected_':0,
                'offline':1,
                'online':2,
                'unavailable':3,
                'invisible':4,
                'away':5,
                'extended away':6,
                'mobile':7,
                'tune':8}
    def __init__(self, message_recieve_handler, status_changed_handler, message_readed_handler, connecting_handler, signed_on_handler):
        """message_recieve_handler is function, have args: sender, account, message, unread(tuple), status_changed_hanler - function with status arg"""
        bus = dbus.SessionBus()
        obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
        self.__purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")

        #add event handlers
        self.status_changed_handler = status_changed_handler
        bus.add_signal_receiver(self.on_savedstatus_changed,
                        dbus_interface="im.pidgin.purple.PurpleInterface",
                        signal_name="SavedstatusChanged")

        self.signed_on_handler = signed_on_handler
        bus.add_signal_receiver(self.on_signed_on,
                        dbus_interface="im.pidgin.purple.PurpleInterface",
                        signal_name="SignedOn")

        self.message_recieve_handler = message_recieve_handler
        bus.add_signal_receiver(self.on_received_im_msg,
                        dbus_interface="im.pidgin.purple.PurpleInterface",
                        signal_name="ReceivedImMsg")


        self.message_readed_handler = message_readed_handler
        bus.add_signal_receiver(self.on_message_readed,
                        dbus_interface="im.pidgin.purple.PurpleInterface",
                        signal_name="ConversationUpdated")

        self.connecting_handler = connecting_handler
        bus.add_signal_receiver(self.on_connecting,
                        dbus_interface="im.pidgin.purple.PurpleInterface",
                        signal_name="AccountConnecting")


    def on_savedstatus_changed(self, newstatus, oldstatus):
        #print self.__purple.PurpleSavedstatusGetType(newstatus)
        self.status_changed_handler()

    def on_signed_on(self, conn):
        self.signed_on_handler()

    def on_message_readed(self, conv, type):
        #print self.__purple.PurpleSavedstatusGetType(newstatus)
        self.message_readed_handler()

    def on_connecting(self, account):
        self.connecting_handler(account=account)

    def __detect_unread_conversations(self):
        purple = self.__purple
        im = True
        chat = True
        tooltip = ""
        blink = False
        allcount = 0
        conversations = []
        if im and chat:
            convs = purple.PurpleGetConversations()
        elif im:
            convs = purple.PurpleGetIms()
        elif chat:
            convs = purple.PurpleGetChats()
        else:
            convs = None
        for conv in convs:
            count = purple.PurpleConversationGetData(conv, "unseen-count")
            if count and count > 0:
                blink = True
                allcount += count
                conversations.append( {'name': purple.PurpleConversationGetName(conv),\
                        'count': count} )
                tooltip = tooltip + "\n" + purple.PurpleConversationGetName(conv) + " (" + str(count) + ")"
        text_representation = tooltip
        return (allcount, conversations,
            text_representation)

    def on_received_im_msg(self, account, sender, message, conversation, flags):
        #print sender, "said:", message
        self.message_recieve_handler(sender=sender, account=account, message=message, unread=self.__detect_unread_conversations())

    def GetStatus(self):
        """Gets current status"""
        status = self.__purple.PurpleSavedstatusGetCurrent()        # get current status
        status_type = self.__purple.PurpleSavedstatusGetType(status)    # get current status type
        return status_type

    def SetStatus(self, status):
        """Sets status, status must be status name"""
        st = self.__purple.PurpleSavedstatusGetCurrent()
        self.__purple.PurpleSavedstatusSetType(st, self.STATUS[status])
        self.__purple.PurpleSavedstatusActivate(st)

    def GetUnreadMessages(self):
        """Gets number of unread messages"""
        return self.__detect_unread_conversations()

    def GetUnreadMessagesNum(self):
        """Gets number of unread messages"""
        return self.__detect_unread_conversations()[0]



if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    p = Pidgin(MessageRecieve,StatusChanged, MessageReaded, Connecting, StatusChanged)
    print p.GetStatus()
    loop = gobject.MainLoop()
    loop.run()
