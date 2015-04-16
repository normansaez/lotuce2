#!/usr/bin/env python
import os
import sys
from gi.repository import Gtk
from gi.repository import GObject

from darcaravis import DarcAravis

import ConfigParser
class Go:


    def __init__( self ):
        path, fil = os.path.split(os.path.abspath(__file__))

        self.builder = Gtk.Builder()
        self.builder.add_from_file(path+"/play.glade")
        self.window = self.builder.get_object ("window1")
        self.window.set_events(self.window.get_events())
        
        self.DarcAravis = DarcAravis()

        path, fil = os.path.split(os.path.abspath(__file__))
        self.configfile=path+'/../../conf/config.cfg'
        self.config = None
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.configfile)

        if self.window:
            self.window.connect("destroy", Gtk.main_quit)



        self.button_play = self.builder.get_object("play")
        self.button_pause = self.builder.get_object("pause")
        
        self.button_play.connect("clicked", self._callback, "play")
        self.button_pause.connect("clicked", self._callback, "pause")

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
                for i in range(0,4):
                    camera = 'cam%d' % i
                    print "\n\nReading configuration for %s ... " % camera
        #            pxlx = self.config.get(camera, 'pxlx')
        #            pxly = self.config.get(camera, 'pxly')
                    offset_x = self.config.get(camera, 'offset_x')
                    offset_y = self.config.get(camera, 'offset_y')
                    trigger = self.config.get(camera, 'trigger')
                    exptime = self.config.get(camera, 'exptime')
        #            print pxlx
        #            print pxly
                    print "OffsetX: %s" % offset_x 
                    print "OffsetY: %s" % offset_y 
                    print "Trigger: %s" % trigger
                    print "exptime: %s" % exptime
                    print "\nReading current configuration from HW : %s" % camera
                    self.DarcAravis.get(i, 'OffsetX') 
                    self.DarcAravis.get(i, 'OffsetY') 
                    self.DarcAravis.get(i, 'ExposureTimeAbs')
                    self.DarcAravis.get(i, 'TriggerSource') 
                    print "\nSET configuration readed from file, for  %s" % camera
                    self.DarcAravis.set(i, 'OffsetX', offset_x) 
                    self.DarcAravis.set(i, 'OffsetY', offset_y) 
                    self.DarcAravis.set(i, 'ExposureTimeAbs', exptime)
                    if trigger.__contains__('True'):
                        value = 'Line1'
                    else:
                        value = 'Freerun'
                    self.DarcAravis.set(i, 'TriggerSource', value) 
                #
                # Seting up BBB
                # 
                import os
                freq = self.config.get('bbb', 'frequency')
                os.system('/bin/set_frecuency %s' % freq)
                #
                #
                #
                prefix =    self.config.get('bbb', 'prefix')
                directory = self.config.get('bbb', 'image_path')
                time = self.config.get('bbb', 'adquisition_time')
                script = self.config.get('bbb', 'adquisition_script')
                os.system('python %s -d %s -t %s' % (script, directory, time))
            if data == "pause":
                self.button_play.set_active(False)

    def quit(self, widget):
        '''
        quit
        '''
        sys.exit(0)

if __name__ == '__main__':

    Go = Go()
    Go.window.show()
    Gtk.main()
