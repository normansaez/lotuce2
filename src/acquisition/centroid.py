import FITS
import darc
import time
import argparse 
from pprint import pprint
import numpy as np
import re
import os
import glob

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

print np.cov(x0,x1)[0][1]
print np.cov(x0,x2)[0][1]
print np.cov(x0,x3)[0][1]
print np.cov(x1,x2)[0][1]
print np.cov(x1,x3)[0][1]
print np.cov(x2,x3)[0][1]

print np.cov(y0,y1)[0][1]
print np.cov(y0,y2)[0][1]
print np.cov(y0,y3)[0][1]
print np.cov(y1,y2)[0][1]
print np.cov(y1,y3)[0][1]
print np.cov(y2,y3)[0][1]

