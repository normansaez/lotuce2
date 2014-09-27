import FITS
import darc
import time
from optparse import OptionParser
from pprint import pprint
parse = OptionParser()
#parse.add_option('-c', '--camera', dest='camera', type='str', help='Camera num: 0,1,2,3 etc', default="0")
parse.add_option('-p', '--prefix', dest='prefix', type='str', help='Camera prefix: default all', default="all")
parse.add_option('-e', '--exptime', dest='exptime', type=int, help='Value for ExposureTimeAbs', default=12000)
parse.add_option('-i', '--nimg', dest='nimg', type=int, help='Number of images', default=100)
(options , argv) = parse.parse_args()
#Takes camera instance
d=darc.Control(options.prefix)
#Get the buffer and set as bg Image
#bg=d.SumData('rtcPxlBuf',1,'f')[0]/1
#d.Set('bgImage',bg)
#bg = d.Get("bgImage")

#takes camera pixels (x,y)
pxlx =d.Get("npxlx")[0]
pxly =d.Get("npxly")[0]
print pxlx
print pxly
#change the default shape of image (default shape is usually: (x*y,1))
#data = bg.reshape(pxlx,pxly)
#writes a fits
#fitsname = "test.fits"
#FITS.Write(data, fitsname, writeMode='a')

#Set exposure time to 58 micro seconds (min:58[us] - max 60[s])
#>>> c.Get('aravisCmd0')
#'ProgFrameTimeEnable=true;ProgFrameTimeAbs=50000;ExposureTimeAbs=58;'

img_to_take =  options.nimg
#d.Set("aravisGet","?0:ExposureTimeAbs")
#try:
#    exptime=int(d.Get("aravisGet"))
#except:
#    print "Can't get exptime"
#    exptime=-1
#print "Current ExposureTimeAbs =%d" % exptime
#print "Setting to %d in all cameras" % options.exptime
times_x = [12000]#,5000,10000,12000,15000]
fps_e = []
for exptime in times_x:
    d.Set("aravisCmdAll",'ExposureTimeAbs=%d;'% exptime)
    d.Set("aravisGet","?0:ExposureTimeAbs")
    exptime=int(d.Get("aravisGet"))
    print "New Exposure Time %d" % exptime
    average = 0
    t1 = 0
    for i in range(0, img_to_take+1):
        t0 = t1 #time.clock()
        #Preparing name for fits:
        fitsname = "img_%s.fits" % str(i).zfill(3)
#        print "Taking %d ...." % i
        #Getting image from buffer
        t1 = time.clock()
#        stream=d.GetStream('%srtcPxlBuf'%options.prefix)#a single frame
        streamBlock = d.GetStreamBlock('%srtcPxlBuf'%options.prefix,img_to_take)  # hardniter frames - as a dict
        pprint(streamBlock)
        break
        #change the default shape of image (default shape is usually: (x*y,1))
        data = stream[0].reshape((2*pxly,pxlx))
    #    data = stream[0].reshape(pxlx,pxly)
        #writes a fits
        FITS.Write(data, fitsname, writeMode='w')
        fps = 1./ (t1 - t0)
        print fps
#    print fps_e

