#!/usr/bin/python
import datetime
from pylab import grid#imshow,show
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import ticker
import argparse 
import sys
import os
import numpy as np

if __name__=="__main__":
    usage = '''
    '''
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-f', '--filename', dest='filename', type=str, help='Path to get txt source', default=None)
    parser.add_argument('-l', '--limit', dest='limit', type=int, help='Default limit to plot', default=None)#131100)#393300)#786600)#None)

    (options, unknown) = parser.parse_known_args()

    if options.filename is None:
        print "No filename to be to analised, you need give a path for the filename"
        print "Use -f /path/to/the/filename"
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
    print "%d total"% (len(axis_x))
    plt.show()
