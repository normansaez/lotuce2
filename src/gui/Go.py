#!/usr/bin/env python
import os
import sys
import time
import signal
import ConfigParser

from multiprocessing import Process
from subprocess import Popen, PIPE

from gi.repository import Gtk
from gi.repository import GObject

from darcaravis import DarcAravis

#signal.signal(signal.SIGINT, receive_signal)

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
        self.button_mode = self.builder.get_object("mode")
        self.button_stop = self.builder.get_object("stop")
        self.label = self.builder.get_object("label")
        self.m_label = self.builder.get_object("m_label")
        
        self.button_play.connect("clicked", self._cb_play, "play")
        self.button_mode.connect("clicked", self._callback, "mode")
        self.button_stop.connect("clicked", self._cb_stop, "stop")

        dic = { 
            "on_buttonQuit_clicked" : self.quit,
        }
        
        self.builder.connect_signals( dic )
        self.proc_grab = None
        self.proc_daem = None

    def grab(self, cmd):
        process = Popen(cmd , stdout=PIPE , stderr=PIPE , shell=True)
        self.proc_grab = process
        process.wait()
    
    def daemon(self, cmd):
        process = Popen(cmd , stdout=PIPE , stderr=PIPE , shell=True)
        self.proc_daem = process
        process.wait()

    def _cb_stop( self, widget, data=None):
        print "%s: %s" % (data, ("disconnecting", "connecting")[widget.get_active()])
#        if widget.get_active() is True:

    def _cb_play(self, widget, data=None):
        print "%s: %s" % (data, ("disconnecting", "connecting")[widget.get_active()])
        image=Gtk.Image()
        if widget.get_active() is True:
            image.set_from_stock(Gtk.STOCK_MEDIA_PLAY, Gtk.IconSize.BUTTON)
            self.button_play.set_image(image)
            self.button_play.set_label("Play")
        else:
            image.set_from_stock(Gtk.STOCK_MEDIA_PAUSE, Gtk.IconSize.BUTTON)
            self.button_play.set_image(image)
            self.button_play.set_label("Pause")

        mode = self.label.get_text()
        if mode == 'Adquisition':
            print "adquire"
#                for i in range(0,4):
#                    camera = 'cam%d' % i
#                    print "\n\nReading configuration for %s ... " % camera
#                    offset_x = self.config.get(camera, 'offset_x')
#                    offset_y = self.config.get(camera, 'offset_y')
#                    trigger = self.config.get(camera, 'trigger')
#                    exptime = self.config.get(camera, 'exptime')
#                    print "OffsetX: %s" % offset_x 
#                    print "OffsetY: %s" % offset_y 
#                    print "Trigger: %s" % trigger
#                    print "exptime: %s" % exptime
#                    print "\nReading current configuration from HW : %s" % camera
#                    self.DarcAravis.get(i, 'OffsetX') 
#                    self.DarcAravis.get(i, 'OffsetY') 
#                    self.DarcAravis.get(i, 'ExposureTimeAbs')
#                    self.DarcAravis.get(i, 'TriggerSource') 
#                    print "\nSET configuration readed from file, for  %s" % camera
#                    self.DarcAravis.set(i, 'OffsetX', offset_x) 
#                    self.DarcAravis.set(i, 'OffsetY', offset_y) 
#                    self.DarcAravis.set(i, 'ExposureTimeAbs', exptime)
#                    if trigger.__contains__('True'):
#                        value = 'Line1'
#                    else:
#                        value = 'Freerun'
#                    self.DarcAravis.set(i, 'TriggerSource', value) 
#                #
#                # Seting up BBB
#                # 
#                import os
#                freq = self.config.get('bbb', 'frequency')
#                os.system('/bin/set_frecuency %s' % freq)
#                #
#                #
#                #
#                prefix =    self.config.get('bbb', 'prefix')
#                directory = self.config.get('bbb', 'image_path')
#                time = self.config.get('bbb', 'adquisition_time')
#                #
#                #
#                #
#                script = self.config.get('bbb', 'adquisition_script')
#                daemon = self.config.get('bbb', 'daemon')
#
#                cmd = "python %s -d %s -t %s" %  (script, directory, time)
#                proc_daemon = Process(target=self.daemon, args=(cmd,)) 
#                proc_daemon.start()
#
#                cmd = "python %s -d %s -t %s" %  (script, directory, time)
#                proc_grab = Process(target=self.grab, args=(cmd,)) 
#                proc_grab.start()
#                
#                self.proc_grab.join()
#                proc_grab.join()
#                if proc_grab.is_alive() is False:
#                    self.proc_daem.terminate()
#                    proc_daemon.terminate()

#            if data == "pause":
#                self.button_play.set_active(False)
#                self.proc_grab.terminate()
#                self.proc_daemon.terminate()
#                self.proc_daem.terminate()
            

    def _callback(self, widget, data=None):
        '''
        callback
        '''
        print "%s: %s" % (data, ("disconnecting", "connecting")[widget.get_active()])
        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_MEDIA_PAUSE, Gtk.IconSize.BUTTON)
        self.button_play.set_image(image)
        self.button_play.set_label("Pause")
        self.button_play.set_active(False)
        if self.button_mode.get_active():
            self.label.set_text("Adquisition")
            self.m_label.set_text("Push to change from\nAdquisition --> Calibration")
        if not self.button_mode.get_active():
            self.label.set_text("Calibration")
            self.m_label.set_text("Push to change from\nCalibration --> Adquisition")


    def quit(self, widget):
        '''
        quit
        '''
        sys.exit(0)

if __name__ == '__main__':

    Go = Go()
    Go.window.show()
    Gtk.main()
