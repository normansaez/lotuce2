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
    parser.add_argument('-s', '--sfilename', dest='sfilename', type=str, help='Path to get txt second source', default=None)
    parser.add_argument('-e', '--experiment', dest='experiment', type=str, help='Experiment name', default='A')
    parser.add_argument('-l', '--limit', dest='limit', type=int, help='Default limit to plot', default=None)#131100)#393300)#786600)#None)

    (options, unknown) = parser.parse_known_args()

    if options.filename is None:
        print "No filename to be to analised, you need give a path for the filename"
        print "Use -f /path/to/the/filename"
        sys.exit(-1)

    options.filename = os.path.normpath(options.filename)
    basename = os.path.basename(options.filename)
    if options.sfilename is not None:
        options.sfilename = os.path.normpath(options.sfilename)
        sbasename = os.path.basename(options.sfilename)
        
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
    
    for j in range(0,i-1):
        fno_id = np_fnos[j+1] - np_fnos[j]
        fns.append(fno_id)
    if options.sfilename is not None:
        sfnos = []
        sfns = []
        i = 0
        print options.sfilename
        with open(options.sfilename, "r+b") as f:
            map = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
            for line in iter(map.readline, ""):
                line = line.rstrip('\n').split(' ')
                ts = float(line[0])
                fno= float(line[1])
                sfnos.append(fno)
                d = datetime.datetime.fromtimestamp(ts)
                axis_x.append(d)
                i += 1
                if i == options.limit:
                    break
        del axis_x[-1]
        np_sfnos = np.array(sfnos)
        print (np_sfnos[1:]-np_sfnos[:-1]).max()
        print (np_sfnos[1:]-np_sfnos[:-1]).min()
        
        for j in range(0,i-1):
            sfno_id = np_sfnos[j+1] - np_sfnos[j]
            sfns.append(sfno_id)
    cmax = 0
    if (np_sfnos[1:]-np_sfnos[:-1]).max() > (np_fnos[1:]-np_fnos[:-1]).max():
        cmax = (np_sfnos[1:]-np_sfnos[:-1]).max()
    else:
        cmax = (np_fnos[1:]-np_fnos[:-1]).max()
    bins = np.linspace(0,int(cmax+1),20)#20#range(0,3000,10)#[0,10,100,200,500,100,3000]#range(0,200,10)
    print bins
    hist(fns,bins,normed=True,log=True, color='b', label='C', alpha=0.5)
    if options.sfilename is not None:
        hist(sfns, bins, histtype='stepfilled', normed=True, log=True ,color='r', alpha=0.5, label='F')
    runexec = basename.split('-')[3].replace('_','-').split('.')
    plt.title("Histograma: %s:%s:%s"%(options.experiment,runexec[0], runexec[1]))
    plt.xlabel("valor")
    plt.ylabel("log(cuentas)")
    plt.legend(loc='upper right')
    plt.savefig(options.experiment+'-'+str(__file__).split('.')[0]+'.png')
    show()
