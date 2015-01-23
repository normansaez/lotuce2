import darc
import time
import sys
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--on', dest='on', action='store_false' , help='Enable trigger')
parser.add_argument('-p', '--prefix', dest='prefix', type=str, help='Camera prefix: default all', default="all")
(options, unknown) = parser.parse_known_args()
ncam_selector = { "cam0": 1, "cam1": 1, "cam2":1, "cam3":1, "both":2, "cam1cam2":2, "cam2cam3":2, "cam3cam0":2, "cam013":3,"all": 4}

ncam = ncam_selector[options.prefix]
d = darc.Control(options.prefix)

def set(camera, parameter, value):
    cam = "aravisCmd%d" % camera
    cmd = '%s=%s;' % (parameter, str(value))
    d.Set(cam, cmd)
    print sys._getframe().f_code.co_name,
    print "Cam%d => %s: %s" % (camera, parameter, str(value))

def get(camera, parameter):
    cmd = "?%d:%s" % (camera, parameter)
    d.Set('aravisGet',cmd)
    try:
        r = int(d.Get("aravisGet"))
    except ValueError, e:
        r = d.Get("aravisGet")
        print sys._getframe().f_code.co_name,
        print "Cam%d => %s: %s" % (cam, parameter, r)
        return r
    print sys._getframe().f_code.co_name,
    print "Cam%d => %s: %d" % (cam, parameter, r)
    return r

print "---------------"
for cam in range(0,ncam):
    x =  get(cam, 'Width')
    y  = get(cam, 'Height')
        
    get(cam, 'OffsetX')
    get(cam, 'OffsetY')
    print "####"
    offsetX = int((656 - x )/2.0)
    offsetY = int((492 - y)/2.0)
    
    set(cam, 'OffsetX', offsetX)
    set(cam, 'OffsetY', offsetY)
    print "---------------"

for cam in range(0,ncam):
    exptime =  get(cam, 'ExposureTimeAbs')
    exptime = 1000
    print "####"
    set(cam, 'ExposureTimeAbs', exptime)
    print "---------------"
    exptime =  get(cam, 'ExposureTimeAbs')
print "---------------"
for cam in range(0,ncam):
    trigger =  get(cam, 'TriggerSource')
    print "####"
    if options.on is True:
        set(cam, 'TriggerSource', 'Line1')
    else:
        set(cam, 'TriggerSource', 'Freerun')
    print "---------------"
    get(cam, 'TriggerSource')
    

#Fine tune ....
OffsetX = 254
OffsetY = 200
cam = 0
set(cam, 'OffsetX', OffsetX)
set(cam, 'OffsetY', OffsetY)

cam = 1
OffsetX = 252
OffsetY = 100
set(cam, 'OffsetX', OffsetX)
set(cam, 'OffsetY', OffsetY)

cam = 2
OffsetX = 100
OffsetY = 154
set(cam, 'OffsetX', OffsetX)
set(cam, 'OffsetY', OffsetY)

cam = 3
OffsetX = 172
OffsetY = 130
set(cam, 'OffsetX', OffsetX)
set(cam, 'OffsetY', OffsetY)

