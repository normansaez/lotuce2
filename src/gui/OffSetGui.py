#!/usr/bin/env python
import os
import sys
from gi.repository import Gtk
from gi.repository import GObject

from darcaravis import DarcAravis

class OffSetGui:


    def __init__( self ):
        path, fil = os.path.split(os.path.abspath(__file__))

        self.builder = Gtk.Builder()
        self.builder.add_from_file(path+"/offset.glade")
        self.window = self.builder.get_object ("window1")
        self.window.set_events(self.window.get_events())
        
        self.DarcAravis = DarcAravis()

        #step
        self.__step = 10

        if self.window:
            self.window.connect("destroy", Gtk.main_quit)

        self.camera = 0
        #Offset x,y
        self.offset_x = self.builder.get_object("offset_x")
        offset_x = self.DarcAravis.get(self.camera, 'OffsetX')
        self.offset_x.set_text("%s pixel(s)"% offset_x)

        self.offset_y = self.builder.get_object("offset_y")
        offset_y = self.DarcAravis.get(self.camera, 'OffsetY')
        self.offset_y.set_text("%s pixel(s)"% offset_y)

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

        #apply_step
        self.button_apply_step = self.builder.get_object("apply_step")
        self.button_apply_step.connect("clicked", self.step_callback, "step")

        self.step = self.builder.get_object("step")
        self.current_step = self.builder.get_object("current_step")
        self.current_step.set_text("-- pixel(s)")
        self.step.set_text("10")

        dic = { 
            "on_buttonQuit_clicked" : self.quit,
        }
        
        self.builder.connect_signals( dic )

    def callback(self, widget, data=None):
        '''
        callback
        '''
        print "%s: %s" % (data, ("disconnecting", "connecting")[widget.get_active()])
        #CONN
        if widget.get_active() is True:
            print "cam0: %s" % self.togglebutton_cam0.get_active()
            print "cam1: %s" % self.togglebutton_cam1.get_active()
            print "cam2: %s" % self.togglebutton_cam2.get_active()
            print "cam3: %s" % self.togglebutton_cam3.get_active()
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

            self.camera = int(data)
            offset_y = self.DarcAravis.get(self.camera, 'OffsetY')
            self.offset_y.set_text("%d pixel(s)"% int(offset_y)) 
            offset_x = self.DarcAravis.get(self.camera, 'OffsetX')
            self.offset_x.set_text("%d pixel(s)"% int(offset_x))


#        if widget.get_active() is False:
#            print "OFF"

    def offset_callback(self, widget, data=None):
        '''
        offset callback

        The offset is taking as reference darcplot gui.  Therefore the offset
        cross follows that darcplot axis references.
        '''
        print "offset: %s" % (data)
        offset_y = self.DarcAravis.get(self.camera, 'OffsetY')
        offset_x = self.DarcAravis.get(self.camera, 'OffsetX')
        print "before apply step(%d)\noffset(%d,%d)" % (self.__step, offset_x, offset_y)

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

        offset_y = self.DarcAravis.get(self.camera, 'OffsetY')
        offset_x = self.DarcAravis.get(self.camera, 'OffsetX')
        if data =='up' or data =='do':
            self.offset_y.set_text("%d pixel(s)"% int(offset_y))
        if data =='le' or data =='ri':
            self.offset_x.set_text("%d pixel(s)"% int(offset_x))
        print "after apply: offset(%d,%d)" % (offset_x, offset_y)
        


    def step_callback(self, widget, data=None):
        '''
        step_callback
        '''
        step = self.step.get_text()
        print "step %s" % step
        if step == "":
            step = "10"
        self.__step = int(step)
        print "self.__step %d" % self.__step
        self.current_step.set_text("%s pixel(s)"% step)
        self.step.set_text("")

    def quit(self, widget):
        '''
        quit
        '''
        sys.exit(0)

if __name__ == '__main__':

    OffSetGui = OffSetGui()
    OffSetGui.window.show()
    Gtk.main()
