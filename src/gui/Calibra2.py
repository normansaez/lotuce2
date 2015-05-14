#!/usr/bin/env python

import os
import gtk
import darc
import gobject
import numpy as np
import matplotlib
matplotlib.use('GTKAgg')
from matplotlib.figure import Figure
#from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas

class Acquisition:
    def __init__(self, timeout):
        self.window = gtk.Window()
        self.window.connect('destroy', lambda wid: gtk.main_quit())
        self.window.connect('delete_event', lambda a1,a2:gtk.main_quit())
        self.window.set_default_size(800,800)
        # Vertical Box contains all horizontal boxes
        #    
        # | hbox1 |
        # | hbox2 |
        # | hbox3 |
        # | hbox4 |
        #    ^
        #    |
        #   vbox
        #
        vbox=gtk.VBox()
        #
        # Horizontal Box contains a row such as follows
        #   | -    | c0px | c1px | -    |  -> hbox1
        #   | c0py | cam0 | cam1 | c1py |  -> hbox2
        #   | c2py | cam2 | cam3 | c3py |  -> hbox3
        #   | -    | c2px | c3px | -    |  -> hbox4
        #
        hbox1=gtk.HBox()
        hbox2=gtk.HBox()
        hbox3=gtk.HBox()
        hbox4=gtk.HBox()
        # 
        # Create frames to fill up hboxes
        #
        #
        #Labels frames
        #
        frame_label_cam0=gtk.Frame()
        frame_label_cam1=gtk.Frame()
        frame_label_cam2=gtk.Frame()
        frame_label_cam3=gtk.Frame()
        #
        # Profiles frames: 2 per camera x,y
        #
        self.frame_c0px=gtk.Frame()
        self.frame_c0py=gtk.Frame()
        
        self.frame_c1px=gtk.Frame()
        self.frame_c1py=gtk.Frame()
        
        self.frame_c2px=gtk.Frame()
        self.frame_c2py=gtk.Frame()
        
        self.frame_c3px=gtk.Frame()
        self.frame_c3py=gtk.Frame()
        #
        # Camera frames
        #
        self.frame_cam0=gtk.Frame()
        self.frame_cam1=gtk.Frame()
        self.frame_cam2=gtk.Frame()
        self.frame_cam3=gtk.Frame()
        #
        # Fill hbox with camera content
        #
        hbox1.pack_start(frame_label_cam0,True)
        hbox1.pack_start(self.frame_c0py,True)
        hbox1.pack_start(self.frame_c1py,True)
        hbox1.pack_start(frame_label_cam1,True)
        #
        #
        #Fill with calculate profiles and plots
        #
#        self.canvas_c0px = None
#        self.data_builder()
        hbox2.pack_start(self.frame_c0px,True)
#        hbox2.pack_start(self.image_c0px,True)
#        hbox2.pack_start(self.canvas_c0px,True)
#        print "in>",
#        print id(self.canvas_c0px)
        hbox2.pack_start(self.frame_cam0,True)
        hbox2.pack_start(self.frame_cam1,True)
        hbox2.pack_start(self.frame_c1px,True)
        #
        hbox3.pack_start(self.frame_c2px,True)
        hbox3.pack_start(self.frame_cam2,True)
        hbox3.pack_start(self.frame_cam3,True)
        hbox3.pack_start(self.frame_c3px,True)
        #
        hbox4.pack_start(frame_label_cam2,True)
        hbox4.pack_start(self.frame_c2py,True)
        hbox4.pack_start(self.frame_c3py,True)
        hbox4.pack_start(frame_label_cam3,True)
        #
        # Fill vbox with hbox content 
        #
        vbox.pack_start(hbox1,True)
        vbox.pack_start(hbox2,True)
        vbox.pack_start(hbox3,True)
        vbox.pack_start(hbox4,True)
        #
        #Fill with DARC content
        #
        self.counter = 0
        self.darc_reader()

        #
        #Fill with calculate profiles and plots
        #
#        self.data_builder()

        #
        # Fill window with vbox content 
        #
        self.window.add(vbox)
        self.window.show_all()

        # register a periodic timer
        gobject.timeout_add_seconds(timeout, self._cb_timer)

    def darc_reader(self):
        import plot
        _prefix = 'all'
        configdir = "/opt/darc/conf"
        path, fil = os.path.split(os.path.abspath(os.path.realpath(__file__)))
        plot_cam0 = plot.DarcReader([], prefix=_prefix, dec=125, configdir=configdir, withScroll=1, window=self.frame_cam0, showPlots=0)
        plot_px_cam0 = plot.DarcReader([], prefix=_prefix, dec=125, configdir=configdir, withScroll=1, window=self.frame_c0px, showPlots=0)
#        plot_cam1 = plot.DarcReader([], prefix=_prefix, dec=125, configdir=configdir, withScroll=1, window=self.frame_cam1, showPlots=0)
#        plot_cam2 = plot.DarcReader([], prefix=_prefix, dec=125, configdir=configdir, withScroll=1, window=self.frame_cam2, showPlots=0)
#        plot_cam3 = plot.DarcReader([], prefix=_prefix, dec=125, configdir=configdir, withScroll=1, window=self.frame_cam3, showPlots=0)

        plot_cam0.p.loadFunc(path+"/xmlcfg/cam0.xml")
        plot_px_cam0.p.loadFunc(path+"/xmlcfg/p0x.xml")
#        plot_cam1.p.loadFunc(path+"/xmlcfg/cam1.xml")
#        plot_cam2.p.loadFunc(path+"/xmlcfg/cam2.xml")
#        plot_cam3.p.loadFunc(path+"/xmlcfg/cam3.xml")

    def data_builder(self):
        _prefix = 'all'
        d_obj = darc.Control(_prefix)
        
        int_max = (2**12 - 1. )# 0 to 2^(camera bits). As start from 0, it is needed get one value less
        pxlx =d_obj.Get("npxlx")[0]
        pxly =d_obj.Get("npxly")[0]
        stream=d_obj.GetStream('%srtcPxlBuf'% _prefix)
        mydata = stream[0].reshape((1*pxly,pxlx))
#        mydata = stream[0].reshape((4*pxly,pxlx))
#
#        xi_cam0 = 0*pxly
#        xf_cam0 = 1*pxly
#        yi_cam0 = 0*pxlx
#        yf_cam0 = 1*pxlx
#        
#        xi_cam1 = 1*pxly
#        xf_cam1 = 2*pxly
#        yi_cam1 = 0*pxlx
#        yf_cam1 = 1*pxlx
#        
#        xi_cam2 = 2*pxly
#        xf_cam2 = 3*pxly
#        yi_cam2 = 0*pxlx
#        yf_cam2 = 1*pxlx
#        
#        xi_cam3 = 3*pxly
#        xf_cam3 = 4*pxly
#        yi_cam3 = 0*pxlx
#        yf_cam3 = 1*pxlx
        
        #data per camera:
        cam0 = mydata
#        cam0 = mydata[xi_cam0:xf_cam0,yi_cam0:yf_cam0]
#        cam1 = mydata[xi_cam1:xf_cam1,yi_cam1:yf_cam1]
#        cam2 = mydata[xi_cam2:xf_cam2,yi_cam2:yf_cam2]
#        cam3 = mydata[xi_cam3:xf_cam3,yi_cam3:yf_cam3]

        x = len(cam0)
        cam0_nx = np.array([])
        cam0_ny = np.array([])
#        cam1_nx = np.array([])
#        cam1_ny = np.array([])
#        cam2_nx = np.array([])
#        cam2_ny = np.array([])
#        cam3_nx = np.array([])
#        cam3_ny = np.array([])
        
        c0 = cam0.max()
#        c1 = cam1.max()
#        c2 = cam2.max()
#        c3 = cam3.max()
         
        for i in range(0,x):
            cam0_nx = np.append(cam0_nx, cam0[i,].sum())
            cam0_ny = np.append(cam0_ny, cam0[:,i].sum())
#            cam1_nx = np.append(cam1_nx, cam1[i,].sum())
#            cam1_ny = np.append(cam1_ny, cam1[:,i].sum())
#            cam2_nx = np.append(cam2_nx, cam2[i,].sum())
#            cam2_ny = np.append(cam2_ny, cam2[:,i].sum())
#            cam3_nx = np.append(cam3_nx, cam3[i,].sum())
#            cam3_ny = np.append(cam3_ny, cam3[:,i].sum())
        axis = range(0,x)
        #normalize according cameras:
        cam0_nx = cam0_nx/int_max
        cam0_ny = cam0_ny/int_max
        
#        cam1_nx = cam1_nx/int_max
#        cam1_ny = cam1_ny/int_max
#        
#        cam2_nx = cam2_nx/int_max
#        cam2_ny = cam2_ny/int_max
#        
#        cam3_nx = cam3_nx/int_max
#        cam3_ny = cam3_ny/int_max
        
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
#        #--------------------------------------------------
#        #cam1_fx = Figure(figsize=(5,4), dpi=30)
#        cam1_fx = Figure(dpi=30, tight_layout=True)
#        ax = cam1_fx.add_subplot(111)
#        #ax.set_xlim(0,1)
#        ax.set_ylim(0,x)
#        ax.plot(cam1_nx,axis,'-')
#        
#        #cam1_fy = Figure(figsize=(5,4), dpi=30)
#        cam1_fy = Figure(dpi=30, tight_layout=True)
#        ax2 = cam1_fy.add_subplot(111)
#        ax2.set_xlim(0,x)
#        #ax2.set_ylim(0,1)
#        ax2.plot(axis,cam1_ny,'-')
#        #--------------------------------------------------
#        #cam2_fx = Figure(figsize=(5,4), dpi=30)
#        cam2_fx = Figure(dpi=30, tight_layout=True)
#        ax = cam2_fx.add_subplot(111)
#        #ax.set_xlim(0,1)
#        ax.set_ylim(0,x)
#        ax.invert_xaxis()
#        ax.plot(cam2_nx,axis,'-')
#        
#        #cam2_fy = Figure(figsize=(5,4), dpi=30)
#        cam2_fy = Figure(dpi=30, tight_layout=True)
#        ax2 = cam2_fy.add_subplot(111)
#        ax2.set_xlim(0,x)
#        #ax2.set_ylim(0,1)
#        ax2.invert_yaxis()
#        ax2.plot(axis,cam2_ny,'-')
#        #--------------------------------------------------
#        #cam3_fx = Figure(figsize=(5,4), dpi=30)
#        cam3_fx = Figure(dpi=30, tight_layout=True)
#        ax = cam3_fx.add_subplot(111)
#        #ax.set_xlim(0,1)
#        ax.set_ylim(0,x)
#        ax.plot(cam3_nx,axis,'-')
#        
#        #cam3_fy = Figure(figsize=(5,4), dpi=30)
#        cam3_fy = Figure(dpi=30, tight_layout=True)
#        ax2 = cam3_fy.add_subplot(111)
#        ax2.set_xlim(0,x)
#        #ax2.set_ylim(0,1)
#        ax2.invert_yaxis()
#        ax2.plot(axis,cam3_ny,'-')

        #fill up profiles
#        self.canvas_c0px = FigureCanvas(cam0_fx)  # a gtk.DrawingArea
#        canvas_c0_fy = FigureCanvas(cam0_fy)  # a gtk.DrawingArea
#        self.image_c0px.set_from_pixbuf(self.canvas_c0_fx)
#        self.frame_c0py.add(self.canvas_c0_fy)
#        print "bd>",
#        print id(self.canvas_c0px)
#        self.canvas_c0_fy.draw()
            
#        canvas_c1_fx = FigureCanvas(cam1_fx)  # a gtk.DrawingArea
#        canvas_c1_fy = FigureCanvas(cam1_fy)  # a gtk.DrawingArea
#        self.frame_c1px.add(canvas_c1_fx)
#        self.frame_c1py.add(canvas_c1_fy)
#        
#        canvas_c2_fx = FigureCanvas(cam2_fx)  # a gtk.DrawingArea
#        canvas_c2_fy = FigureCanvas(cam2_fy)  # a gtk.DrawingArea
#        self.frame_c2px.add(canvas_c2_fx)
#        self.frame_c2py.add(canvas_c2_fy)
#        
#        canvas_c3_fx = FigureCanvas(cam3_fx)  # a gtk.DrawingArea
#        canvas_c3_fy = FigureCanvas(cam3_fy)  # a gtk.DrawingArea
#        self.frame_c3px.add(canvas_c3_fx)
#        self.frame_c3py.add(canvas_c3_fy)

    def _cb_timer(self):
        self.counter += 1
        print self.counter
        print "cb>",
#        print id(self.canvas_c0px)
#        self.canvas_c0px.draw()
#        self.data_builder()
        return True

if __name__ == '__main__':
    acq = Acquisition(1)
    gtk.main()
