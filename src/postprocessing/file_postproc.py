import FITS
import glob
import sys
import os
from pylab import grid#imshow,show
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import argparse 
import numpy as np
from skimage.measure import regionprops
from skimage.measure import label
from math import floor
import matplotlib.patches as patches
from matplotlib.path import Path

#COLOR CONST
BLUE     = '\033[34m'
RED      = '\033[31m'
GREEN    = '\033[32m'
YELLOW   = '\033[33m'
BLACK    = '\033[30m'
CRIM     = '\033[36m'
NO_COLOR = '\033[0m'

def get_square(cx, cy, side, color='red'):
    verts = [
        (cx-side, cy-side), # left, bottom
        (cx-side, cy+side), # left, top
        (cx+side, cy+side), # right, top
        (cx+side, cy-side), # right, bottom
        (cx, cy), # ignored
        ]
    
    codes = [Path.MOVETO,
             Path.LINETO,
             Path.LINETO,
             Path.LINETO,
             Path.CLOSEPOLY,
             ]
    
    path = Path(verts, codes)
    
    patch = patches.PathPatch(path, facecolor='none', EdgeColor=color, lw=1)
    return patch


def bit_check(x, y, img, threshold, width):
    intensity = img[y-width:y+width,x-width:x+width].mean()
    print "(%.0f >= %.0f)" % (intensity, threshold),
    if intensity >= threshold:
        print " ON" 
        return 1
    print 
    return 0

def get_centroid(img):
    label_img = label(img)
    regions = regionprops(label_img)
    
    for props in regions:
        y0, x0 = props.centroid
        return floor(y0), floor(x0)
    return -1, -1

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
pattern_cam0 = []
pattern_cam1 = []
pattern_cam2 = []
pattern_cam3 = []
diff = []
axis_x = []
sync_on = 0
sync_off = 0
fnos = []
filename = os.path.normpath(options.filename)
print filename
f = open(filename,'r')
filehandler = f.readlines()
i = 0
f.close()
f1 = 0
f2 = 0
for line in filehandler:
    line = line.rstrip('\n').split(' ')
    ts = float(line[0])
    fno= float(line[1])
    num_cam0 = float(line[2])
    num_cam1 = float(line[3])
    num_cam2 = float(line[4])
    num_cam3 = float(line[5])
    dif = num_cam0 - num_cam1
    pattern_cam0.append(num_cam0)
    pattern_cam1.append(num_cam1)
    pattern_cam2.append(num_cam2)
    pattern_cam3.append(num_cam3)
    diff.append(dif)
    fnos.append(fno)

    axis_x.append(i)
    i += 1
nnn = np.array(fnos)
print (nnn[1:]-nnn[:-1]).max()
print (nnn[1:]-nnn[:-1]).min()
#Prepare graph
#on  = 100.*(sync_on*1./len(axis_x))
#off = 100.*(sync_off*1./len(axis_x)) 
title = 'img v.s id: %s' % (basename)#, on, off)
#plot it
fig = plt.figure()
ax = plt.subplot(111)

ax.plot(axis_x, fnos, 'r-',label='fno')
#ax.plot(axis_x, pattern_cam0, 'r-x',label='cam0')
#ax.plot(axis_x, pattern_cam1, 'b-x', label='cam1')

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
plt.title(title)
plt.ylabel('id number')
plt.xlabel('image number')
ax.xaxis.grid(True)
grid()
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig(basename+'-id.png')
#print "%.2f%% synchronized" % on
#print "%.2f%% NOT synchronized" % off
print "%d total"% (len(axis_x))
plt.show()
################ line plot #######################
#plt.clf()
#ax2 = plt.subplot(111)
#ax2.plot(axis_x, diff, 'r-x',label='cam0 - cam1')
#box = ax2.get_position()
#ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
#plt.ylabel('pattern diff')
#plt.xlabel('image number')
#title = 'img v.s pat diff: %s\nsynchronized: YES: %d , NO: %d' % (basename, sync_on, sync_off)
#plt.title(title)
#ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#plt.savefig(basename+'.png')
#
#plt.show()

