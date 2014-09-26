import darc
prefix = "both"
d = darc.Control(prefix)

def set(camera, parameter, value):
    cam = "aravisCmd%d" % camera
    cmd = '%s=%s;' % (parameter, str(value))
    d.Set(cam, cmd)

def get(camera, parameter):
    cmd = '?%d=%s;' % (camera, parameter)
    d.Set("aravisGet",cmd)
    return int(d.Get("aravisGet"))

#cam0 = 76
#cam1 = 77
print "76 => cam 0"
print "77 => cam 0"
for cam in range(0,1+1):
    x =  get(cam, 'Width')
    print "Cam%d => Width: %d" % (cam, x)
    y  = get(cam, 'Height')
    print "Cam%d => Height: %d" % (cam, y)
    
    offsetX = int((656 - x )/2.0)
    offsetY = int((492 - y)/2.0)
    
    set(cam, 'OffsetX', offsetX)
    print "Cam%d => OffsetX: %d" % (cam, get(0,'OffsetX'))
    set(cam, 'OffsetY', offsetY)
    print "Cam%d => OffsetY: %d" % (cam, get(0,'OffsetY'))
#Cam0 => cam76 => Width: 200
#Cam0 => cam76 => Height: 200
#Cam0 => cam76 => OffsetX: 278
#Cam0 => cam76 => OffsetY: 146
#Cam1 => cam77 => Width: 200
#Cam1 => cam77 => Height: 200
#Cam1 => cam77 => OffsetX: 198
#Cam1 => cam77 => OffsetY: 146
