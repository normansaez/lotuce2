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

streamBlock = d.GetStreamBlock('%srtcPxlBuf'%'all',1)#,block=1,flysave=options.directory+'/img.fits')
streams = streamBlock['%srtcPxlBuf'%'all']
count = 0
for stream in streams:
    data = stream[0].reshape((4*pxly,pxlx))
    fitsname = 'full.fits'#options.directory+"/img_%s.fits" % (str(count).zfill(3))
    FITS.Write(data, fitsname, writeMode='w')
    count += 1
    print data
