import darc,plot,gtk,os
from darcaravis import DarcAravis

gtk.gdk.threads_init()
configdir = "/opt/darc/conf"
w=gtk.Window()
w.set_default_size(800,600)
v=gtk.VBox()
h1=gtk.HBox()
h2=gtk.HBox()
f1=gtk.Frame()
f2=gtk.Frame()
f3=gtk.Frame()
f4=gtk.Frame()
v.pack_start(h1,True)
v.pack_start(h2,True)
h1.pack_start(f1,True)
h1.pack_start(f2,True)
h2.pack_start(f3,True)
h2.pack_start(f4,True)
w.add(v)
#w.add(h)
p1=plot.DarcReader([], prefix="all", dec=125, configdir=configdir, withScroll=1, window=f1, showPlots=0)
p2=plot.DarcReader([], prefix="all", dec=125, configdir=configdir, withScroll=1, window=f2, showPlots=0)
p3=plot.DarcReader([], prefix="all", dec=125, configdir=configdir, withScroll=1, window=f3, showPlots=0)
p4=plot.DarcReader([], prefix="all", dec=125, configdir=configdir, withScroll=1, window=f4, showPlots=0)
p1.p.loadFunc("/home/lotuce2/lotuce2/src/gui/cam0.xml")
p2.p.loadFunc("/home/lotuce2/lotuce2/src/gui/cam1.xml")
p3.p.loadFunc("/home/lotuce2/lotuce2/src/gui/cam2.xml")
p4.p.loadFunc("/home/lotuce2/lotuce2/src/gui/cam3.xml")
p1.subWid.hide()
p2.subWid.hide()


def quit(w,a=None):
    p1.p.quit(w)
    p2.p.quit(w)
    p3.p.quit(w)
    p4.p.quit(w)
    gtk.main_quit()

w.connect("delete-event",quit)
w.show_all()
gtk.main()#note - currently doesn't quit cleanly!

