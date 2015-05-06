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

class Go:


    def __init__( self ):
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
            self.window.connect("destroy", Gtk.main_quit)



        self.button_play = self.builder.get_object("play")
        self.button_mode = self.builder.get_object("mode")
        self.button_stop = self.builder.get_object("stop")
        self.label = self.builder.get_object("label")
        self.m_label = self.builder.get_object("m_label")
        
        self.button_play.connect("clicked", self._cb_play, "play")
        self.button_mode.connect("clicked", self._callback, "mode")
        self.button_stop.connect("clicked", self._cb_stop)

        dic = { 
            "on_buttonQuit_clicked" : self.quit,
        }
        
        self.builder.connect_signals( dic )
        self.proc_grab = None
        self.proc_daem = None

    def _cb_stop( self, button):
        print "Stop was clicked"
        cmd = "ps aux|grep calibra|awk '{print $2}'|xargs kill -9"
        print cmd
#        process = Popen(cmd , stdout=sys.stdout , stderr=sys.stderr , shell=True)
        cmd = "ps aux|grep acquisition|awk '{print $2}'|xargs kill -9"
        print cmd
#        process = Popen(cmd , stdout=sys.stdout , stderr=sys.stderr , shell=True)
        cmd = 'darcmagic stop -c  --prefix=all'
        print cmd
#        process = Popen(cmd , stdout=sys.stdout , stderr=sys.stderr , shell=True)
#        process.wait()


    def _cb_play(self, widget, data=None):
        print "%s: %s" % (data, ("disconnecting", "connecting")[widget.get_active()])
        image=Gtk.Image()
        if widget.get_active() is True:
            image.set_from_stock(Gtk.STOCK_MEDIA_PAUSE, Gtk.IconSize.BUTTON)
            self.button_play.set_image(image)
            self.button_play.set_label("Pause")
        else:
            image.set_from_stock(Gtk.STOCK_MEDIA_PLAY, Gtk.IconSize.BUTTON)
            self.button_play.set_image(image)
            self.button_play.set_label("Play")

        if self.label.get_text() == 'Calibration' and widget.get_active():
            try:
                self.DarcAravis = DarcAravis()
                self.darc_running = True
            except:
                pass

            if not self.darc_running:
                #
                # START DARC
                #
                cmd = 'darccontrol -o %s --prefix=%s' % (self.config.get('bbb','cfgdarcCAL'), 'all')#self.DarcAravis.get_darc_prefix())
                print cmd
                process = Popen(cmd , stdout=sys.stdout , stderr=sys.stderr , shell=True)
                print cmd
                time.time(30)
                cmd = 'python %s' % (self.config.get('bbb','calGUI'))
                print cmd
                process = Popen(cmd , stdout=sys.stdout , stderr=sys.stderr , shell=True)
            else:
                time.time(30)
                cmd = 'python %s' % (self.config.get('bbb','calGUI'))
                print cmd
                process = Popen(cmd , stdout=sys.stdout , stderr=sys.stderr , shell=True)
                    
        if self.label.get_text() == 'Adquisition' and widget.get_active():
            if self.darc_running:
                cmd = 'darcmagic stop -c  --prefix=%s' % (self.DarcAravis.get_darc_prefix())
                print cmd
                process = Popen(cmd , stdout=sys.stdout , stderr=sys.stderr , shell=True)
                process.wait()

                cmd = "ps aux|grep Calibra|awk '{print $2}'|xargs kill -9"
                print cmd
                process = Popen(cmd , stdout=sys.stdout , stderr=sys.stderr , shell=True)

                cmd = 'darccontrol -o %s --prefix=%s' % (self.config.get('bbb','cfgdarcACQ'), self.DarcAravis.get_darc_prefix())
                print cmd
                process = Popen(cmd , stdout=sys.stdout , stderr=sys.stderr , shell=True)
                #
                time.sleep(30)
                cmd = "python %s" % (self.config.get('bbb','acqGUI'))
                print cmd
                process = Popen(cmd , stdout=sys.stdout , stderr=sys.stderr , shell=True)

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
#                    self.DarcAravis.get(i, 'OffsetX') 
#                    self.DarcAravis.get(i, 'OffsetY') 
#                    self.DarcAravis.get(i, 'ExposureTimeAbs')
#                    self.DarcAravis.get(i, 'TriggerSource') 
                    print "\nSET configuration readed from file, for  %s" % camera
#                    self.DarcAravis.set(i, 'OffsetX', offset_x) 
#                    self.DarcAravis.set(i, 'OffsetY', offset_y) 
#                    self.DarcAravis.set(i, 'ExposureTimeAbs', exptime)
#                    if trigger.__contains__('True'):
#                        value = 'Line1'
#                    else:
#                        value = 'Freerun'
#                    self.DarcAravis.set(i, 'TriggerSource', value) 
                    #
                    # Seting up BBB
                    # 
                    freq = self.config.get('bbb', 'frequency')
                    os.system('/bin/set_frecuency %s' % freq)
                    #
                    #
                    #

                    cmd = "python %s -d %s -t %s" %  (self.config.get('bbb','daemon'), self.config.get('bbb','storepath'), 60) #XXX: to be fixed !!!
                    print cmd
                    cmd = "python %s -d %s -t %s" %  (self.config.get('bbb','capture'), self.config.get('bbb','storepath'), 60) #XXX time to be fixed !!
                    print cmd


    def _callback(self, widget, data=None):
        '''
        callback
        '''
        print "%s: %s" % (data, ("disconnecting", "connecting")[widget.get_active()])
        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_MEDIA_PLAY, Gtk.IconSize.BUTTON)
        self.button_play.set_image(image)
        self.button_play.set_label("Play")
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
