import darc
import time
import sys
import argparse 

prefix = "all"
d = darc.Control(prefix)

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

if __name__=="__main__":
    print "Get status"
    usage = '''
    '''
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-o', '--on', dest='on', action='store_true' , help='Enable trigger')

    (options, unknown) = parser.parse_known_args()

    print "76 => cam0"
    print "77 => cam1"
    print "60 => cam2"
    print "61 => cam3"
    for cam in range(0,3+1):
        print "---------------"
        trigger =  get(cam, 'TriggerSource')
        exptime =  get(cam, 'ExposureTimeAbs')
        exptime =  get(cam, 'Width')
        exptime =  get(cam, 'Height')
        exptime =  get(cam, 'OffsetX')
        exptime =  get(cam, 'OffsetY')
        print "---------------"
    
