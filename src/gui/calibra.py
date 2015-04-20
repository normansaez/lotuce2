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
from darcaravis import DarcAravis

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
        GObject.threads_init()
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
        
        self.__step = "--"
        if self.window:
            self.window.connect("destroy", Gtk.main_quit)


        self.counter = 0
        GObject.timeout_add_seconds(1, self._cb_timeout)

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
#TODO: remove all of this shit from init to somewere else        
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
        #Toggle button to connect to cam0
        self.togglebutton_cam0 = self.builder.get_object ("togglebutton0")
        self.togglebutton_cam0.connect("toggled", self.callback, "0")

        #Toggle button to connect to cam1
        self.togglebutton_cam1 = self.builder.get_object ("togglebutton1")
        self.togglebutton_cam1.connect("toggled", self.callback, "1")

        #Toggle button to connect to cam2
        self.togglebutton_cam2 = self.builder.get_object ("togglebutton2")
        self.togglebutton_cam2.connect("toggled", self.callback, "2")

        #Toggle button to connect to cam3
        self.togglebutton_cam3 = self.builder.get_object ("togglebutton3")
        self.togglebutton_cam3.connect("toggled", self.callback, "3")
        
        #Default cam0:
        self.togglebutton_cam0.set_active(True)

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

        self.button_apply_offset.connect("clicked", self.step_callback, "step")
        dic = { 
            "on_buttonQuit_clicked" : self.quit,
        }
        
        self.builder.connect_signals( dic )

    def step_callback(self, widget, data=None):
        '''
        step_callback
        '''
        step = self.entry_offset.get_text()
        print "step %s" % step
        if step == "":
            step = "10"
        self.__step = int(step)
        print "self.__step %d" % self.__step
        self.label_offset.set_text("%s" % str(step))
        self.entry_offset.set_text("")

    def offset_callback(self, widget, data=None):
        '''
        offset callback

        The offset is taking as reference darcplot gui.  Therefore the offset
        cross follows that darcplot axis references.
        '''
#        print "offset: %s" % (data)
#        offset_y = self.DarcAravis.get(self.camera, 'OffsetY')
#        offset_x = self.DarcAravis.get(self.camera, 'OffsetX')
#        print "before apply step(%d)\noffset(%d,%d)" % (self.__step, offset_x, offset_y)

        if data == 'up':
            val = offset_y + self.__step
            print "to be applied: %d" % val
            self.DarcAravis.set(self.camera, 'OffsetY', val)
        if data == 'do':
            val = offset_y - self.__step
            print "to be applied: %d" % val
            self.DarcAravis.set(self.camera, 'OffsetY', val)
        if data == 'le':
            val = offset_x + self.__step
            print "to be applied: %d" % val
            self.DarcAravis.set(self.camera, 'OffsetX', val)
        if data == 'ri':
            val = offset_x - self.__step
            print "to be applied: %d" % val
            self.DarcAravis.set(self.camera, 'OffsetX', val)

        if data == 'first try':
            x = self.DarcAravis.get(self.camera, 'Width')
            y = self.DarcAravis.get(self.camera, 'Height')
            offsetX = int((656 - x )/2.0)
            offsetY = int((492 - y)/2.0)
            self.DarcAravis.set(self.camera, 'OffsetX', offsetX)
            self.DarcAravis.set(self.camera, 'OffsetY', offsetY)

        offset_y = self.DarcAravis.get(self.camera, 'OffsetY')
        offset_x = self.DarcAravis.get(self.camera, 'OffsetX')
        if data =='up' or data =='do' or data == 'first try':
            self.offset_y.set_text("%d pixel(s)"% int(offset_y))
        if data =='le' or data =='ri' or data == 'first try':
            self.offset_x.set_text("%d pixel(s)"% int(offset_x))
        print "after apply: offset(%d,%d)" % (offset_x, offset_y)
        


    def callback(self, widget, data=None):
        '''
        callback
        '''
        print "%s: %s" % (data, ("disconnecting", "connecting")[widget.get_active()])
        #CONN
        if widget.get_active() is True:
            if data == "0":
#                self.togglebutton_cam0.set_active(False)
                self.togglebutton_cam1.set_active(False)
                self.togglebutton_cam2.set_active(False)
                self.togglebutton_cam3.set_active(False)

            if data == "1":
                self.togglebutton_cam0.set_active(False)
#                self.togglebutton_cam1.set_active(False)
                self.togglebutton_cam2.set_active(False)
                self.togglebutton_cam3.set_active(False)

            if data == "2":
                self.togglebutton_cam0.set_active(False)
                self.togglebutton_cam1.set_active(False)
#                self.togglebutton_cam2.set_active(False)
                self.togglebutton_cam3.set_active(False)

            if data == "3":
                self.togglebutton_cam0.set_active(False)
                self.togglebutton_cam1.set_active(False)
                self.togglebutton_cam2.set_active(False)
#                self.togglebutton_cam3.set_active(False)

#            self.camera = int(data)
#            offset_y = self.DarcAravis.get(self.camera, 'OffsetY')
#            self.offset_y.set_text("%d pixel(s)"% int(offset_y)) 
#            offset_x = self.DarcAravis.get(self.camera, 'OffsetX')
#            self.offset_x.set_text("%d pixel(s)"% int(offset_x))


#        if widget.get_active() is False:
#            print "OFF"

    def _cb_timeout(self):
        self.counter += 1 
        self.label_refresh.set_text(str(self.counter))
        print "pase"

    def _cb_stop( self, button):
        print "Stop was clicked"

    def _cb_play(self, widget, data=None):
        print "%s: %s" % (data, ("disconnecting", "connecting")[widget.get_active()])

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
