import darc,plot,gtk,os
from darcaravis import DarcAravis

gtk.gdk.threads_init()
configdir = "/opt/darc/conf"
w=gtk.Window()
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
p1=plot.DarcReader([],prefix="all",configdir=configdir,withScroll=1,window=f1, showPlots=1)
p2=plot.DarcReader([],prefix="all",configdir=configdir,withScroll=1,window=f2, showPlots=1)
p3=plot.DarcReader([],prefix="all",configdir=configdir,withScroll=1,window=f3, showPlots=1)
p4=plot.DarcReader([],prefix="all",configdir=configdir,withScroll=1,window=f4, showPlots=1)
p1.loadFunc("/opt/darc/conf/plotRawPxls.xml")
#p1.subWid.hide()
p2.loadFunc("/opt/darc/conf/plotRawPxls.xml")
#p2.subWid.hide()
p3.loadFunc("/opt/darc/conf/plotRawPxls.xml")
p4.loadFunc("/opt/darc/conf/plotRawPxls.xml")

def quit(w,a=None):
    p1.p.quit(w)
    p2.p.quit(w)
    p3.p.quit(w)
    p4.p.quit(w)
    gtk.main_quit()

w.connect("delete-event",quit)
w.show_all()
gtk.main()#note - currently doesn't quit cleanly!

