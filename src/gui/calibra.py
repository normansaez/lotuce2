#!/usr/bin/env python
import os
import sys
import time
import signal
import cairo
import ConfigParser

from multiprocessing import Process
from subprocess import Popen, PIPE

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

from darcaravis import DarcAravis

#signal.signal(signal.SIGINT, receive_signal)

import numpy as np

class Go:


    def __init__( self ):
        path, fil = os.path.split(os.path.abspath(os.path.realpath(__file__)))
        self.builder = Gtk.Builder()
        self.builder.add_from_file(path+"/calibra.glade")
        self.window = self.builder.get_object ("window1")
        self.window.set_events(self.window.get_events())
        
        self.DarcAravis = DarcAravis()

        self.configfile=path+'/../../conf/config.cfg'
        self.config = None
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.configfile)

        if self.window:
            self.window.connect("destroy", Gtk.main_quit)



        self.button_apply_subap = self.builder.get_object("apply_subap_button")
        self.button_apply_refresh = self.builder.get_object("refresh_button")
        self.button_apply_offset = self.builder.get_object("offset_step_button")

        self.entry_subap = self.builder.get_object("subap_size_entry")
        self.entry_refresh = self.builder.get_object("refresh_entry")
        self.entry_offset = self.builder.get_object("offset_step_entry")

        self.label_subap = self.builder.get_object("subap_label")
        self.label_refresh = self.builder.get_object("refresh_label")
        self.label_offset = self.builder.get_object("offset_step_label")
################ fully test
        self.img_cam0 = self.builder.get_object("image_cam0")
        self.img_cam1 = self.builder.get_object("image_cam1")
        self.img_cam2 = self.builder.get_object("image_cam2")
        self.img_cam3 = self.builder.get_object("image_cam3")
        self.img_cam0_x = self.builder.get_object("image_cam0_x")
        self.img_cam1_x = self.builder.get_object("image_cam1_x")
        self.img_cam2_x = self.builder.get_object("image_cam2_x")
        self.img_cam3_x = self.builder.get_object("image_cam3_x")
        self.img_cam0_y = self.builder.get_object("image_cam0_y")
        self.img_cam1_y = self.builder.get_object("image_cam1_y")
        self.img_cam2_y = self.builder.get_object("image_cam2_y")
        self.img_cam3_y = self.builder.get_object("image_cam3_y")
        #dummy data
        data = np.zeros(200*200).reshape(200,200)
        data[:,4] = 1
        data[:,196] = 1
        data[24,:] = 1
        data[176,:] = 1
        surface = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_RGB24, 200, 200)
#        cr = cairo.Context(surface)
        pb = Gdk.pixbuf_get_from_surface(surface,0,0,200,200)
        self.img_cam0_x.set_from_pixbuf(pb)
        self.img_cam1_x.set_from_pixbuf(pb)
        self.img_cam2_x.set_from_pixbuf(pb)
        self.img_cam3_x.set_from_pixbuf(pb)
        self.img_cam0_y.set_from_pixbuf(pb)
        self.img_cam1_y.set_from_pixbuf(pb)
        self.img_cam2_y.set_from_pixbuf(pb)
        self.img_cam3_y.set_from_pixbuf(pb)
        self.img_cam0.set_from_pixbuf(pb)
        self.img_cam1.set_from_pixbuf(pb)
        self.img_cam2.set_from_pixbuf(pb)
        self.img_cam3.set_from_pixbuf(pb)
################
#        self.button_apply_subap.connect("clicked", self._cb_subap, "subap")
#        self.button_apply_refresh.connect("clicked", self._cb_refresh, "refresh")
#        self.button_apply_offset.connect("clicked", self._cb_offset,"offset")
#
        dic = { 
            "on_buttonQuit_clicked" : self.quit,
        }
        
        self.builder.connect_signals( dic )
        self.proc_grab = None
        self.proc_daem = None

    def _cb_stop( self, button):
        print "Stop was clicked"

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
            print "Starting DARC from this GUI"
            #
            # START DARC
            #
            cmd = 'python /opt/darc/bin/darccontrol -o /home/lotuce2/lotuce2/conf/configMantaFULL.py --prefix=all'
            process = Popen(cmd , stdout=sys.stdout , stderr=sys.stderr , shell=True)
            #
            # Wait until DARC start, and then show GUI
            time.sleep(30)
            cmd = 'python /home/lotuce2/lotuce2/src/gui/lotuce2Commander.py'
            process = Popen(cmd , stdout=sys.stdout , stderr=sys.stderr , shell=True)
        else:
            cmd = 'darcmagic stop -c  --prefix=all'
            process = Popen(cmd , stdout=sys.stdout , stderr=sys.stderr , shell=True)
            process.wait()

        if self.label.get_text() == 'Adquisition' and widget.get_active():
            print "Parto Adquiero imagenes"

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
