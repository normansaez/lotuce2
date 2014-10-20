import darc
import time
import sys
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--prefix', dest='prefix', type=str, help='Darc prefix: default all', default="all")
parser.add_argument('-v', '--value'   , dest='value', type=str, help='value to set', default=None)
parser.add_argument('-l', '--label'   , dest='label', type=str, help='Name of feature, default Exposure Time', default="ExposureTimeAbs")
parser.add_argument('-c', '--camera', dest='camera', type=int , help='Singe camera to be commanded, otherwise, all', default=None)

(options, unknown) = parser.parse_known_args()

ncam_selector = { "cam0": 1, "cam1": 1, "cam2":1, "cam3":1, "cam0cam1":2, "cam1cam2":2, "cam2cam3":2, "cam3cam0":2, "cam013":3,"all": 4}
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

print """
Common commands
------------
TriggerSource
ExposureTimeAbs
Width
Height
OffsetX
OffsetY
SyncInLevels
PixelFormat

TriggerMode
TriggerActivation"
-------------
"""
ncam_init = 0
if options.camera is  not None:
    ncam = options.camera + 1
    ncam_init = options.camera

for cam in range(ncam_init, ncam):
    if options.value is not None:
        set(cam, options.label, options.value)
    else:
        get(cam, options.label
    
