import FITS
import darc
import time
import argparse 
from pprint import pprint
import numpy as np
import re
import os
import glob

d=darc.Control('all')
#takes camera pixels (x,y)
pxlx =d.Get("npxlx")[0]
pxly =d.Get("npxly")[0]

streamBlock = d.GetStreamBlock('%srtcCentBuf'%'all',1)#,block=1,flysave=options.directory+'/img.fits')
streams = streamBlock['%srtcCentBuf'%'all']
for stream in streams:
    print stream[0]
    print stream[0].shape
    data = stream[0]
    fitsname = 'centroid.fits'#options.directory+"/img_%s.fits" % (str(count).zfill(3))
    FITS.Write(data, fitsname, writeMode='w')
