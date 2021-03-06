#darc, the Durham Adaptive optics Real-time Controller.
#Copyright (C) 2013 Alastair Basden.

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as
#published by the Free Software Foundation, either version 3 of the
#License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.

#You should have received a copy of the GNU Affero General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#This is a configuration file for CANARY.
#Aim to fill up the control dictionary with values to be used in the RTCS.

#import correlation
import string
import FITS
import tel
import numpy
from pprint import pprint

ncam_selector = { "cam0": 1, "cam1": 1, "cam2":1, "cam3":1, "both":2, "cam1cam2":2, "cam2cam3":2, "cam3cam0":2, "cam013":3, "all": 4}
ncam = ncam_selector[prefix]

print "Using %d cameras"%ncam
#####################################
nacts_number = 54
subap_number = 1 #This means: subap_numberxsubap_number
pixel_number_x = 200#50#656#200#100#656#50
pixel_number_y = 200#50#2#10#60#320#480#492#200#100#492#50
exposure_time_val = 40000#12500#24000
OffsetX = 0
OffsetY = 0
#####################################
nacts = nacts_number
ncamThreads=numpy.ones((ncam,),numpy.int32)*1
npxly=numpy.zeros((ncam,),numpy.int32)
npxly[:]= pixel_number_y
npxlx=npxly.copy()
npxlx[:]=pixel_number_x
nsuby=npxlx.copy()
nsuby[:]= subap_number #sub aps [cam0_subap, cam1_subap] 
nsubx=nsuby.copy()#sub aps [cam0_subap, cam1_subap]  
nsub=nsubx*nsuby#This is used by rtc.
nsubaps=nsub.sum()#(nsuby*nsubx).sum()
individualSubapFlag=tel.Pupil(subap_number, int(subap_number/2.), 0, subap_number).subflag.astype("i")
pprint(individualSubapFlag)
subapFlag=numpy.ones((nsubaps,),"i")
pprint(subapFlag)
#print subapFlag.reshape(subap_number,subap_number)
for i in range(ncam):
    tmp=subapFlag[nsub[:i].sum():nsub[:i+1].sum()]
    tmp.shape=nsuby[i],nsubx[i]
    tmp[:]=individualSubapFlag
ncents=subapFlag.sum()*2
npxls=(npxly*npxlx).sum()

fakeCCDImage=None#(numpy.random.random((npxls,))*20).astype("i")

bgImage=None#FITS.Read("shimgb1stripped_bg.fits")[1].astype("f")#numpy.zeros((npxls,),"f")
darkNoise=None#FITS.Read("shimgb1stripped_dm.fits")[1].astype("f")
flatField=None#FITS.Read("shimgb1stripped_ff.fits")[1].astype("f")

subapLocation=numpy.zeros((nsubaps,6),"i")
nsubapsCum=numpy.zeros((ncam+1,),numpy.int32)
ncentsCum=numpy.zeros((ncam+1,),numpy.int32)
for i in range(ncam):
    nsubapsCum[i+1]=nsubapsCum[i]+nsub[i]
    ncentsCum[i+1]=ncentsCum[i]+subapFlag[nsubapsCum[i]:nsubapsCum[i+1]].sum()*2

# now set up a default subap location array...
#this defines the location of the subapertures.
subx=(npxlx-48)/nsubx
suby=(npxly-8)/nsuby
xoff=[24]*ncam
yoff=[4]*ncam
for k in range(ncam):
    for i in range(nsuby[k]):
        for j in range(nsubx[k]):
            indx=nsubapsCum[k]+i*nsubx[k]+j
            subapLocation[indx]=(yoff[k]+i*suby[k],yoff[k]+i*suby[k]+suby[k],1,xoff[k]+j*subx[k],xoff[k]+j*subx[k]+subx[k],1)

pxlCnt=numpy.ones((nsubaps,),"i")
print "############ ACA ##################"
print pxlCnt
## set up the pxlCnt array - number of pixels to wait until each subap is ready.  Here assume identical for each camera.
#for k in range(ncam):
#    # tot=0#reset for each camera
#    for i in range(nsub[k]):
#        indx=nsubapsCum[k]+i
#        #n=(subapLocation[indx,1]-1)*npxlx[k]+subapLocation[indx,4]
#        n=subapLocation[indx,1]*npxlx[k]#whole rows together...
#        pxlCnt[indx]=n
pxlCnt = pxlCnt*pixel_number_x*pixel_number_y
print pxlCnt
print "############ ACA ##################"
#The params are dependent on the interface library used.
"""
  //Parameters are:
  //bpp[ncam]
  //blocksize[ncam]
  //offsetX[ncam]
  //offsetY[ncam]
  //prio[ncam]
  //affinElSize
  //affin[ncam*elsize]
  //length of names (a string with all camera IDs, semicolon separated).
  //The names as a string.
  //recordTimestamp
"""
cameras_selected = { "cam0":["Allied Vision Technologies-50-0503342076"][:ncam],
                     "cam1":["Allied Vision Technologies-50-0503342077"][:ncam],
                     "cam2":["Allied Vision Technologies-50-0503347160"][:ncam],
                     "cam3":["Allied Vision Technologies-50-0503347161"][:ncam],
                     "both":["Allied Vision Technologies-50-0503342076","Allied Vision Technologies-50-0503342077"][:ncam],
                     "cam1cam2":["Allied Vision Technologies-50-0503342077","Allied Vision Technologies-50-0503347160"][:ncam],
                     "cam2cam3":["Allied Vision Technologies-50-0503347160","Allied Vision Technologies-50-0503347161"][:ncam],
                     "cam3cam0":["Allied Vision Technologies-50-0503347161","Allied Vision Technologies-50-0503342076"][:ncam],
                     "cam013":["Allied Vision Technologies-50-0503342076","Allied Vision Technologies-50-0503342077","Allied Vision Technologies-50-0503347161"][:ncam],
                     "all":["Allied Vision Technologies-50-0503342076","Allied Vision Technologies-50-0503342077","Allied Vision Technologies-50-0503347160","Allied Vision Technologies-50-0503347161"][:ncam]}
camList= cameras_selected[prefix]
camNames=string.join(camList,";")
print camNames
while len(camNames)%4!=0:
    camNames+="\0"
namelen=len(camNames)
cameraParams=numpy.zeros((6*ncam+3+(namelen+3)//4,),numpy.int32)
cameraParams[0:ncam]=12#8#8 bpp - cam0, cam1
cameraParams[ncam:2*ncam]=5184#block size
cameraParams[2*ncam:3*ncam]=0#x offset
cameraParams[3*ncam:4*ncam]=0#y offset
cameraParams[4*ncam:5*ncam]=50#priority
cameraParams[5*ncam]=1#affin el size
cameraParams[5*ncam+1:6*ncam+1]=8#affinity
cameraParams[6*ncam+1]=namelen#number of bytes for the name.
cameraParams[6*ncam+2:6*ncam+2+(namelen+3)//4].view("c")[:]=camNames
cameraParams[6*ncam+2+(namelen+3)//4]=0#record timestamp

rmx=numpy.random.random((nacts,ncents)).astype("f")

#camCommand="ExposureTimeAbs=%d;PixelFormat=Mono12;Width=%d;Height=%d;TriggerSource=Line1;TriggerMode=On;TriggerActivation=AnyEdge;" % (exposure_time_val, pixel_number_x, pixel_number_y)
#camCommand="ExposureTimeAbs=%d;PixelFormat=Mono12;Width=%d;Height=%d;TriggerSource=Freerun;TriggerMode=On;TriggerActivation=AnyEdge;" % (exposure_time_val, pixel_number_x, pixel_number_y)
#camCommand="Width=%d;Height=%d;OffsetX=%d;OffsetY=%d;ExposureTimeAbs=%d;PixelFormat=Mono12;TriggerSource=Freerun;TriggerMode=On;TriggerActivation=AnyEdge;" % (pixel_number_x, pixel_number_y, OffsetX, OffsetY, exposure_time_val)
camCommand="Width=%d;Height=%d;OffsetX=%d;OffsetY=%d;ExposureTimeAbs=%d;PixelFormat=Mono12;TriggerSource=Freerun;TriggerMode=On;TriggerActivation=RisingEdge;" % (pixel_number_x, pixel_number_y, OffsetX, OffsetY, exposure_time_val)
#camCommand="Width=%d;Height=%d;OffsetX=%d;OffsetY=%d;ExposureTimeAbs=%d;PixelFormat=Mono12;TriggerSource=Line1;TriggerMode=On;TriggerActivation=AnyEdge;" % (pixel_number_x, pixel_number_y, OffsetX, OffsetY, exposure_time_val)


control={
    "switchRequested":0,#this is the only item in a currently active buffer that can be changed...
    "pause":0,
    "go":1,
    "maxClipped":nacts,
    "refCentroids":None,
    "centroidMode":"CoG",#whether data is from cameras or from WPU.
    "windowMode":"basic",
    "thresholdAlgo":1,
    "reconstructMode":"simple",#simple (matrix vector only), truth or open
    "centroidWeight":None,
    "v0":numpy.ones((nacts,),"f")*32768,#v0 from the tomograhpcic algorithm in openloop (see spec)
    "bleedGain":0.0,#0.05,#a gain for the piston bleed...
    "actMax":numpy.ones((nacts,),numpy.uint16)*65535,#4095,#max actuator value
    "actMin":numpy.zeros((nacts,),numpy.uint16),#4095,#max actuator value
    "nacts":nacts,
    "ncam":ncam,
    "nsub":nsub,
    #"nsubx":nsubx,
    "npxly":npxly,
    "npxlx":npxlx,
    "ncamThreads":ncamThreads,
    "pxlCnt":pxlCnt,
    "subapLocation":subapLocation,
    "bgImage":bgImage,
    "darkNoise":darkNoise,
    "closeLoop":1,
    "flatField":flatField,#numpy.random.random((npxls,)).astype("f"),
    "thresholdValue":0.,#could also be an array.
    "powerFactor":1.,#raise pixel values to this power.
    "subapFlag":subapFlag,
    "fakeCCDImage":fakeCCDImage,
    "printTime":0,#whether to print time/Hz
    "rmx":rmx,#numpy.random.random((nacts,ncents)).astype("f"),
    "gain":numpy.ones((nacts,),"f"),
    "E":numpy.zeros((nacts,nacts),"f"),#E from the tomoalgo in openloop.
    "threadAffinity":None,
    "threadPriority":numpy.ones((ncamThreads.sum()+1,),numpy.int32)*10,
    "delay":0,
    "clearErrors":0,
    "camerasOpen":1,
    "camerasFraming":1,
    "cameraName":"libcamAravis.so",#"camfile",
    #"cameraName":"libcamera.so",
    "cameraParams":cameraParams,
    "mirrorName":"libmirror.so",
    "mirrorParams":None,
    "mirrorOpen":0,
    "frameno":0,
    "switchTime":numpy.zeros((1,),"d")[0],
    "adaptiveWinGain":0.5,
    "corrThreshType":0,
    "corrThresh":0.,
    "corrFFTPattern":None,#correlation.transformPSF(correlationPSF,ncam,npxlx,npxly,nsubx,nsuby,subapLocation),
#    "correlationPSF":correlationPSF,
    "nsubapsTogether":1,
    "nsteps":0,
    "addActuators":0,
    "actuators":None,#(numpy.random.random((3,52))*1000).astype("H"),#None,#an array of actuator values.
    "actSequence":None,#numpy.ones((3,),"i")*1000,
    "recordCents":0,
    "pxlWeight":None,
    "averageImg":0,
    "slopeOpen":1,
    "slopeParams":None,
    "slopeName":"librtcslope.so",
    "actuatorMask":None,
    "averageCent":0,
    "calibrateOpen":1,
    "calibrateName":"librtccalibrate.so",
    "calibrateParams":None,
    "corrPSF":None,
    "centCalData":None,
    "centCalBounds":None,
    "centCalSteps":None,
    "figureOpen":0,
    "figureName":"figureSL240",
    "figureParams":None,
    "reconName":"libreconmvm.so",
    "fluxThreshold":0,
    "printUnused":1,
    "useBrightest":0,
    "figureGain":1,
    "decayFactor":None,#used in libreconmvm.so
    "reconlibOpen":1,
    "maxAdapOffset":0,
    "version":" "*120,
    }
for i in range(ncam):
    control["aravisCmd%d"%i]=camCommand
pprint(control)

