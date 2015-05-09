#!/usr/bin/env python
import os
import sys
import darc
import ConfigParser

from pylab import imshow

from gi.repository import Gtk
from gi.repository import GObject

import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

class Acquisition(GObject.GObject):


    def __init__(self):
        GObject.GObject.__init__(self)
        self.counter = 0
        GObject.timeout_add_seconds(30, self._cb_counter)
        path, fil = os.path.split(os.path.abspath(os.path.realpath(__file__)))
        self.builder = Gtk.Builder()
        self.builder.add_from_file(path+"/glade/acquisition.glade")
        self.window = self.builder.get_object ("window1")
        self.window.set_events(self.window.get_events())
        
        self.configfile=path+'/../../conf/config.cfg'
        self.config = None
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.configfile)
        
        self.__refresh = "--"
        if self.window:
            self.window.connect("destroy", Gtk.main_quit)

        self.button_apply_refresh = self.builder.get_object("button_apply")
        self.entry_refresh = self.builder.get_object("entry_refresh")
        self.label_refresh = self.builder.get_object("label_refresh")
        #Camera IMG
        self.img_cam0 = self.builder.get_object("image_cam0")
        self.img_cam1 = self.builder.get_object("image_cam1")
        self.img_cam2 = self.builder.get_object("image_cam2")
        self.img_cam3 = self.builder.get_object("image_cam3")
        self.img_cov = self.builder.get_object("image_cov")

        self.button_apply_refresh.connect("clicked", self._cb_refresh, "refresh")
        dic = { 
            "on_buttonQuit_clicked" : self.quit,
        }
        
        self.builder.connect_signals( dic )


    def data_builder(self):
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
        inchs = 4
        #get mask
#        mask = get_mask_spot(radio,kernel)

#        cy, cx = get_centroid(cam0, mask)
        
        plt.figure(1, frameon=False)
#        patch = get_square(cx,cy,subap)
#        plt.gca().add_patch(patch)
#        patch = get_square(cx,cy,height,color='green')
#        plt.gca().add_patch(patch)
        plt.gcf().set_size_inches(inchs,inchs)
        plt.Axes(plt.figure(1), [0., 0., 1., 1.])
        plt.gca().set_axis_off()
        imshow(cam0, aspect='normal', cmap = cm.Greys_r)
        plt.savefig("cam0.png")

        plt.figure(2, frameon=False)
#        cy, cx = get_centroid(cam1, mask)
#        patch = get_square(cx,cy,subap)
#        plt.gca().add_patch(patch)
#        patch = get_square(cx,cy,height,color='green')
#        plt.gca().add_patch(patch)
        plt.Axes(plt.figure(2), [0., 0., 1., 1.])
        plt.gcf().set_size_inches(inchs,inchs)
        plt.gca().set_axis_off()
        imshow(cam1, aspect='normal', cmap = cm.Greys_r)
        plt.savefig("cam1.png")

        plt.figure(3, frameon=False)
#        cy, cx = get_centroid(cam2, mask)
#        patch = get_square(cx,cy,subap)
#        plt.gca().add_patch(patch)
#        patch = get_square(cx,cy,height,color='green')
#        plt.gca().add_patch(patch)
        plt.Axes(plt.figure(3), [0., 0., 1., 1.])
        plt.gcf().set_size_inches(inchs,inchs)
        plt.gca().set_axis_off()
        imshow(cam2, aspect='normal', cmap = cm.Greys_r)
        plt.savefig("cam2.png")

        plt.figure(4, frameon=False)
#        cy, cx = get_centroid(cam3, mask)
#        patch = get_square(cx,cy,subap)
#        plt.gca().add_patch(patch)
#        patch = get_square(cx,cy,height,color='green')
#        plt.gca().add_patch(patch)
        plt.Axes(plt.figure(4), [0., 0., 1., 1.])
        plt.gcf().set_size_inches(inchs,inchs)
        plt.gca().set_axis_off()
        imshow(cam3, aspect='normal', cmap = cm.Greys_r)
        plt.savefig("cam3.png")
        
        self.img_cam0.set_from_file("cam0.png")
        self.img_cam1.set_from_file("cam1.png")
        self.img_cam2.set_from_file("cam2.png")
        self.img_cam3.set_from_file("cam3.png")

        #COVAR
        prefix = "all"
        streamBlock = d.GetStreamBlock('%srtcCentBuf'%prefix,5)#,block=1,flysave=options.directory+'/img.fits')
        streams = streamBlock['%srtcCentBuf'%prefix]
        x0 = np.array([])
        x1 = np.array([])
        x2 = np.array([])
        x3 = np.array([])
        y0 = np.array([])
        y1 = np.array([])
        y2 = np.array([])
        y3 = np.array([])
        for stream in streams:
            data = stream[0]
            x0 = np.append(x0,data[0])
            y0 = np.append(x0,data[1])
        
            x1 = np.append(x1,data[2])
            y1 = np.append(x1,data[3])
        
            x2 = np.append(x2,data[4])
            y2 = np.append(x2,data[5])
        
            x3 = np.append(x3,data[6])
            y3 = np.append(x3,data[7])
        
        cov_x = np.array([])
        cov_x = np.append(cov_x, np.cov(x0,x1)[0][1]) 
        cov_x = np.append(cov_x, np.cov(x0,x2)[0][1])
        cov_x = np.append(cov_x, np.cov(x0,x3)[0][1])
        cov_x = np.append(cov_x, np.cov(x1,x2)[0][1])
        cov_x = np.append(cov_x, np.cov(x1,x3)[0][1])
        cov_x = np.append(cov_x, np.cov(x2,x3)[0][1])
        
        cov_y = np.array([])
        cov_y = np.append(cov_y, np.cov(y0,y1)[0][1]) 
        cov_y = np.append(cov_y, np.cov(y0,y2)[0][1])
        cov_y = np.append(cov_y, np.cov(y0,y3)[0][1])
        cov_y = np.append(cov_y, np.cov(y1,y2)[0][1])
        cov_y = np.append(cov_y, np.cov(y1,y3)[0][1])
        cov_y = np.append(cov_y, np.cov(y2,y3)[0][1])
        
        
        baselines = [2,10,15,20,50,120]
        plt.close()
        fig = plt.figure()
        ax = plt.subplot(111)
        ax.plot(baselines, cov_x,'ro-',label=r'$COV(X_{i},X_{i+1})$')
        ax.plot(baselines, cov_y,'bo-',label=r'$COV(Y_{i},Y_{i+1})$')
        x = ax.get_position()
        plt.title(r'COV(X,Y) v/s Baseline')
        plt.ylabel(r'$COV(XY_{i},XY_{i+1})$')
        plt.xlabel(r'baseline')
        ax.xaxis.grid(True)
        ax.yaxis.grid(True)
        ax.legend(loc='center left', bbox_to_anchor=(0.75, 0.92))
        plt.gcf().set_size_inches(inchs,inchs)
        plt.savefig('covx.png')
        self.img_cov.set_from_file("covx.png")

    def _cb_refresh(self, widget, data=None):
        '''
        
        '''
        refresh = self.entry_refresh.get_text()
        print "refresh every: %s" % refresh
        if refresh == "":
            refresh = "10"
        self.__refresh = int(refresh)
        print "self.__refresh %d" % self.__refresh
        self.label_refresh.set_text("refresh every: %s" % str(refresh))
        self.entry_refresh.set_text("")

    def _cb_counter(self):
        self.counter += 1
        self.data_builder()
        print self.counter
        return True

    def quit(self, widget):
        '''
        quit
        '''
        sys.exit(0)

if __name__ == '__main__':

    Acquisition = Acquisition()
    Acquisition.window.show()
    Gtk.main()
