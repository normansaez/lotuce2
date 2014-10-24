#!/usr/bin/env python
import os
import sys
#import pygtk  
#pygtk.require("2.0")  
#import gtk  
from gi.repository import Gtk
#from gi.repository import GObject


class BeagleDarcGui:


    def __init__( self ):
        path, fil = os.path.split(os.path.abspath(__file__))

        self.builder = Gtk.Builder()
        self.builder.add_from_file(path+"/offset.glade")
        self.window = self.builder.get_object ("window1")
        self.window.set_events(self.window.get_events())

        if self.window:
            self.window.connect("destroy", Gtk.main_quit)

        #Toggle button to connect to beaglebone
        self.connect_togglebutton = self.builder.get_object ("connect_togglebutton")
#        self.connect_togglebutton.connect("toggled", self.callback, "Connection")

        #default entries
        self.entry1 = self.builder.get_object("entry1")
        self.entry2 = self.builder.get_object("entry2")
        self.entry3 = self.builder.get_object("entry3")
        self.image4 = self.builder.get_object("image4")


        dic = { 
            "on_buttonQuit_clicked" : self.quit,
        }
        
        self.builder.connect_signals( dic )

    def callback(self, widget, data=None):
        '''
        callback
        '''
        print "%s: %s" % (data, ("disconnecting", "connecting")[widget.get_active()])
        #CONN
        if widget.get_active() is True:
            widget.set_label(gtk.STOCK_DISCONNECT)
            widget.set_use_stock(True)
            self.image4.set_from_stock(gtk.STOCK_CONNECT, gtk.ICON_SIZE_MENU)
            self.bds.ior = self.entry3.get_text()

        if widget.get_active() is False:
            widget.set_label(gtk.STOCK_CONNECT)
            widget.set_use_stock(True)
            self.image4.set_from_stock(gtk.STOCK_DISCONNECT, gtk.ICON_SIZE_MENU)

    def quit(self, widget):
        sys.exit(0)


BeagleDarcGui = BeagleDarcGui()
BeagleDarcGui.window.show()
Gtk.main()
