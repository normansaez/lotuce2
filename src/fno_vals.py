#!/usr/bin/env python
import re
import darc
import pylab

#Setting up!
print "Setup"
plot_on = False
n_img = 50000
prefix = "both"
d = darc.Control(prefix)
#ExposureTimeAbs = 30000 (min:58-max:6e+07)
exptime = 2500#2200#9500#8000#1e6 #1s = 1
d.Set("aravisCmdAll",'ExposureTimeAbs=%d;'% exptime)
d.Set("aravisGet","?0:ExposureTimeAbs")
exptime_obtained =int(d.Get("aravisGet"))
print "exptime: %d [us]\n" % exptime_obtained
#-------------------------------------------------------------

#Getting data:
#data=d.GetStreamBlock("rtcPxlBuf",100,asArray=1)
data=d.GetStreamBlock("rtcPxlBuf",n_img,-1,asArray=1)

#-------------------------------------------------------------
#frame number
fno=data["rtcPxlBuf"][2]
print "fno"
#print fno
print "this should be an array with 1, if everything is ok."
print fno[1:]-fno[:-1]
print "max  %d" % (fno[1:]-fno[:-1]).max()
print "min  %d" % (fno[1:]-fno[:-1]).min()
print

#-------------------------------------------------------------
#timestamp
print "timestamp"
timestamp=data["rtcPxlBuf"][1]
#print timestamp
print "this should be an array with exptime in micro secs [us]"
print (timestamp[1:]-timestamp[:-1])*1e6
print "max  %.3f" % ((timestamp[1:]-timestamp[:-1])*1e6).max()
print "min  %.3f" % ((timestamp[1:]-timestamp[:-1])*1e6).min()
print "mean %.3f" % ((timestamp[1:]-timestamp[:-1])*1e6).mean()
#print "this should be an array with zero (or close to it)"
#print (timestamp[1:]-timestamp[:-1])*1e6 -exptime_obtained
print

#-------------------------------------------------------------
#status
info,ftime,fno=d.GetStream(prefix+"rtcStatusBuf")
line = info.tostring()
#Frame time 1.00187s (0.998133Hz)
sts = re.search(r'Frame time .*s (.*)', line, re.M|re.I)
try:
    hz = (1./exptime_obtained)*1e6
    print "expected Hz : %.3f Hz" % hz
    print "Hz from darc: ", sts.group(1)
#    print "sts: ", sts.group(1)
#    print "sts: ", sts.group(2)
    print 
except:
    pass
#-------------------------------------------------------------
#plot
if prefix == "both" and plot_on:
    pxls=data["rtcPxlBuf"][0]
    s1=pxls[:,:pxls.size/2].sum(1)
    s2=pxls[:,pxls.size/2:].sum(1)
    
    #Then have a look at s1 and s2:
    pylab.plot(s1)
    pylab.plot(s2)
    pylab.show()
    
