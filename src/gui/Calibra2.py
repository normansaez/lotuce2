#!/usr/bin/env python

import gtk, gobject

class Acquisition:
    def __init__(self, timeout):

        # create a simple window with a label
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
        frame_c0px=gtk.Frame()
        frame_c0py=gtk.Frame()
        
        frame_c1px=gtk.Frame()
        frame_c1py=gtk.Frame()
        
        frame_c2px=gtk.Frame()
        frame_c2py=gtk.Frame()
        
        frame_c3px=gtk.Frame()
        frame_c3py=gtk.Frame()
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
        hbox1.pack_start(frame_c0py,True)
        hbox1.pack_start(frame_c1py,True)
        hbox1.pack_start(frame_label_cam1,True)
        #
        hbox2.pack_start(frame_c0px,True)
        hbox2.pack_start(self.frame_cam0,True)
        hbox2.pack_start(self.frame_cam1,True)
        hbox2.pack_start(frame_c1px,True)
        #
        hbox3.pack_start(frame_c2px,True)
        hbox3.pack_start(self.frame_cam2,True)
        hbox3.pack_start(self.frame_cam3,True)
        hbox3.pack_start(frame_c3px,True)
        #
        hbox4.pack_start(frame_label_cam2,True)
        hbox4.pack_start(frame_c2py,True)
        hbox4.pack_start(frame_c3py,True)
        hbox4.pack_start(frame_label_cam3,True)
        #
        # Fill vbox with hbox content 
        #
        vbox.pack_start(hbox1,True)
        vbox.pack_start(hbox2,True)
        vbox.pack_start(hbox3,True)
        vbox.pack_start(hbox4,True)
        #
        # Fill window with vbox content 
        #
        self.window.add(vbox)
        self.window.show_all()

        # register a periodic timer
        self.counter = 0
        gobject.timeout_add_seconds(timeout, self.callback)
        #
        #Fill with DARC content
        #
        #self.darc_reader()

        #
        #Fill with calculate profiles and plots
        #
        #self.data_builder()

    def darc_reader(self):
        plot_cam0 = plot.DarcReader([], prefix=_prefix, dec=125, configdir=configdir, withScroll=1, window=self.frame_cam0, showPlots=0)
        plot_cam1 = plot.DarcReader([], prefix=_prefix, dec=125, configdir=configdir, withScroll=1, window=self.frame_cam1, showPlots=0)
        plot_cam2 = plot.DarcReader([], prefix=_prefix, dec=125, configdir=configdir, withScroll=1, window=self.frame_cam2, showPlots=0)
        plot_cam3 = plot.DarcReader([], prefix=_prefix, dec=125, configdir=configdir, withScroll=1, window=self.frame_cam3, showPlots=0)

        plot_cam0.p.loadFunc("/home/lotuce2/lotuce2/src/gui/xmlcfg/cam0.xml")
        plot_cam1.p.loadFunc("/home/lotuce2/lotuce2/src/gui/xmlcfg/cam1.xml")
        plot_cam2.p.loadFunc("/home/lotuce2/lotuce2/src/gui/xmlcfg/cam2.xml")
        plot_cam3.p.loadFunc("/home/lotuce2/lotuce2/src/gui/xmlcfg/cam3.xml")

    def callback(self):
        self.counter += 1
        print self.counter
        return True

if __name__ == '__main__':
    acq = Acquisition(1)
    gtk.main()
