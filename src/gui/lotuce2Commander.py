import darc
import plot
import gtk
import os
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
import numpy as np
from matplotlib.figure import Figure
from scipy.stats import norm


#DARC stuff
_prefix = 'all'
d_obj = darc.Control(_prefix)

int_max = (2**12 - 1. )# 0 to 2^(camera bits). As start from 0, it is needed get one value less
# funcs
def update_profile():
    pxlx =d_obj.Get("npxlx")[0]
    pxly =d_obj.Get("npxly")[0]
    print "x: %d" % pxlx
    print "y: %d" % pxly
    stream=d_obj.GetStream('%srtcPxlBuf'% _prefix)
    mydata = stream[0].reshape((4*pxly,pxlx))

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
    cam0 = mydata[xi_cam0:xf_cam0,yi_cam0:yf_cam0]
    cam1 = mydata[xi_cam1:xf_cam1,yi_cam1:yf_cam1]
    cam2 = mydata[xi_cam2:xf_cam2,yi_cam2:yf_cam2]
    cam3 = mydata[xi_cam3:xf_cam3,yi_cam3:yf_cam3]
    return cam0, cam1, cam2, cam3 

#####################
def quit(win,a=None):
    p1.p.quit(win)
    p2.p.quit(win)
    p3.p.quit(win)
    p4.p.quit(win)
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

c0 = cam0.max()
c1 = cam1.max()
c2 = cam2.max()
c3 = cam3.max()
 
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
#normalize according cameras:
cam0_nx = cam0_nx/int_max
cam0_ny = cam0_ny/int_max

cam1_nx = cam1_nx/int_max
cam1_ny = cam1_ny/int_max

cam2_nx = cam2_nx/int_max
cam2_ny = cam2_ny/int_max

cam3_nx = cam3_nx/int_max
cam3_ny = cam3_ny/int_max

#cam0_fx = Figure(figsize=(5,4), dpi=30)
cam0_fx = Figure(dpi=30, tight_layout=True)
ax = cam0_fx.add_subplot(111)
#ax.set_xlim(0,1)
ax.set_ylim(0,x)
ax.invert_xaxis()
ax.plot(cam0_nx,axis,'-')
#mu, std = norm.fit(cam0_nx)
#p = norm.pdf(axis, mu, std)
#ax.plot(axis, p, 'k', linewidth=2)

#cam0_fy = Figure(figsize=(5,4), dpi=30)
cam0_fy = Figure(dpi=30, tight_layout=True)
ax2 = cam0_fy.add_subplot(111)
ax2.set_xlim(0,x)
#ax2.set_ylim(0,1)
ax2.plot(axis,cam0_ny,'-')
#--------------------------------------------------
#cam1_fx = Figure(figsize=(5,4), dpi=30)
cam1_fx = Figure(dpi=30, tight_layout=True)
ax = cam1_fx.add_subplot(111)
#ax.set_xlim(0,1)
ax.set_ylim(0,x)
ax.plot(cam1_nx,axis,'-')

#cam1_fy = Figure(figsize=(5,4), dpi=30)
cam1_fy = Figure(dpi=30, tight_layout=True)
ax2 = cam1_fy.add_subplot(111)
ax2.set_xlim(0,x)
#ax2.set_ylim(0,1)
ax2.plot(axis,cam1_ny,'-')
#--------------------------------------------------
#cam2_fx = Figure(figsize=(5,4), dpi=30)
cam2_fx = Figure(dpi=30, tight_layout=True)
ax = cam2_fx.add_subplot(111)
#ax.set_xlim(0,1)
ax.set_ylim(0,x)
ax.invert_xaxis()
ax.plot(cam2_nx,axis,'-')

#cam2_fy = Figure(figsize=(5,4), dpi=30)
cam2_fy = Figure(dpi=30, tight_layout=True)
ax2 = cam2_fy.add_subplot(111)
ax2.set_xlim(0,x)
#ax2.set_ylim(0,1)
ax2.invert_yaxis()
ax2.plot(axis,cam2_ny,'-')
#--------------------------------------------------
#cam3_fx = Figure(figsize=(5,4), dpi=30)
cam3_fx = Figure(dpi=30, tight_layout=True)
ax = cam3_fx.add_subplot(111)
#ax.set_xlim(0,1)
ax.set_ylim(0,x)
ax.plot(cam3_nx,axis,'-')

#cam3_fy = Figure(figsize=(5,4), dpi=30)
cam3_fy = Figure(dpi=30, tight_layout=True)
ax2 = cam3_fy.add_subplot(111)
ax2.set_xlim(0,x)
#ax2.set_ylim(0,1)
ax2.invert_yaxis()
ax2.plot(axis,cam3_ny,'-')
#--------------------------------------------------
gtk.gdk.threads_init()
configdir = "/opt/darc/conf"
win=gtk.Window()
win.set_default_size(800,800)
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
#----- profiles: 2 per camera x,y
cam0_p_x=gtk.Frame()
cam0_p_y=gtk.Frame()

cam1_p_x=gtk.Frame()
cam1_p_y=gtk.Frame()

cam2_p_x=gtk.Frame()
cam2_p_y=gtk.Frame()

cam3_p_x=gtk.Frame()
cam3_p_y=gtk.Frame()

# labels: 1 per camera
cam0_l=gtk.Frame()
cam1_l=gtk.Frame()
cam2_l=gtk.Frame()
cam3_l=gtk.Frame()
c0_label = gtk.Label("cam0\n int max: %d\n sat: %.2f %% " % (c0,(c0/int_max)*100.))
c1_label = gtk.Label("cam1\n int max: %d\n sat: %.2f %% " % (c1,(c1/int_max)*100.))
c2_label = gtk.Label("cam2\n int max: %d\n sat: %.2f %% " % (c2,(c2/int_max)*100.))
c3_label = gtk.Label("cam3\n int max: %d\n sat: %.2f %% " % (c3,(c3/int_max)*100.))
cam0_l.add(c0_label)
cam1_l.add(c1_label)
cam2_l.add(c2_label)
cam3_l.add(c3_label)
#----------------------
hor1.pack_start(cam0_l,True)
hor1.pack_start(cam0_p_y,True)
hor1.pack_start(cam1_p_y,True)
hor1.pack_start(cam1_l,True)
#----------------------
hor2.pack_start(cam0_p_x,True)
hor2.pack_start(f0,True)
hor2.pack_start(f1,True)
hor2.pack_start(cam1_p_x,True)
#----------------------
hor3.pack_start(cam2_p_x,True)
hor3.pack_start(f2,True)
hor3.pack_start(f3,True)
hor3.pack_start(cam3_p_x,True)
#----------------------
hor4.pack_start(cam2_l,True)
hor4.pack_start(cam2_p_y,True)
hor4.pack_start(cam3_p_y,True)
hor4.pack_start(cam3_l,True)
#-------------------
win.add(ver1)

p1=plot.DarcReader([], prefix=_prefix, dec=125, configdir=configdir, withScroll=1, window=f0, showPlots=0)
p2=plot.DarcReader([], prefix=_prefix, dec=125, configdir=configdir, withScroll=1, window=f1, showPlots=0)
p3=plot.DarcReader([], prefix=_prefix, dec=125, configdir=configdir, withScroll=1, window=f2, showPlots=0)
p4=plot.DarcReader([], prefix=_prefix, dec=125, configdir=configdir, withScroll=1, window=f3, showPlots=0)
p1.p.loadFunc("/home/lotuce2/lotuce2/src/gui/cam0.xml")
p2.p.loadFunc("/home/lotuce2/lotuce2/src/gui/cam1.xml")
p3.p.loadFunc("/home/lotuce2/lotuce2/src/gui/cam2.xml")
p4.p.loadFunc("/home/lotuce2/lotuce2/src/gui/cam3.xml")
#p1.subWid.hide()
#p2.subWid.hide()

#fill up profiles
canvas_c0_fx = FigureCanvas(cam0_fx)  # a gtk.DrawingArea
canvas_c0_fy = FigureCanvas(cam0_fy)  # a gtk.DrawingArea
cam0_p_x.add(canvas_c0_fx)
cam0_p_y.add(canvas_c0_fy)

canvas_c1_fx = FigureCanvas(cam1_fx)  # a gtk.DrawingArea
canvas_c1_fy = FigureCanvas(cam1_fy)  # a gtk.DrawingArea
cam1_p_x.add(canvas_c1_fx)
cam1_p_y.add(canvas_c1_fy)

canvas_c2_fx = FigureCanvas(cam2_fx)  # a gtk.DrawingArea
canvas_c2_fy = FigureCanvas(cam2_fy)  # a gtk.DrawingArea
cam2_p_x.add(canvas_c2_fx)
cam2_p_y.add(canvas_c2_fy)

canvas_c3_fx = FigureCanvas(cam3_fx)  # a gtk.DrawingArea
canvas_c3_fy = FigureCanvas(cam3_fy)  # a gtk.DrawingArea
cam3_p_x.add(canvas_c3_fx)
cam3_p_y.add(canvas_c3_fy)

win.connect("delete-event",quit)
win.show_all()
gtk.main()#note - currently doesn't quit cleanly!

