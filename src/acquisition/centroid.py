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
for stream in streams:
    print stream[0]
    print type(stream[0])
    print stream[0].shape
    data = stream[0]
#    fitsname = 'centroid.fits'#options.directory+"/img_%s.fits" % (str(count).zfill(3))
#    FITS.Write(data, fitsname, writeMode='w')
    x0 = np.append(x0,data[0])
    x1 = np.append(x1,data[2])
print x0
print x1
print "-----"
print np.cov(x0,x1)[0][1]
