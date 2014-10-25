#!/usr/bin/env python
import os
import sys
from gi.repository import Gtk
from gi.repository import GObject


class OffSetGui:


    def __init__( self ):
        path, fil = os.path.split(os.path.abspath(__file__))

        self.builder = Gtk.Builder()
        self.builder.add_from_file(path+"/offset.glade")
        self.window = self.builder.get_object ("window1")
        self.window.set_events(self.window.get_events())

        if self.window:
            self.window.connect("destroy", Gtk.main_quit)

        #Toggle button to connect to cam0
        self.togglebutton_cam0 = self.builder.get_object ("togglebutton0")
        self.togglebutton_cam0.connect("toggled", self.callback, "cam0")

        #Toggle button to connect to cam1
        self.togglebutton_cam1 = self.builder.get_object ("togglebutton1")
        self.togglebutton_cam1.connect("toggled", self.callback, "cam1")

        #Toggle button to connect to cam2
        self.togglebutton_cam2 = self.builder.get_object ("togglebutton2")
        self.togglebutton_cam2.connect("toggled", self.callback, "cam2")

        #Toggle button to connect to cam3
        self.togglebutton_cam3 = self.builder.get_object ("togglebutton3")
        self.togglebutton_cam3.connect("toggled", self.callback, "cam3")

        #cross to put available offset
        # up = up
        # do = down
        # le = left
        # ri = right
        self.button_up = self.builder.get_object("button_up")
        self.button_do = self.builder.get_object("button_do")
        self.button_le = self.builder.get_object("button_le")
        self.button_ri = self.builder.get_object("button_ri")
        
        self.button_up.connect("clicked", self.offset_callback, "up")
        self.button_do.connect("clicked", self.offset_callback, "do")
        self.button_le.connect("clicked", self.offset_callback, "le")
        self.button_ri.connect("clicked", self.offset_callback, "ri")

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
            print "cam0: %s" % self.togglebutton_cam0.get_active()
            print "cam1: %s" % self.togglebutton_cam1.get_active()
            print "cam2: %s" % self.togglebutton_cam2.get_active()
            print "cam3: %s" % self.togglebutton_cam3.get_active()
            if data == "cam0":
#                self.togglebutton_cam0.set_active(False)
                self.togglebutton_cam1.set_active(False)
                self.togglebutton_cam2.set_active(False)
                self.togglebutton_cam3.set_active(False)

            if data == "cam1":
                self.togglebutton_cam0.set_active(False)
#                self.togglebutton_cam1.set_active(False)
                self.togglebutton_cam2.set_active(False)
                self.togglebutton_cam3.set_active(False)

            if data == "cam2":
                self.togglebutton_cam0.set_active(False)
                self.togglebutton_cam1.set_active(False)
#                self.togglebutton_cam2.set_active(False)
                self.togglebutton_cam3.set_active(False)

            if data == "cam3":
                self.togglebutton_cam0.set_active(False)
                self.togglebutton_cam1.set_active(False)
                self.togglebutton_cam2.set_active(False)
#                self.togglebutton_cam3.set_active(False)

        if widget.get_active() is False:
            print "OFF"

    def offset_callback(self, widget, data=None):
        '''
        offset callback
        '''
        print "%s" % (data)

    def cmd_cam(self, cam):
        selector  = {"aravisCmd0":"cam0", "aravisCmd1":"cam1", "aravisCmd2":"cam2", "aravisCmd3":"cam3"}
    def quit(self, widget):
        sys.exit(0)

if __name__ == '__main__':
    import darc
#    d = darc.Control("both")

    OffSetGui = OffSetGui()
    OffSetGui.window.show()
    Gtk.main()
