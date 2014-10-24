import FITS
import darc
import time
from optparse import OptionParser
from pprint import pprint
import numpy as np

parse = OptionParser()
#parse.add_option('-c', '--camera', dest='camera', type='str', help='Camera num: 0,1,2,3 etc', default="0")
parse.add_option('-p', '--prefix', dest='prefix', type='str', help='Camera prefix: default all', default="all")
parse.add_option('-e', '--exptime', dest='exptime', type=int, help='Value for ExposureTimeAbs', default=1000)
parse.add_option('-i', '--nimg', dest='nimg', type=int, help='Number of images', default=40)
(options , argv) = parse.parse_args()
#Takes camera instance
d=darc.Control(options.prefix)
#takes camera pixels (x,y)
pxlx =d.Get("npxlx")[0]
pxly =d.Get("npxly")[0]

img_to_take =  options.nimg
exptime = options.exptime
d.Set("aravisCmdAll",'ExposureTimeAbs=%d;'% exptime)
d.Set("aravisGet","?0:ExposureTimeAbs")
exptime=int(d.Get("aravisGet"))
t0 = time.clock()
streamBlock = d.GetStreamBlock('%srtcPxlBuf'%options.prefix,img_to_take)
t1 = time.clock()
streams = streamBlock['%srtcPxlBuf'%options.prefix]
count = 0
for stream in streams:
    data = stream[0].reshape((2*pxly,pxlx))
    fitsname = "img_%s.fits" % (str(count).zfill(3))
    FITS.Write(data, fitsname, writeMode='w')
    count += 1
