#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="benjamin"
__date__ ="$Aug 23, 2011 12:18:24 PM$"

import gtk


class Menu(gtk.Menu):

    def __init__(self):
        gtk.Menu.__init__(self)


        # add menu item
        menu_item = gtk.MenuItem('test')
        self.append(menu_item)
        menu_item.show()

        self.show()
        



if __name__ == "__main__":
    print "Hello World";
