#!/usr/bin/env python
import os
import sys
import time
import ConfigParser

from subprocess import Popen, PIPE

from gi.repository import Gtk
from gi.repository import GObject

from darcaravis import DarcAravis

class Go(GObject.GObject):
    def __init__(self):
        GObject.GObject.__init__(self)
        self.counter = 0
        GObject.timeout_add_seconds(1, self._cb_counter)

        path, fil = os.path.split(os.path.abspath(os.path.realpath(__file__)))
        self.builder = Gtk.Builder()
        self.builder.add_from_file(path+"/glade/Go.glade")
        self.window = self.builder.get_object ("window1")
        self.window.set_events(self.window.get_events())
        
        self.DarcAravis = None
        self.darc_running = False

        self.configfile=path+'/../../conf/config.cfg'
        self.config = None
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.configfile)

        if self.window:
            self.window.connect("destroy", self.quit)#Gtk.main_quit)

        self.button_play = self.builder.get_object("play")
        self.calibration = self.builder.get_object("calibration")
        self.acquisition = self.builder.get_object("acquisition")
       
        self.calibration.set_active(True)
        self.button_play.connect("clicked", self._cb_play, "play")
        self.calibration.connect("clicked", self._cb_check_cal, "calibration")
        self.acquisition.connect("clicked", self._cb_check_acq, "acquisition")

        dic = { 
            "on_buttonQuit_clicked" : self.quit,
        }
        
        self.builder.connect_signals( dic )
    def _cmd(self, cmd, wait=False):
        print cmd
        process = Popen(cmd , stdout=sys.stdout , stderr=sys.stderr , shell=True)
        if wait is True:
            process.wait()
        return

    def _darc_start(self, filename, prefix):
        try:
            self.DarcAravis = DarcAravis()
            self.darc_running = True
        except:
            print "DARC is already running"
        self.darc_running = False
        if not self.darc_running:
            cmd = 'darccontrol -o %s --prefix=%s' % (filename, prefix)
            self._cmd(cmd)
            time.sleep(20)

    def _darc_stop(self):
        cmd = "ps aux|grep Acquisition.py|awk '{print $2}'|xargs kill -9"
        self._cmd(cmd, wait=True)
        cmd = "ps aux|grep Calibra.py|awk '{print $2}'|xargs kill -9"
        self._cmd(cmd, wait=True)
        cmd = 'darcmagic stop -c  --prefix=all'
        self._cmd(cmd, wait=True)
        cmd = "ps aux|grep darcmain|awk '{print $2}'|xargs kill -9"
        self._cmd(cmd, wait=True)
        cmd = "ps aux|grep darccontrol|awk '{print $2}'|xargs kill -9"
        self._cmd(cmd, wait=True)

    def _darc_cal(self):
        print "Calibrating ..."
        cmd = "python %s" % (self.config.get('bbb','calGUI'))
        self._cmd(cmd)
        print "Seeting up ..."
        if self.DarcAravis is None:
            self.DarcAravis = DarcAravis()
        for i in range(0,4):
            camera = 'cam%d' % i
            print "\n\nReading configuration for %s ... " % camera
            trigger = self.config.get(camera, 'trigger')
            print "Trigger: %s" % trigger
            print "\nReading current configuration from HW : %s" % camera
            self.DarcAravis.get(i, 'TriggerSource') 
            print "\nSET configuration readed from file, for  %s" % camera
            if trigger.__contains__('True'):
                value = 'Line1'
            else:
                value = 'Freerun'
            self.DarcAravis.set(i, 'TriggerSource', value) 
        for i in range(0,4):
            camera = 'cam%d' % i
            exptime = self.config.get(camera, 'exptime')
            self.DarcAravis.set(i, 'ExposureTimeAbs', exptime)

    def _darc_acq(self):
        print "Acquiring ..."
        if self.DarcAravis is None:
            self.DarcAravis = DarcAravis()
        for i in range(0,4):
            camera = 'cam%d' % i
            print "\n\nReading configuration for %s ... " % camera
            offset_x = self.config.getint(camera, 'offset_x')
            offset_y = self.config.getint(camera, 'offset_y')
            trigger = self.config.get(camera, 'trigger')
            exptime = self.config.getint(camera, 'exptime')
            print "OffsetX: %d" % offset_x 
            print "OffsetY: %d" % offset_y 
            print "Trigger: %s" % trigger
            print "exptime: %d" % exptime
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
#            self.DarcAravis.set(i, 'TriggerSource', value) 
        freq = self.config.get('bbb', 'frequency')
        cmd = '/bin/set_frecuency %s' % freq
        self._cmd(cmd)
        cmd = "python %s" % (self.config.get('bbb','acqGUI'))
        self._cmd(cmd)

    def _cb_counter(self):
        self.counter += 1
        return True

    def _cb_play(self, widget, data=None):
        print "%s: %s" % (data, ("STOP", "PLAY")[widget.get_active()])
        image=Gtk.Image()
        #This happend when PLAY is pressed
        if widget.get_active() is True:
            image.set_from_stock(Gtk.STOCK_MEDIA_STOP, Gtk.IconSize.BUTTON)
            self.button_play.set_image(image)
            self.button_play.set_label("Stop")
            self.calibration.set_sensitive(False)
            self.acquisition.set_sensitive(False)
            if self.calibration.get_active() is True:
                filename = self.config.get('bbb','cfgdarcCAL')
                prefix   = self.config.get('bbb','prefix')
                self._darc_start(filename, prefix)
                self._darc_cal()
            if self.acquisition.get_active() is True:
                filename = self.config.get('bbb','cfgdarcACQ')
                prefix   = self.config.get('bbb','prefix')
                self._darc_start(filename, prefix)
                self._darc_acq()
        else:
            #This happend when STOP is pressed
            image.set_from_stock(Gtk.STOCK_MEDIA_PLAY, Gtk.IconSize.BUTTON)
            self.button_play.set_image(image)
            self.button_play.set_label("Play")
            self._darc_stop()
            self.calibration.set_sensitive(True)
            self.acquisition.set_sensitive(True)
            
    def _cb_check_cal(self, widget, data=None):
        self.calibration.set_active(True)
        if self.acquisition.get_active() is True:
            self.acquisition.set_active(False)

    def _cb_check_acq(self, widget, data=None):
        self.acquisition.set_active(True)
        if self.calibration.get_active() is True:
            self.calibration.set_active(False)
        
    def quit(self, widget):
        '''
        quit
        '''
        self._darc_stop()
        sys.exit(0)

if __name__ == '__main__':

    Go = Go()
    Go.window.show()
    Gtk.main()
