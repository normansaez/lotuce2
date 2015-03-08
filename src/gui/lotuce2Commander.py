import darc
import plot
import gtk
import os
from darcaravis import DarcAravis
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from numpy import arange, sin, pi, array, append
import numpy as np
from matplotlib.figure import Figure


#takes camera pixels (x,y)
_prefix = 'all'
d = darc.Control(_prefix)
def update_profile():
    pxlx =d.Get("npxlx")[0]
    pxly =d.Get("npxly")[0]
    print pxlx
    print pxly
    stream=d.GetStream('%srtcPxlBuf'% _prefix)
    mydata = stream[0].reshape((4*pxly,pxlx))
    
    xi_cam0 = 200#492#200
    xf_cam0 = 400#984#400
    yi_cam0 = 0#0
    yf_cam0 = 200#656#200
    
    xi_cam1 = 0#0
    xf_cam1 = 200#492#200
    yi_cam1 = 0#0
    yf_cam1 = 200#656#200
    
    xi_cam2 = 400#0
    yi_cam2 = 0#0
    xf_cam2 = 600#492#200
    yf_cam2 = 200#656#200
    
    xi_cam3 = 600#0
    yi_cam3 = 0#0
    xf_cam3 = 800#492#200
    yf_cam3 = 200#656#200
    
    #data per camera:
    cam0 = mydata[xi_cam0:xf_cam0,yi_cam0:yf_cam0]
    cam1 = mydata[xi_cam1:xf_cam1,yi_cam1:yf_cam1]
    cam2 = mydata[xi_cam2:xf_cam2,yi_cam2:yf_cam2]
    cam3 = mydata[xi_cam3:xf_cam3,yi_cam3:yf_cam3]
    return cam0, cam1, cam2, cam3 

#####################
def quit(w,a=None):
    p1.p.quit(w)
    p2.p.quit(w)
    p3.p.quit(w)
    p4.p.quit(w)
    gtk.main_quit()
#####################

cam0, cam1, cam2, cam3= update_profile()
x = len(cam0)
cam0_nx = np.array([])
cam0_ny = np.array([])
cam1_nx = np.array([])
cam1_ny = np.array([])
cam2_nx = np.array([])
cam2_ny = np.array([])
cam3_nx = np.array([])
cam3_ny = np.array([])

for i in range(0,x):
    cam0_nx = np.append(cam0_nx, cam0[i,].sum())
    cam0_ny = np.append(cam0_ny, cam0[:,i].sum())
    cam1_nx = np.append(cam1_nx, cam1[i,].sum())
    cam1_ny = np.append(cam1_ny, cam1[:,i].sum())
    cam2_nx = np.append(cam2_nx, cam2[i,].sum())
    cam2_ny = np.append(cam2_ny, cam2[:,i].sum())
    cam3_nx = np.append(cam3_nx, cam3[i,].sum())
    cam3_ny = np.append(cam3_ny, cam3[:,i].sum())
axis = range(0,x)

cam0_fx = Figure(figsize=(5,4), dpi=30)
ax = cam0_fx.add_subplot(111)
ax.set_ylim(0,x)
ax.plot(cam0_nx,axis,'-')

cam0_fy = Figure(figsize=(5,4), dpi=30)
ax2 = cam0_fy.add_subplot(111)
ax2.set_xlim(0,x)
ax2.plot(axis,cam0_ny,'-')
#--------------------------------------------------
cam1_fx = Figure(figsize=(5,4), dpi=30)
ax = cam1_fx.add_subplot(111)
ax.set_ylim(0,x)
ax.plot(cam1_nx,axis,'-')

cam1_fy = Figure(figsize=(5,4), dpi=30)
ax2 = cam1_fy.add_subplot(111)
ax2.set_xlim(0,x)
ax2.plot(axis,cam1_ny,'-')
#--------------------------------------------------
cam2_fx = Figure(figsize=(5,4), dpi=30)
ax = cam2_fx.add_subplot(111)
ax.set_ylim(0,x)
ax.plot(cam2_nx,axis,'-')

cam2_fy = Figure(figsize=(5,4), dpi=30)
ax2 = cam2_fy.add_subplot(111)
ax2.set_xlim(0,x)
ax2.plot(axis,cam2_ny,'-')
#--------------------------------------------------
cam3_fx = Figure(figsize=(5,4), dpi=30)
ax = cam3_fx.add_subplot(111)
ax.set_ylim(0,x)
ax.plot(cam3_nx,axis,'-')

cam3_fy = Figure(figsize=(5,4), dpi=30)
ax2 = cam3_fy.add_subplot(111)
ax2.set_xlim(0,x)
ax2.plot(axis,cam3_ny,'-')
#--------------------------------------------------
gtk.gdk.threads_init()
configdir = "/opt/darc/conf"
w=gtk.Window()
w.set_default_size(800,700)
v=gtk.VBox()
h1=gtk.HBox()
h2=gtk.HBox()
h3=gtk.HBox()
h4=gtk.HBox()
#-----------------
f1=gtk.Frame()
f2=gtk.Frame()
f3=gtk.Frame()
f4=gtk.Frame()
#----------------------
v.pack_start(h4,True)
v.pack_start(h1,True)
v.pack_start(h2,True)
v.pack_start(h3,True)
#----- two plots:
cam_profile=gtk.Frame()
p2_cov=gtk.Frame()
#----------------------
h1.pack_start(f1,True)
h1.pack_start(f2,True)
h1.pack_start(cam_profile,True)

h2.pack_start(f3,True)
h2.pack_start(f4,True)
h2.pack_start(p2_cov,True)
w.add(v)
#w.add(h)
p1=plot.DarcReader([], prefix=_prefix, dec=125, configdir=configdir, withScroll=1, window=f1, showPlots=0)
p2=plot.DarcReader([], prefix=_prefix, dec=125, configdir=configdir, withScroll=1, window=f2, showPlots=0)
p3=plot.DarcReader([], prefix=_prefix, dec=125, configdir=configdir, withScroll=1, window=f3, showPlots=0)
p4=plot.DarcReader([], prefix=_prefix, dec=125, configdir=configdir, withScroll=1, window=f4, showPlots=0)
p1.p.loadFunc("/home/lotuce2/lotuce2/src/gui/cam0.xml")
p2.p.loadFunc("/home/lotuce2/lotuce2/src/gui/cam1.xml")
p3.p.loadFunc("/home/lotuce2/lotuce2/src/gui/cam2.xml")
p4.p.loadFunc("/home/lotuce2/lotuce2/src/gui/cam3.xml")
#p1.subWid.hide()
#p2.subWid.hide()

#f = Figure(figsize=(5,4), dpi=100)
#a = f.add_subplot(111)
#t = arange(0.0,3.0,0.01)
#s = sin(2*pi*t)
#a.plot(t,s)

canvas_c1_fx = FigureCanvas(cam1_fx)  # a gtk.DrawingArea
canvas_c1_fy = FigureCanvas(cam1_fy)  # a gtk.DrawingArea
cam_profile.add(canvas_c1_fx)
p2_cov.add(canvas_c1_fy)


w.connect("delete-event",quit)
w.show_all()
gtk.main()#note - currently doesn't quit cleanly!

