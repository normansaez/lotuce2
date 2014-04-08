import FITS
import darc

#Takes camera instance
d=darc.Control('manta77')
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

d.Set("aravisCmd0",'ProgFrameTimeEnable=true;ProgFrameTimeAbs=50000;ExposureTimeAbs=58;')
dark_to_take =  100

exptime = int(d.Get('aravisCmd0').split(';')[2].split('=')[1])
print "Exposure Time %d" % exptime

for i in range(0, dark_to_take+1):
    #Preparing name for fits:
    if i == 0:
        fitsname = "bias_exp%s.fits" % str(exptime).zfill(2)
    else:
        exptime += 1000
        fitsname = "dark_exp%s.fits" % str(exptime).zfill(2)
    print "Taking %s ...." % fitsname
    d.Set("aravisCmd0",'ProgFrameTimeEnable=true;ProgFrameTimeAbs=50000;ExposureTimeAbs=%d;'%exptime)
    print "Exposure Time for %s is : %d [us]" % (fitsname, exptime)
    #Getting image from buffer
    stream=d.GetStream('manta77rtcPxlBuf')#a single frame
    #change the default shape of image (default shape is usually: (x*y,1))
    data = stream[0].reshape(pxlx,pxly)
    #writes a fits
    FITS.Write(data, fitsname, writeMode='a')
    print "done ...\n"
    

