import sys


def get_Mbps(hz, x=200, y=200):
    Mbps = (x*y*hz*2.*8.)/1e6
    return hz, Mbps

hz = float(sys.argv[1])
try:
    x = float(sys.argv[2])
except:
    x = 200
try:
    y = float(sys.argv[3])
except:
    y = 200
hz, Mbps = get_Mbps(hz,x,y)
exp_time = 1000
print "(x,y)        : (%d,%d)" % (x,y)
print "exp [us]     : %.2f" % exp_time
print "Hz           : %.2f -> AnyEdge: %.2f" % (hz, hz/2.)
print "Mbps         : %.2f" % Mbps
#if Mbps*2 < 1000:
#    print "Mbps *2 cam  : %.2f" % (Mbps*2)
#if Mbps*3 < 1000:
#    print "Mbps *3 cam  : %.2f" % (Mbps*3)
#if Mbps*4 < 1000:
print "Mbps *4 cam  : %.2f" % (Mbps*4)
