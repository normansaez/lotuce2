import sys
import os
from pylab import grid#imshow,show
#from pylab import xticks
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import argparse 
import datetime
import numpy as np
from math import floor
from matplotlib import ticker
from matplotlib.dates import date2num
#from matplotlib import rcParams
from scipy.interpolate import UnivariateSpline
import mmap

#rcParams.update({'font.size': 18, 'text.usetex': True})
#rcParams.update({'font.size': 18, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})

if __name__=="__main__":
    print "Calibrating centroid pattern ..."
    usage = '''
    '''
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-d', '--filename', dest='filename', type=str, help='Path to get images', default=None)
    parser.add_argument('-l', '--limit', dest='limit', type=int, help='Default limit to plot', default=None)#131100)#393300)#786600)#None)

    (options, unknown) = parser.parse_known_args()

    if options.filename is None:
        print "No directory with images to analisis is given, you need give a path with a directory with images"
        print "Use -d /path/directory/images/"
        sys.exit(-1)

    options.filename = os.path.normpath(options.filename)
    basename = os.path.basename(options.filename)

print "GO !!"
axis_x = []
fnos = []
fns = []
filename = os.path.normpath(options.filename)
print filename
print "mmap ok"
i = 0
with open(filename, "r+b") as f:
    map = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
    for line in iter(map.readline, ""):
        line = line.rstrip('\n').split(' ')
        ts = float(line[0])
        fno= float(line[1])
        fnos.append(fno)
        d = datetime.datetime.fromtimestamp(ts)
        axis_x.append(d)
        i += 1
        if i == options.limit:
            break
    #axis_x = [j for j in range(0,i-1)]
del axis_x[-1]
np_fnos = np.array(fnos)
#print (np_fnos[1:]-np_fnos[:-1]).max()
#print (np_fnos[1:]-np_fnos[:-1]).min()

for j in range(0,i-1):
    fno_id = np_fnos[j+1] - np_fnos[j]
    fns.append(fno_id)
print len(axis_x)
print len(fns)
