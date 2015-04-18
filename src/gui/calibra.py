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
#from gi.repository import GObject

from darcaravis import DarcAravis

#signal.signal(signal.SIGINT, receive_signal)

import numpy as np
import darc
import os
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

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
        data[4,:] = 1
        data[196,:] = 1
        data[:,24] = 1
        data[:,176] = 1
        d=darc.Control('all')
        #takes camera pixels (x,y)
        pxlx =d.Get("npxlx")[0]
        pxly =d.Get("npxly")[0]

        streamBlock = d.GetStreamBlock('%srtcPxlBuf'%'all',1)#,block=1,flysave=options.directory+'/img.fits')
        streams = streamBlock['%srtcPxlBuf'%'all']
        stream = streams[0]
        data = stream[0].reshape((4*pxly,pxlx))
        xi_cam0 = 0*pxly
        xf_cam0 = 1*pxly
        yi_cam0 = 0*pxlx
        yf_cam0 = 1*pxlx
    
        xi_cam1 = 1*pxly
        xf_cam1 = 2*pxly
        yi_cam1 = 0*pxlx
        yf_cam1 = 1*pxlx
    
        xi_cam2 = 2*pxly
        xf_cam2 = 3*pxly
        yi_cam2 = 0*pxlx
        yf_cam2 = 1*pxlx
    
        xi_cam3 = 3*pxly
        xf_cam3 = 4*pxly
        yi_cam3 = 0*pxlx
        yf_cam3 = 1*pxlx
    
        #data per camera:
        cam0 = data[xi_cam0:xf_cam0,yi_cam0:yf_cam0]
        cam1 = data[xi_cam1:xf_cam1,yi_cam1:yf_cam1]
        cam2 = data[xi_cam2:xf_cam2,yi_cam2:yf_cam2]
        cam3 = data[xi_cam3:xf_cam3,yi_cam3:yf_cam3]
        h, w = cam0.shape
        h = h - 100
        w = w - 100
        surface0 = cairo.ImageSurface.create_for_data(cam0, cairo.FORMAT_RGB24, w, h)
        surface1 = cairo.ImageSurface.create_for_data(cam1, cairo.FORMAT_RGB24, w, h)
        surface2 = cairo.ImageSurface.create_for_data(cam2, cairo.FORMAT_RGB24, w, h)
        surface3 = cairo.ImageSurface.create_for_data(cam3, cairo.FORMAT_RGB24, w, h)
#        cr = cairo.Context(surface)
        pb0 = Gdk.pixbuf_get_from_surface(surface0,0,0,w,h)
        pb1 = Gdk.pixbuf_get_from_surface(surface1,0,0,w,h)
        pb2 = Gdk.pixbuf_get_from_surface(surface2,0,0,w,h)
        pb3 = Gdk.pixbuf_get_from_surface(surface3,0,0,w,h)

        self.img_cam0.set_from_pixbuf(pb0)
        self.img_cam1.set_from_pixbuf(pb1)
        self.img_cam2.set_from_pixbuf(pb2)
        self.img_cam3.set_from_pixbuf(pb3)
        #new profile
        x = len(cam0)
        cam0_nx = np.array([])
        cam0_ny = np.array([])
        cam1_nx = np.array([])
        cam1_ny = np.array([])
        cam2_nx = np.array([])
        cam2_ny = np.array([])
        cam3_nx = np.array([])
        cam3_ny = np.array([])
        
        c0 = cam0.max()
        c1 = cam1.max()
        c2 = cam2.max()
        c3 = cam3.max()
        
        for i in range(0,x):
            cam0_nx = np.append(cam0_nx, cam0[i,].sum())
            cam0_ny = np.append(cam0_ny, cam0[:,i].sum())
            cam1_nx = np.append(cam1_nx, cam1[i,].sum())
            cam1_ny = np.append(cam1_ny, cam1[:,i].sum())
            cam2_nx = np.append(cam2_nx, cam2[i,].sum())
            cam2_ny = np.append(cam2_ny, cam2[:,i].sum())
            cam3_nx = np.append(cam3_nx, cam3[i,].sum())
            cam3_ny = np.append(cam3_ny, cam3[:,i].sum())
        axis = range(0,x)
        #normalize according cameras:
        int_max = 4095
        cam0_nx = cam0_nx/int_max
        cam0_ny = cam0_ny/int_max
        
        cam1_nx = cam1_nx/int_max
        cam1_ny = cam1_ny/int_max
        
        cam2_nx = cam2_nx/int_max
        cam2_ny = cam2_ny/int_max
        
        cam3_nx = cam3_nx/int_max
        cam3_ny = cam3_ny/int_max
        
        #cam0_fx = Figure(figsize=(5,4), dpi=30)
        cam0_fx = Figure(dpi=30, tight_layout=True)
        ax = cam0_fx.add_subplot(111)
        #ax.set_xlim(0,1)
        ax.set_ylim(0,x)
        ax.invert_xaxis()
        ax.plot(cam0_nx,axis,'-')
        #mu, std = norm.fit(cam0_nx)
        #p = norm.pdf(axis, mu, std)
        #ax.plot(axis, p, 'k', linewidth=2)
        
        #cam0_fy = Figure(figsize=(5,4), dpi=30)
        cam0_fy = Figure(dpi=30, tight_layout=True)
        ax2 = cam0_fy.add_subplot(111)
        ax2.set_xlim(0,x)
        #ax2.set_ylim(0,1)
        ax2.plot(axis,cam0_ny,'-')
        #--------------------------------------------------
        #cam1_fx = Figure(figsize=(5,4), dpi=30)
        cam1_fx = Figure(dpi=30, tight_layout=True)
        ax = cam1_fx.add_subplot(111)
        #ax.set_xlim(0,1)
        ax.set_ylim(0,x)
        ax.plot(cam1_nx,axis,'-')
        
        #cam1_fy = Figure(figsize=(5,4), dpi=30)
        cam1_fy = Figure(dpi=30, tight_layout=True)
        ax2 = cam1_fy.add_subplot(111)
        ax2.set_xlim(0,x)
        #ax2.set_ylim(0,1)
        ax2.plot(axis,cam1_ny,'-')
        #--------------------------------------------------
        #cam2_fx = Figure(figsize=(5,4), dpi=30)
        cam2_fx = Figure(dpi=30, tight_layout=True)
        ax = cam2_fx.add_subplot(111)
        #ax.set_xlim(0,1)
        ax.set_ylim(0,x)
        ax.invert_xaxis()
        ax.plot(cam2_nx,axis,'-')
        
        #cam2_fy = Figure(figsize=(5,4), dpi=30)
        cam2_fy = Figure(dpi=30, tight_layout=True)
        ax2 = cam2_fy.add_subplot(111)
        ax2.set_xlim(0,x)
        #ax2.set_ylim(0,1)
        ax2.invert_yaxis()
        ax2.plot(axis,cam2_ny,'-')
        #--------------------------------------------------
        #cam3_fx = Figure(figsize=(5,4), dpi=30)
        cam3_fx = Figure(dpi=30, tight_layout=True)
        ax = cam3_fx.add_subplot(111)
        #ax.set_xlim(0,1)
        ax.set_ylim(0,x)
        ax.plot(cam3_nx,axis,'-')
        
        #cam3_fy = Figure(figsize=(5,4), dpi=30)
        cam3_fy = Figure(dpi=30, tight_layout=True)
        ax2 = cam3_fy.add_subplot(111)
        ax2.set_xlim(0,x)
        #ax2.set_ylim(0,1)
        ax2.invert_yaxis()
        ax2.plot(axis,cam3_ny,'-')
        plt.savefig("testfig.png")
        #--------------------------------------------------
        #fill up profiles
#        canvas_c0_fx = FigureCanvas(cam0_fx)  # a gtk.DrawingArea
#        canvas_c0_fy = FigureCanvas(cam0_fy)  # a gtk.DrawingArea
##        cam0_p_x.add(canvas_c0_fx)
##        cam0_p_y.add(canvas_c0_fy)
#        
#        canvas_c1_fx = FigureCanvas(cam1_fx)  # a gtk.DrawingArea
#        canvas_c1_fy = FigureCanvas(cam1_fy)  # a gtk.DrawingArea
##        cam1_p_x.add(canvas_c1_fx)
##        cam1_p_y.add(canvas_c1_fy)
#        
#        canvas_c2_fx = FigureCanvas(cam2_fx)  # a gtk.DrawingArea
#        canvas_c2_fy = FigureCanvas(cam2_fy)  # a gtk.DrawingArea
##        cam2_p_x.add(canvas_c2_fx)
##        cam2_p_y.add(canvas_c2_fy)
#        
#        canvas_c3_fx = FigureCanvas(cam3_fx)  # a gtk.DrawingArea
#        canvas_c3_fy = FigureCanvas(cam3_fy)  # a gtk.DrawingArea
##        cam3_p_x.add(canvas_c3_fx)
##        cam3_p_y.add(canvas_c3_fy)
#
        self.img_cam0_x.set_from_file("circle.png")
        self.img_cam1_x.set_from_file("circle.png")
        self.img_cam2_x.set_from_file("circle.png")
        self.img_cam3_x.set_from_file("circle.png")
        self.img_cam0_y.set_from_file("circle.png")
        self.img_cam1_y.set_from_file("circle.png")
        self.img_cam2_y.set_from_file("circle.png")
        self.img_cam3_y.set_from_file("circle.png")










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
