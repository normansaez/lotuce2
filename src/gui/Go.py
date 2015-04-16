#!/usr/bin/env python
import os
import sys
from gi.repository import Gtk
from gi.repository import GObject

from darcaravis import DarcAravis

class Go:


    def __init__( self ):
        path, fil = os.path.split(os.path.abspath(__file__))

        self.builder = Gtk.Builder()
        self.builder.add_from_file(path+"/play.glade")
        self.window = self.builder.get_object ("window1")
        self.window.set_events(self.window.get_events())
        
        self.DarcAravis = DarcAravis()

        #step
        self.__step = 10

        if self.window:
            self.window.connect("destroy", Gtk.main_quit)



        #cross to put available offset
        # up = up
        # do = down
        # le = left
        # ri = right
        self.button_play = self.builder.get_object("play")
        self.button_pause = self.builder.get_object("pause")
        
        self.button_play.connect("clicked", self._callback, "play")
        self.button_pause.connect("clicked", self._callback, "pause")

        #apply_step

        dic = { 
            "on_buttonQuit_clicked" : self.quit,
        }
        
        self.builder.connect_signals( dic )

    def _callback(self, widget, data=None):
        '''
        callback
        '''
        print "%s: %s" % (data, ("disconnecting", "connecting")[widget.get_active()])
        #CONN
        if widget.get_active() is True:
            if data == "play":
                self.button_pause.set_active(False)

            if data == "pause":
                self.button_play.set_active(False)
            offset_y = self.DarcAravis.get(self.camera, 'OffsetY')
            self.offset_y.set_text("%d pixel(s)"% int(offset_y)) 
            offset_x = self.DarcAravis.get(self.camera, 'OffsetX')
            self.offset_x.set_text("%d pixel(s)"% int(offset_x))

    def quit(self, widget):
        '''
        quit
        '''
        sys.exit(0)

if __name__ == '__main__':

    Go = Go()
    Go.window.show()
    Gtk.main()
