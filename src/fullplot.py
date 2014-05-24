#!/usr/bin/env python
import FITS
from pylab import imshow,show
import matplotlib.pyplot as plt
import numpy as np
import glob
import time

all_fits = glob.glob('*.fits')
#plt.ion()
#plt.show()
#plt.gca().invert_yaxis()
for fits_name in all_fits:
    f = FITS.Read(fits_name)[1]
    #The subplot() command specifies numrows, numcols, fignum 
    nx = np.array([])
    for i in range(0,984):
        nx = np.append(nx,f[i,].sum())
    y = range(0,984)
    
    fig = plt.figure(1)
#    plt.subplot(223)
    ax = fig.add_subplot(2,2,3)
    ax.set_xlim(0,656)
    ax.set_ylim(0,984)
    ax.autoscale(False)
#    ax.set_adjustable('box-forced')
    ax.imshow(f)
#    plt.subplot(224)
    ax2 = fig.add_subplot(2,2,4,sharey=ax)
#    ax2.set_xlim(0,656)
    ax2.set_ylim(0,984)
    ax2.autoscale(False,axis='y')
    ax2.plot(nx,y,'-')
    ny = np.array([])
    for i in range(0,656):
        ny = np.append(ny,f[:,i].sum())
    x = range(0,656)
#    plt.subplot(221)
    ax4 = fig.add_subplot(2,2,1,sharex=ax)
    ax4.set_xlim(0,656)
    ax4.autoscale(False,axis='x')
#    ax4.set_ylim(0,984)
    ax4.plot(x,ny,'-')

#    plt.draw()
#    time.sleep(0.05)
    plt.show()
    
