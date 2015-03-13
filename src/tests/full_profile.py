#import gtk
import os
#from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
import numpy as np
#from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import FITS
cam0_nx = np.array([])
cam0_ny = np.array([])
f = FITS.Read('~/full.fits')#'800x200.fits')
#f = FITS.Read('~/800x200.fits')
data = f[1]
print data.shape
x = len(data)
axis = range(0,x)
for i in range(0,x):
    cam0_nx = np.append(cam0_nx, data[i,].sum())
cam0_nx = cam0_nx/4095.
count = 0
for i in axis:
    if cam0_nx[i] == 0:
        print "%d" % i
        count +=1
        cam0_nx[i] = 0.07
        if count == 4:
            count = 0
            print
cam0_fx = plt.figure()#Figure(figsize=(5,4), dpi=30)
ax = cam0_fx.add_subplot(111)
ax.set_ylim(0,x)
ax.invert_xaxis()
ax.plot(cam0_nx,axis,'-')
plt.show()
count = 0
delta = np.diff(cam0_nx)
axis = range(0, len(delta))
cam0_fx = plt.figure()#Figure(figsize=(5,4), dpi=30)
ax = cam0_fx.add_subplot(111)
ax.set_ylim(0,x)
ax.invert_xaxis()
ax.plot(delta,axis,'-')
plt.show()

