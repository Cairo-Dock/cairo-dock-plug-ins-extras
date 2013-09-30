#!/usr/bin/python

# This is a part of the external Moon applet for Cairo-Dock
#
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br

from __future__ import print_function

DEBUG = False

def log (string):
    if DEBUG:
        print("[+] Moon: %s" % string)
