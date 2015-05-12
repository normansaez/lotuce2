#!/usr/bin/env python

import gtk, gobject

class Acquisition:
    def __init__(self, timeout):

        # create a simple window with a label
        self.window = gtk.Window()
        self.window.connect('destroy', lambda wid: gtk.main_quit())
        self.window.connect('delete_event', lambda a1,a2:gtk.main_quit())
        self.window.set_default_size(800,800)
        #Vertical Box contains all horizontal boxes
        #    
        # | hbox1 |
        # | hbox2 |
        # | hbox3 |
        # | hbox4 |
        #    ^
        #    |
        #   vbox
        vbox=gtk.VBox()
        #Horizontal Box contains a row such as follows
        #   | -    | c0px | c1px | -    |  -> hbox1
        #   | c0py | cam0 | cam1 | c1py |  -> hbox2
        #   | c2py | cam2 | cam3 | c3py |  -> hbox3
        #   | -    | c2px | c3px | -    |  -> hbox4

        hbox1=gtk.HBox()
        hbox2=gtk.HBox()
        hbox3=gtk.HBox()
        hbox4=gtk.HBox()

        hbox1.pack_start(cam0_l,True)
        hbox1.pack_start(cam0_p_y,True)
        hbox1.pack_start(cam1_p_y,True)
        hbox1.pack_start(cam1_l,True)
        #----------------------
        hbox2.pack_start(cam0_p_x,True)
        hbox2.pack_start(f0,True)
        hbox2.pack_start(f1,True)
        hbox2.pack_start(cam1_p_x,True)
        #----------------------
        hbox3.pack_start(cam2_p_x,True)
        hbox3.pack_start(f2,True)
        hbox3.pack_start(f3,True)
        hbox3.pack_start(cam3_p_x,True)
        #----------------------
        hbox4.pack_start(cam2_l,True)
        hbox4.pack_start(cam2_p_y,True)
        hbox4.pack_start(cam3_p_y,True)
        hbox4.pack_start(cam3_l,True)
        #-----------------
        f0=gtk.Frame()
        f1=gtk.Frame()
        f2=gtk.Frame()
        f3=gtk.Frame()
        #----------------------
        vbox.pack_start(hbox1,True)
        vbox.pack_start(hbox2,True)
        vbox.pack_start(hbox3,True)
        vbox.pack_start(hbox4,True)
        #---------------------------
        self.window.add(vbox)
        self.window.show_all()

        # register a periodic timer
        self.counter = 0
        gobject.timeout_add_seconds(timeout, self.callback)

    def callback(self):
        self.counter += 1
        print self.counter
        return True

if __name__ == '__main__':
    acq = Acquisition(1)
    gtk.main()
