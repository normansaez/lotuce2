import darc
prefix = "both"
d = darc.Control(prefix)
#cam0 =76
d.Set("aravisGet","?0:Width")
x =  int(d.Get("aravisGet"))
print "Cam0 => cam76 => Width: %d" % x
d.Set("aravisGet","?0:Height")
y = int(d.Get("aravisGet"))
print "Cam0 => cam76 => Height: %d" % y

cam76_offsetX = int((656 - x )/2.0)
cam76_offsetY = int((492 - y)/2.0)

d.Set("aravisCmd0",'OffsetX=%d;'% cam76_offsetX)
d.Set("aravisGet","?0:OffsetX")
print "Cam0 => cam76 => OffsetX: %d" % int(d.Get("aravisGet"))
d.Set("aravisCmd0",'OffsetY=%d;'% cam76_offsetY)
d.Set("aravisGet","?0:OffsetY")
print "Cam0 => cam76 => OffsetY: %d" % int(d.Get("aravisGet"))

#cam1 =77
d.Set("aravisGet","?1:Width")
x =  int(d.Get("aravisGet"))
print "Cam1 => cam77 => Width: %d" % x
d.Set("aravisGet","?1:Height")
y = int(d.Get("aravisGet"))
print "Cam1 => cam77 => Height: %d" % y

cam77_offsetX = int((656 - x )/2.0)
cam77_offsetY = int((492 - y)/2.0)

d.Set("aravisCmd1",'OffsetX=%d;'% cam77_offsetX)
d.Set("aravisGet","?1:OffsetX")
print "Cam1 => cam77 => OffsetX: %d" % int(d.Get("aravisGet"))
d.Set("aravisCmd1",'OffsetY=%d;'% cam77_offsetY)
d.Set("aravisGet","?1:OffsetY")
print "Cam1 => cam77 => OffsetY: %d" % int(d.Get("aravisGet"))

#Cam0 => cam76 => Width: 200
#Cam0 => cam76 => Height: 200
#Cam0 => cam76 => OffsetX: 278
#Cam0 => cam76 => OffsetY: 146
#Cam1 => cam77 => Width: 200
#Cam1 => cam77 => Height: 200
#Cam1 => cam77 => OffsetX: 198
#Cam1 => cam77 => OffsetY: 146
