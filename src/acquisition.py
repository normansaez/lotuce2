import FITS
import darc

#Takes camera instance
d=darc.Control('both')
#Get the buffer and set as bg Image
#bg=d.SumData('rtcPxlBuf',1,'f')[0]/1
#d.Set('bgImage',bg)
#bg = d.Get("bgImage")

#takes camera pixels (x,y)
pxlx =d.Get("npxlx")[0]
pxly =d.Get("npxly")[0]

#change the default shape of image (default shape is usually: (x*y,1))
#data = bg.reshape(pxlx,pxly)
#writes a fits
#fitsname = "test.fits"
#FITS.Write(data, fitsname, writeMode='a')

#Set exposure time to 58 micro seconds (min:58[us] - max 60[s])
#>>> c.Get('aravisCmd0')
#'ProgFrameTimeEnable=true;ProgFrameTimeAbs=50000;ExposureTimeAbs=58;'

dark_to_take =  100
d.Set("aravisGet","?0:ExposureTimeAbs")
try:
    exptime=int(d.Get("aravisGet"))
except:
    print "Can't get exptime"
    exptime=-1
print exptime
print type(exptime)
#import sys
#sys.exit(0)

print "Exposure Time %d" % exptime

for i in range(0, dark_to_take+1):
    #Preparing name for fits:
    exptime  = 12000
    fitsname = "dark_exp%s.fits" % str(exptime).zfill(2)
    print "Taking %s ...." % fitsname
    d.Set("aravisCmdAll",'ExposureTimeAbs=%d;'%exptime)
    print "Exposure Time for %s is : %d [us]" % (fitsname, exptime)
    #Getting image from buffer
    stream=d.GetStream('bothrtcPxlBuf')#a single frame
    #change the default shape of image (default shape is usually: (x*y,1))
    data = stream[0].reshape(2*pxlx,pxly)
#    data = stream[0].reshape(pxlx,pxly)
    #writes a fits
    FITS.Write(data, fitsname, writeMode='a')
    print "done ...\n"
    

