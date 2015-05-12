#!/usr/bin/env python

import gtk, gobject

class Acquisition:
    def __init__(self, timeout):

        # create a simple window with a label
        self.window = gtk.Window()
        self.window.connect('destroy', lambda wid: gtk.main_quit())
        self.window.connect('delete_event', lambda a1,a2:gtk.main_quit())
        self.window.set_default_size(800,800)
        ver1=gtk.VBox()
        hor1=gtk.HBox()
        hor2=gtk.HBox()
        hor3=gtk.HBox()
        hor4=gtk.HBox()
        #-----------------
        f0=gtk.Frame()
        f1=gtk.Frame()
        f2=gtk.Frame()
        f3=gtk.Frame()
        #----------------------
        ver1.pack_start(hor1,True)
        ver1.pack_start(hor2,True)
        ver1.pack_start(hor3,True)
        ver1.pack_start(hor4,True)
        self.window.add(ver1)
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
