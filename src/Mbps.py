import sys


def get_Mbps(exp_time):
    x = 656
    y = 120#492
    hz = (1./exp_time)*1e6
    Mbps = (x*y*hz*2.*8.)/1e6
    return hz, Mbps

exp_time = float(sys.argv[1])
hz, Mbps = get_Mbps(exp_time)
print "exp [us]     : %.2f" % exp_time
print "Hz           : %.2f" % hz
print "Mbps         : %.2f" % Mbps

if Mbps*2 > 1000:
    print "doesn't work"
