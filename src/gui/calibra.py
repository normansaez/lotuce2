#!/usr/bin/env python
import os
import sys
import time
import darc
import cairo
import signal
import ConfigParser

from multiprocessing import Process
from subprocess import Popen, PIPE
from pylab import imshow,show
from scipy import signal
from matplotlib.figure import Figure
from matplotlib.path import Path

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def get_square(cx, cy, side, color='red'):
    verts = [
        (cx-side, cy-side), # left, bottom
        (cx-side, cy+side), # left, top
        (cx+side, cy+side), # right, top
        (cx+side, cy-side), # right, bottom
        (cx, cy), # ignored
        ]
    
    codes = [Path.MOVETO,
             Path.LINETO,
             Path.LINETO,
             Path.LINETO,
             Path.CLOSEPOLY,
             ]
    
    path = Path(verts, codes)
    
    patch = patches.PathPatch(path, facecolor='none', EdgeColor=color, lw=1)
    return patch

def get_centroid(img, mask):
    correlation = signal.fftconvolve(img,mask,mode='same')
    #Getting max 
    cy, cx = np.unravel_index(correlation.argmax(),correlation.shape)
    return cy,cx

def get_mask_spot(radio=5, kernel=20):
    # syntetic img to be convolved
    y,x = np.ogrid[-kernel: kernel+1, -kernel: kernel+1]
    mask = x**2+y**2 <= np.pi*radio**2
    mask = mask*1
    return mask

class Go:


    def __init__( self ):
        path, fil = os.path.split(os.path.abspath(os.path.realpath(__file__)))
        self.builder = Gtk.Builder()
        self.builder.add_from_file(path+"/calibra.glade")
        self.window = self.builder.get_object ("window1")
        self.window.set_events(self.window.get_events())
        
#        self.DarcAravis = DarcAravis()

        self.configfile=path+'/../../conf/config.cfg'
        self.config = None
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.configfile)

        if self.window:
            self.window.connect("destroy", Gtk.main_quit)


        self.counter = 0
        GObject.timeout_add_seconds(30, self._cb_timeout)

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

#        weight = 120
        height = 30
        subap = 60
        radio = 5
        kernel = 20
        inchs = 2
        #get mask
        mask = get_mask_spot(radio,kernel)

        cy, cx = get_centroid(cam0, mask)
        
        plt.figure(1, frameon=False)
        patch = get_square(cx,cy,subap)
        plt.gca().add_patch(patch)
        patch = get_square(cx,cy,height,color='green')
        plt.gca().add_patch(patch)
        plt.gcf().set_size_inches(inchs,inchs)
        plt.Axes(plt.figure(1), [0., 0., 1., 1.])
        plt.gca().set_axis_off()
        imshow(cam0, aspect='normal', cmap = cm.Greys_r)
        plt.savefig("cam0.png")

        plt.figure(2, frameon=False)
        cy, cx = get_centroid(cam1, mask)
        patch = get_square(cx,cy,subap)
        plt.gca().add_patch(patch)
        patch = get_square(cx,cy,height,color='green')
        plt.gca().add_patch(patch)
        plt.Axes(plt.figure(2), [0., 0., 1., 1.])
        plt.gcf().set_size_inches(inchs,inchs)
        plt.gca().set_axis_off()
        imshow(cam1, aspect='normal', cmap = cm.Greys_r)
        plt.savefig("cam1.png")

        plt.figure(3, frameon=False)
        cy, cx = get_centroid(cam2, mask)
        patch = get_square(cx,cy,subap)
        plt.gca().add_patch(patch)
        patch = get_square(cx,cy,height,color='green')
        plt.gca().add_patch(patch)
        plt.Axes(plt.figure(3), [0., 0., 1., 1.])
        plt.gcf().set_size_inches(inchs,inchs)
        plt.gca().set_axis_off()
        imshow(cam2, aspect='normal', cmap = cm.Greys_r)
        plt.savefig("cam2.png")

        plt.figure(4, frameon=False)
        cy, cx = get_centroid(cam3, mask)
        patch = get_square(cx,cy,subap)
        plt.gca().add_patch(patch)
        patch = get_square(cx,cy,height,color='green')
        plt.gca().add_patch(patch)
        plt.Axes(plt.figure(4), [0., 0., 1., 1.])
        plt.gcf().set_size_inches(inchs,inchs)
        plt.gca().set_axis_off()
        imshow(cam3, aspect='normal', cmap = cm.Greys_r)
        plt.savefig("cam3.png")
        
        self.img_cam0.set_from_file("cam0.png")
        self.img_cam1.set_from_file("cam1.png")
        self.img_cam2.set_from_file("cam2.png")
        self.img_cam3.set_from_file("cam3.png")
        
        #profiles
        int_max = (2**12 - 1. )# 0 to 2^(camera bits). As start from 0, it is needed get one value less
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
        cam0_nx = cam0_nx/int_max
        cam0_ny = cam0_ny/int_max
        
        cam1_nx = cam1_nx/int_max
        cam1_ny = cam1_ny/int_max
        
        cam2_nx = cam2_nx/int_max
        cam2_ny = cam2_ny/int_max
        
        cam3_nx = cam3_nx/int_max
        cam3_ny = cam3_ny/int_max

        #plot px,py cam0       
        plt.close()
        cam0_fy = plt.figure(11, tight_layout=True, frameon=False)
        ax = cam0_fy.add_subplot(111)
        ax.set_ylim(0,x)
        ax.invert_xaxis()
        ax.plot(cam0_nx,axis,'-')
        plt.gcf().set_size_inches(inchs,inchs)
        plt.Axes(cam0_fy, [0., 0., 1., 1.])
        plt.gca().set_axis_off()
        plt.gca().set_title("sat: %.2f%%"%((c0/int_max)*100.))
        plt.savefig("cam0y.png")
        self.img_cam0_y.set_from_file("cam0y.png")
        
        plt.close()
        cam0_fx = plt.figure(12, tight_layout=True, frameon=False)
        ax2 = cam0_fx.add_subplot(111)
        ax2.set_xlim(0,x)
        ax2.plot(axis,cam0_ny,'-')
        plt.gcf().set_size_inches(inchs,inchs)
        plt.Axes(cam0_fx, [0., 0., 1., 1.])
        plt.gca().set_axis_off()
        plt.savefig("cam0x.png")
        self.img_cam0_x.set_from_file("cam0x.png")

        #--------------------------------------------------
        plt.close()
        cam1_fy = plt.figure(dpi=30, tight_layout=True, frameon=False)
        ax = cam1_fy.add_subplot(111)
        ax.set_ylim(0,x)
        ax.plot(cam1_nx,axis,'-')
        plt.gcf().set_size_inches(inchs,inchs)
        plt.Axes(cam1_fy, [0., 0., 1., 1.])
        plt.gca().set_axis_off()
        plt.gca().set_title("sat: %.2f%%"%((c1/int_max)*100.))
        plt.savefig("cam1y.png")
        self.img_cam1_y.set_from_file("cam1y.png")
        
        plt.close()
        cam1_fx = plt.figure(dpi=30, tight_layout=True, frameon=False)
        ax2 = cam1_fx.add_subplot(111)
        ax2.set_xlim(0,x)
        ax2.plot(axis,cam1_ny,'-')
        plt.gcf().set_size_inches(inchs,inchs)
        plt.Axes(cam1_fx, [0., 0., 1., 1.])
        plt.gca().set_axis_off()
        plt.savefig("cam1x.png")
        self.img_cam1_x.set_from_file("cam1x.png")
        
        #--------------------------------------------------
        plt.close()
        cam2_fy = plt.figure(dpi=30, tight_layout=True, frameon=False)
        ax = cam2_fy.add_subplot(111)
        ax.set_ylim(0,x)
        ax.invert_xaxis()
        ax.plot(cam2_nx,axis,'-')
        plt.gcf().set_size_inches(inchs,inchs)
        plt.Axes(cam2_fy, [0., 0., 1., 1.])
        plt.gca().set_axis_off()
        plt.gca().set_title("sat: %.2f%%"%((c2/int_max)*100.))
        plt.savefig("cam2y.png")
        self.img_cam2_y.set_from_file("cam2y.png")
        
        
        plt.close()
        cam2_fx = plt.figure(dpi=30, tight_layout=True, frameon=False)
        ax2 = cam2_fx.add_subplot(111)
        ax2.set_xlim(0,x)
        ax2.invert_yaxis()
        ax2.plot(axis,cam2_ny,'-')
        plt.gcf().set_size_inches(inchs,inchs)
        plt.Axes(cam2_fx, [0., 0., 1., 1.])
        plt.gca().set_axis_off()
        plt.savefig("cam2x.png")
        self.img_cam2_x.set_from_file("cam2x.png")
        #--------------------------------------------------
        plt.close()
        cam3_fy = plt.figure(dpi=30, tight_layout=True, frameon=False)
        ax = cam3_fy.add_subplot(111)
        ax.set_ylim(0,x)
        ax.plot(cam3_nx,axis,'-')
        plt.gcf().set_size_inches(inchs,inchs)
        plt.Axes(cam3_fy, [0., 0., 1., 1.])
        plt.gca().set_axis_off()
        plt.gca().set_title("sat: %.2f%%"%((c3/int_max)*100.))
        plt.savefig("cam3y.png")
        self.img_cam3_y.set_from_file("cam3y.png")
        
        plt.close()
        cam3_fx = plt.figure(dpi=30, tight_layout=True, frameon=False)
        ax2 = cam3_fx.add_subplot(111)
        ax2.set_xlim(0,x)
        ax2.invert_yaxis()
        ax2.plot(axis,cam3_ny,'-')
        plt.Axes(cam3_fx, [0., 0., 1., 1.])
        plt.gca().set_axis_off()
        plt.gcf().set_size_inches(inchs,inchs)
        plt.savefig("cam3x.png")
        self.img_cam3_x.set_from_file("cam3x.png")
        

################
#        self.button_apply_subap.connect("clicked", self._cb_subap, "subap")
#        self.button_apply_refresh.connect("clicked", self._cb_refresh, "refresh")
#        self.button_apply_offset.connect("clicked", self._cb_offset,"offset")
#
        dic = { 
            "on_buttonQuit_clicked" : self.quit,
        }
        
        self.builder.connect_signals( dic )

    def _cb_timeout(self):
        self.label_refresh.set_text(str(self.counter))
        self.counter += 30 

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
