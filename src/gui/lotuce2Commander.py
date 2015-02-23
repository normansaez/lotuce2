import darc,plot,gtk,os
from darcaravis import DarcAravis

gtk.gdk.threads_init()
configdir = "/opt/darc/conf"
w=gtk.Window()
v=gtk.VBox()
f1=gtk.Frame()
f2=gtk.Frame()
v.pack_start(f1,True)
v.pack_start(f2,True)
w.add(v)
p1=plot.DarcReader([],prefix="all",configdir=configdir,withScroll=1,window=f1, showPlots=0)
p2=plot.DarcReader([],prefix="all",configdir=configdir,withScroll=1,window=f2, showPlots=0)
p1.loadFunc("/opt/darc/conf/plotRawPxls.xml")
#p1.subWid.hide()
p2.loadFunc("/opt/darc/conf/plotRawPxls.xml")
#p2.subWid.hide()

def quit(w,a=None):
    p1.p.quit(w)
    p2.p.quit(w)
    gtk.main_quit()

w.connect("delete-event",quit)
w.show_all()
gtk.main()#note - currently doesn't quit cleanly!

