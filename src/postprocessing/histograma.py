#!/usr/bin/python
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
from matplotlib.pylab import hist, show
import mmap

if __name__=="__main__":
    usage = '''
    '''
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-f', '--filename', dest='filename', type=str, help='Path to get txt source', default=None)
    parser.add_argument('-e', '--experiment', dest='experiment', type=str, help='Experiment name', default='A')
    parser.add_argument('-l', '--limit', dest='limit', type=int, help='Default limit to plot', default=None)#131100)#393300)#786600)#None)

    (options, unknown) = parser.parse_known_args()

    if options.filename is None:
        print "No filename to be to analised, you need give a path for the filename"
        print "Use -f /path/to/the/filename"
        sys.exit(-1)

    options.filename = os.path.normpath(options.filename)
    basename = os.path.basename(options.filename)

print "GO !!"
axis_x = []
fnos = []
fns = []
filename = os.path.normpath(options.filename)
print filename
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
del axis_x[-1]
np_fnos = np.array(fnos)
print (np_fnos[1:]-np_fnos[:-1]).max()
print (np_fnos[1:]-np_fnos[:-1]).min()
c_01 = 0
c_2_100 = 0
c_100_200 = 0
c_200_500 = 0
c_500_1000= 0
c_1000_3000 = 0

for j in range(0,i-1):
    fno_id = np_fnos[j+1] - np_fnos[j]
    fns.append(fno_id)
    if fno_id <= 1:
        c_01 += 1
    if fno_id > 1 and fno_id <= 100:
        c_2_100 += 1
    if fno_id > 100 and fno_id <= 200:
        c_100_200 += 1
    if fno_id > 200 and fno_id <= 500:
        c_200_500 += 1
    if fno_id > 500 and fno_id <= 1000:
        c_500_1000 += 1
    if fno_id > 1000 and fno_id <= 3000:
        c_1000_3000 += 1

print len(axis_x)
print len(fns)
#ploy
print "stats"
npfns = np.array(fns)
print npfns.min()
print npfns.max()
print npfns.mean()
print npfns.std()
print "ranges"
print c_01
print c_2_100
print c_100_200
print c_200_500
print c_500_1000
print c_1000_3000
print "ranges"
t = len(fns)*1.
print (c_01/t)*100.
print (c_2_100/t)*100.
print (c_100_200/t)*100.
print (c_200_500/t)*100.
print (c_500_1000/t)*100.
print (c_1000_3000/t)*100.


from math import ceil
bins = 20#range(0,3000,10)#[0,10,100,200,500,100,3000]#range(0,200,10)
print bins
hist(fns,bins,normed=True,log=True)
show()
