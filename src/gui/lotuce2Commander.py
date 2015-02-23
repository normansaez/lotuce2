import darc,plot,gtk,os
from darcaravis import DarcAravis
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from numpy import arange, sin, pi
from matplotlib.figure import Figure



gtk.gdk.threads_init()
configdir = "/opt/darc/conf"
w=gtk.Window()
w.set_default_size(800,600)
v=gtk.VBox()
h1=gtk.HBox()
h2=gtk.HBox()
#-----------------
f1=gtk.Frame()
f2=gtk.Frame()
f3=gtk.Frame()
f4=gtk.Frame()
#----------------------
v.pack_start(h1,True)
v.pack_start(h2,True)
#----- two plots:
p1_cov=gtk.Frame()
p2_cov=gtk.Frame()
#----------------------
h1.pack_start(f1,True)
h1.pack_start(f2,True)
h1.pack_start(p1_cov,True)

h2.pack_start(f3,True)
h2.pack_start(f4,True)
h2.pack_start(p2_cov,True)
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
#p1.subWid.hide()
#p2.subWid.hide()

f = Figure(figsize=(5,4), dpi=100)
a = f.add_subplot(111)
t = arange(0.0,3.0,0.01)
s = sin(2*pi*t)
a.plot(t,s)

canvas = FigureCanvas(f)  # a gtk.DrawingArea
canvas2 = FigureCanvas(f)  # a gtk.DrawingArea
p1_cov.add(canvas)
p2_cov.add(canvas2)


def quit(w,a=None):
    p1.p.quit(w)
    p2.p.quit(w)
    p3.p.quit(w)
    p4.p.quit(w)
    gtk.main_quit()

w.connect("delete-event",quit)
w.show_all()
gtk.main()#note - currently doesn't quit cleanly!

