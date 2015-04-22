import FITS
import darc
import time
import argparse 
from pprint import pprint
import numpy as np
import re
import os
import glob
from pylab import grid#imshow,show
import matplotlib.pyplot as plt

prefix = "all"
d=darc.Control(prefix)
#takes camera pixels (x,y)
pxlx =d.Get("npxlx")[0]
pxly =d.Get("npxly")[0]
streamBlock = d.GetStreamBlock('%srtcCentBuf'%prefix,5)#,block=1,flysave=options.directory+'/img.fits')
streams = streamBlock['%srtcCentBuf'%prefix]
print len(streams)
print "###"
x0 = np.array([])
x1 = np.array([])
x2 = np.array([])
x3 = np.array([])
y0 = np.array([])
y1 = np.array([])
y2 = np.array([])
y3 = np.array([])
for stream in streams:
    print stream[0]
    print type(stream[0])
    print stream[0].shape
    data = stream[0]
#    fitsname = 'centroid.fits'#options.directory+"/img_%s.fits" % (str(count).zfill(3))
#    FITS.Write(data, fitsname, writeMode='w')
    x0 = np.append(x0,data[0])
    y0 = np.append(x0,data[1])

    x1 = np.append(x1,data[2])
    y1 = np.append(x1,data[3])

    x2 = np.append(x2,data[4])
    y2 = np.append(x2,data[5])

    x3 = np.append(x3,data[6])
    y3 = np.append(x3,data[7])

cov_x = np.array([])
cov_x = np.append(cov_x, np.cov(x0,x1)[0][1]) 
cov_x = np.append(cov_x, np.cov(x0,x2)[0][1])
cov_x = np.append(cov_x, np.cov(x0,x3)[0][1])
cov_x = np.append(cov_x, np.cov(x1,x2)[0][1])
cov_x = np.append(cov_x, np.cov(x1,x3)[0][1])
cov_x = np.append(cov_x, np.cov(x2,x3)[0][1])

cov_y = np.array([])
cov_y = np.append(cov_y, np.cov(y0,y1)[0][1]) 
cov_y = np.append(cov_y, np.cov(y0,y2)[0][1])
cov_y = np.append(cov_y, np.cov(y0,y3)[0][1])
cov_y = np.append(cov_y, np.cov(y1,y2)[0][1])
cov_y = np.append(cov_y, np.cov(y1,y3)[0][1])
cov_y = np.append(cov_y, np.cov(y2,y3)[0][1])


baselines = [2,10,15,20,50,120]

fig = plt.figure()
ax = plt.subplot(111)
ax.plot(baselines, cov_x,'ro-',label=r'$COV(X_{i},X_{i+1})$')
ax.plot(baselines, cov_y,'bo-',label=r'$COV(Y_{i},Y_{i+1})$')
x = ax.get_position()
plt.title(r'COV(X,Y) v/s Baseline')
plt.ylabel(r'$COV(XY_{i},XY_{i+1})$')
plt.xlabel(r'baseline')
ax.xaxis.grid(True)
ax.yaxis.grid(True)
ax.legend(loc='center left', bbox_to_anchor=(0.75, 0.92))
plt.savefig('covx.png')
#plt.show()

covariances = open('covariances.txt','w')
for i in range(cov_x):
    covariances.write(cov_x[i])
    covariances.write(' ')
    covariances.write(cov_y[i])
    covariances.write(' \n')

