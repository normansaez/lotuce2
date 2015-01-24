import sys


def get_Mbps(hz, y):
    x = 50#656#50#200#656
#    y = 492#50#200#492#120#492
#    hz = (1./exp_time)*1e6
#    print hz
    Mbps = (x*y*hz*2.*8.)/1e6
    return hz, Mbps

hz = float(sys.argv[1])
y = float(sys.argv[2])
hz, Mbps = get_Mbps(hz, y)
exp_time = 1000
print "exp [us]     : %.2f" % exp_time
print "Hz           : %.2f -> AnyEdge: %.2f" % (hz, hz/2.)
print "Mbps         : %.2f" % Mbps
if Mbps*2 < 1000:
    print "Mbps *2 cam  : %.2f" % (Mbps*2)
if Mbps*3 < 1000:
    print "Mbps *3 cam  : %.2f" % (Mbps*3)
if Mbps*4 < 1000:
    print "Mbps *4 cam  : %.2f" % (Mbps*4)
