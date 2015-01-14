import FITS
import darc
import time
import argparse 
from pprint import pprint
import numpy as np
import re
import os
import glob

parse = argparse.ArgumentParser()
#parse.add_argument('-c', '--camera', dest='camera', type='str', help='Camera num: 0,1,2,3 etc', default="0")
parse.add_argument('-p', '--prefix', dest='prefix', type=str, help='Camera prefix: default all', default="all")
#parse.add_argument('-e', '--exptime', dest='exptime', type=int, help='Value for ExposureTimeAbs', default=1000)
parse.add_argument('-d', '--directory', dest='directory', type=str, help='directory to be store the images', default=None)
parse.add_argument('-t', '--time', dest='time', type=int, help='Image time in seconds', default=1)
(options, unknown) = parse.parse_known_args()

if options.directory is None:
    path, fil = os.path.split(os.path.abspath(__file__))
    current =  str(time.strftime("%Y_%m_%d", time.gmtime()))
    current_dir = glob.glob(path+'/201*[0-90-9].*')
    current_dir.sort(key=os.path.getmtime)
    try:
        last = current_dir[-1]
        adquisition_number = int(last.split('/')[-1].split('.')[1]) + 1
        dir_name = current+'.'+ str(adquisition_number)
    except IndexError, e:
        dir_name = current+'.0'
    options.directory = path+'/'+dir_name
    if not os.path.exists(options.directory):
        print "Creating dir :%s" % options.directory
        os.makedirs(options.directory)

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
#exptime = options.exptime
#d.Set("aravisCmdAll",'ExposureTimeAbs=%d;'% exptime)
#d.Set("aravisGet","?0:ExposureTimeAbs")
#exptime=int(d.Get("aravisGet"))

#t0 = time.clock()
streamBlock = d.GetStreamBlock('%srtcPxlBuf'%options.prefix,img_to_take,block=1,flysave=options.directory+'/img.fits')
#t1 = time.clock()
#print "%f Hz" % (1./(t1-t0))
print "Images stored in : %s" % options.directory

#streams = streamBlock['%srtcPxlBuf'%options.prefix]
#count = 0
#for stream in streams:
#    data = stream[0].reshape((4*pxly,pxlx))
#    fitsname = options.directory+"/img_%s.fits" % (str(count).zfill(3))
#    FITS.Write(data, fitsname, writeMode='w')
#    count += 1
