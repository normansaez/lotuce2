import FITS
import darc
import time
from optparse import OptionParser
from pprint import pprint
import numpy as np
import re

parse = OptionParser()
#parse.add_option('-c', '--camera', dest='camera', type='str', help='Camera num: 0,1,2,3 etc', default="0")
parse.add_option('-p', '--prefix', dest='prefix', type='str', help='Camera prefix: default all', default="both")
parse.add_option('-e', '--exptime', dest='exptime', type=int, help='Value for ExposureTimeAbs', default=1000)
#parse.add_option('-i', '--nimg', dest='nimg', type=int, help='Number of images', default=1)
parse.add_option('-t', '--time', dest='time', type=int, help='Image time in seconds', default=60)
(options , argv) = parse.parse_args()
#Takes camera instance
d=darc.Control(options.prefix)
#takes camera pixels (x,y)
pxlx =d.Get("npxlx")[0]
pxly =d.Get("npxly")[0]

info,ftime,fno=d.GetStream(options.prefix+"rtcStatusBuf")
line = info.tostring()
sts = re.search(r'Frame time .*s (.*)', line, re.M|re.I)
try:
    HZ_str = sts.group(1) 
    print "Hz from darc: %s"% HZ_str
    hz = float(HZ_str.split('(')[1].split('Hz)')[0])
except:
    pass
print "number of images for %f [Hz] and %d time[seconds]: %d images to take" % (hz, options.time,int(hz*options.time))
img_to_take =  int(hz*options.time)#options.nimg
exptime = options.exptime
d.Set("aravisCmdAll",'ExposureTimeAbs=%d;'% exptime)
d.Set("aravisGet","?0:ExposureTimeAbs")
exptime=int(d.Get("aravisGet"))
t0 = time.clock()
streamBlock = d.GetStreamBlock('%srtcPxlBuf'%options.prefix,img_to_take,block=1,flysave='img.fits')
t1 = time.clock()
print "%f" % (t1-t0)
streams = streamBlock['%srtcPxlBuf'%options.prefix]
count = 0
for stream in streams:
    data = stream[0].reshape((2*pxly,pxlx))
    fitsname = "img_%s.fits" % (str(count).zfill(3))
    FITS.Write(data, fitsname, writeMode='w')
    count += 1
