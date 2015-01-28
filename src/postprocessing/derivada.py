import FITS
import glob
import sys
import os
from pylab import grid#imshow,show
from pylab import xticks
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import argparse 
import numpy as np
from math import floor
from matplotlib import ticker
#COLOR CONST
BLUE     = '\033[34m'
RED      = '\033[31m'
GREEN    = '\033[32m'
YELLOW   = '\033[33m'
BLACK    = '\033[30m'
CRIM     = '\033[36m'
NO_COLOR = '\033[0m'


if __name__=="__main__":
    print "Calibrating centroid pattern ..."
    usage = '''
    '''
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-d', '--filename', dest='filename', type=str, help='Path to get images', default=None)

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
f = open(filename,'r')
filehandler = f.readlines()
f.close()

i = 0
for line in filehandler:
    line = line.rstrip('\n').split(' ')
    ts = float(line[0])
    fno= float(line[1])
    fnos.append(fno)
#    axis_x.append(i)
    i += 1
axis_x = [j for j in range(0,i-1)]
np_fnos = np.array(fnos)
print (np_fnos[1:]-np_fnos[:-1]).max()
print (np_fnos[1:]-np_fnos[:-1]).min()

for i in range(0,len(np_fnos)-1):
    fno_id = np_fnos[i+1] - np_fnos[i]
    fns.append(fno_id)
fig = plt.figure()
ax = plt.subplot(111)
ax.plot(axis_x, fns, 'r.',label='fno')
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
plt.title(r'img v.s $d(n) = id(n+1) - id(n)$ %s' % (basename))
plt.ylabel(r'$\Delta id(n) = id(n+1) - id(n)$')
plt.xlabel(r'image number')
#xticks(rotation='vertical')
formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True) 
formatter.set_powerlimits((-1,1)) 
ax.xaxis.set_major_formatter(formatter) 
ax.xaxis.grid(True)
grid()
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig(basename+'-id.png')
print "%d total"% (len(axis_x))
plt.show()
