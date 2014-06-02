import FITS
import darc
import time
from optparse import OptionParser
from pprint import pprint
import numpy as np

parse = OptionParser()
#parse.add_option('-c', '--camera', dest='camera', type='str', help='Camera num: 0,1,2,3 etc', default="0")
parse.add_option('-p', '--prefix', dest='prefix', type='str', help='Camera prefix: default both', default="both")
parse.add_option('-e', '--exptime', dest='exptime', type=int, help='Value for ExposureTimeAbs', default=12000)
parse.add_option('-i', '--nimg', dest='nimg', type=int, help='Number of images', default=100)
(options , argv) = parse.parse_args()
#Takes camera instance
d=darc.Control(options.prefix)
#takes camera pixels (x,y)
pxlx =d.Get("npxlx")[0]
pxly =d.Get("npxly")[0]

img_to_take =  options.nimg
exptime = 12000
d.Set("aravisCmdAll",'ExposureTimeAbs=%d;'% exptime)
d.Set("aravisGet","?0:ExposureTimeAbs")
exptime=int(d.Get("aravisGet"))
average = 0
t1 = 0
win = 0
lose = 0
failures = []
t0 = time.clock()
streamBlock = d.GetStreamBlock('%srtcPxlBuf'%options.prefix,img_to_take)
t1 = time.clock()
streams = streamBlock['%srtcPxlBuf'%options.prefix]

i = 1
width = 10
threshold = 1000
for stream in streams:
    data = stream[0].reshape((2*pxly,pxlx))
    #
#pprint(data)
    y = 820
    x = 557
    b077 = threshold<data[y-width:y+width,x-width:x+width].mean()
    y = 700
    x = 333
    b177 = threshold<data[y-width:y+width,x-width:x+width].mean()
    y = 913
    x = 320
    b277 = threshold<data[y-width:y+width,x-width:x+width].mean()
    y = 810
    x = 88
    b377 = threshold<data[y-width:y+width,x-width:x+width].mean()
    
    y = 256
    x = 190
    b076 = threshold<data[y-width:y+width,x-width:x+width].mean()
    y = 200
    x = 302
    b176 = threshold<data[y-width:y+width,x-width:x+width].mean()
    y = 306
    x = 308
    b276 = threshold<data[y-width:y+width,x-width:x+width].mean()
    y = 254
    x = 422
    b376 = threshold<data[y-width:y+width,x-width:x+width].mean()
    counter77 = '0b'+str(int(b377))+str(int(b277))+str(int(b177))+str(int(b077))
    
    counter76 = '0b'+str(int(b376))+str(int(b276))+str(int(b176))+str(int(b076))
    fitsname = "img_%s-%s-%s_%d_%d.fits" % (str(i).zfill(3),counter77,counter76,eval(counter77), eval(counter76))
    if eval(counter76) == eval(counter77):
        win += 1
    else:
        lose += 1
        print "ERROR",
        print "%s = %s ?" % (counter77,counter76),
        print "==> %s =! %s" % (eval(counter77),eval(counter76))
        failures.append(fitsname)
    data = np.concatenate((data[0:pxly,:],data[pxly:2*pxly,:]),axis=1)
    FITS.Write(data, fitsname, writeMode='w')
    i +=  1
print "OK : %d" % win
print "FAIL : %d" % lose
print "ds9 ",
for j in failures:
    print "%s " %j ,
