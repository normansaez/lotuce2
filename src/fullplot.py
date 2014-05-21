#!/usr/bin/env python
import FITS
from pylab import imshow,show
import matplotlib.pyplot as plt
import numpy as np
import glob
import time

all_fits = glob.glob('*.fits')
plt.ion()
plt.show()
plt.gca().invert_yaxis()
#plt.autoscale(False)
for fits_name in all_fits:
    f = FITS.Read(fits_name)[1]
    #The subplot() command specifies numrows, numcols, fignum 
    nx = np.array([])
    for i in range(0,984):
        nx = np.append(nx,f[i,].sum())
    y = range(0,984)
    
    plt.figure(1)
    plt.subplot(223)
    imshow(f)
    plt.subplot(224)
    plt.plot(nx,y,'-')
    #plt.gca().invert_yaxis()
    plt.gca().autoscale(False)
    ########
    ny = np.array([])
    for i in range(0,656):
        ny = np.append(ny,f[:,i].sum())
    x = range(0,656)
    plt.subplot(221)
    p1 = plt.plot(x,ny,'-')
    plt.draw()
    time.sleep(0.5)

    
