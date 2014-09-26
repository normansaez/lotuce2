import darc
import time
import sys

prefix = "both"
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
    r = int(d.Get("aravisGet"))
    print sys._getframe().f_code.co_name,
    print "Cam%d => %s: %d" % (cam, parameter, r)
    return r

print "76 => cam0"
print "77 => cam1"
print "---------------"
for cam in range(0,1+1):
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

if x == 200:
    print "200x200, defined offset:"
    #Cam0 => cam76 => OffsetX: 278
    #Cam0 => cam76 => OffsetY: 146
    set(0,'OffsetX', 278)
    set(0,'OffsetY', 146)
    #Cam1 => cam77 => OffsetX: 198
    #Cam1 => cam77 => OffsetY: 146
    set(1,'OffsetX', 198)
    set(1,'OffsetY', 146)

