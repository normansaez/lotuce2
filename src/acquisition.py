import FITS
import darc
import time
from optparse import OptionParser

parse = OptionParser()
#parse.add_option('-c', '--camera', dest='camera', type='str', help='Camera num: 0,1,2,3 etc', default="0")
parse.add_option('-p', '--prefix', dest='prefix', type='str', help='Camera prefix: default both', default="both")
parse.add_option('-e', '--exptime', dest='exptime', type=int, help='Value for ExposureTimeAbs', default=12000)
parse.add_option('-i', '--nimg', dest='nimg', type=int, help='Number of images', default=3000)
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
#print "Setting to %d in both cameras" % options.exptime
times_x = [3000,5000,10000,12000,15000]
fps_e = []
for exptime in times_x:
    d.Set("aravisCmdAll",'ExposureTimeAbs=%d;'% exptime)
    d.Set("aravisGet","?0:ExposureTimeAbs")
    exptime=int(d.Get("aravisGet"))
    print "New Exposure Time %d" % exptime
    average = 0
    t0 = time.clock()
    for i in range(0, img_to_take+1):
        #Preparing name for fits:
        fitsname = "img_exp%s.fits" % str(exptime).zfill(2)
#        print "Taking %d ...." % i
        #Getting image from buffer
        stream=d.GetStream('%srtcPxlBuf'%options.prefix)#a single frame
        #change the default shape of image (default shape is usually: (x*y,1))
        data = stream[0].reshape(2*pxlx,pxly)
        average += data.mean()
    #    data = stream[0].reshape(pxlx,pxly)
        #writes a fits
        FITS.Write(data, fitsname, writeMode='a')
    average = average /float(img_to_take)
    t1 = time.clock()
    fps = img_to_take/ (t1 - t0)
    fps_e.append(average)
    hz = (1./exptime)*1e6
    Mbps = (pxlx*pxly*hz*2.*8.)/1e6
    print ""
    print "Theory:  %dx%d = %.3f Hz.  %d num of img. Exptime: %d [us]. %.2f Mbps aprox" % (pxlx,pxly,hz, img_to_take,exptime, Mbps)
    print "Empirical: %dx%d = %.3f fps. %d num of img. Exptime: %d [us]" % (pxlx,pxly,fps, img_to_take, exptime)
    print "########"
    print fps_e

