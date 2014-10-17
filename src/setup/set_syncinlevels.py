import darc
import time
import sys
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--on', dest='on', action='store_true' , help='Enable trigger')
parser.add_argument('-p', '--prefix', dest='prefix', type=str, help='Camera prefix: default all', default="all")
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
    r = int(d.Get("aravisGet"))
    print sys._getframe().f_code.co_name,
    print "Cam%d => %s: %d" % (cam, parameter, r)
    return r

print "---------------"
for cam in range(0,3+1):
    exptime = 1
    print "####"
    set(cam, 'SyncInLevels', exptime)
    exptime =  get(cam, 'SyncInLevels')
    print "---------------"

