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
#from matplotlib import rcParams
import mmap

#rcParams.update({'font.size': 18, 'text.usetex': True})
#rcParams.update({'font.size': 18, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})

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
    map.close()
    del axis_x[-1]
    np_fnos = np.array(fnos)
    print (np_fnos[1:]-np_fnos[:-1]).max()
    print (np_fnos[1:]-np_fnos[:-1]).min()
    
    for j in range(0,i-1):
        fno_id = np_fnos[j+1] - np_fnos[j]
        fns.append(fno_id)
    print len(axis_x)
    print len(fns)
    #axis_x = date2num(axis_x)
    runexec = basename.split('-')[3].replace('_','-').split('.')
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.plot(axis_x, fns,'r.', label=r'$\Delta id(n)$')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    csfont = {'fontname':'Comic Sans MS'}
    hfont = {'fontname':'Helvetica'}
    plt.title(r'timestamp v.s $\Delta id(n)$'+'\n'+ r'$%s:%s:%s$' % (options.experiment, runexec[0], runexec[1]), **hfont)#**csfont)
    plt.ylabel(r'$\Delta id(n) = id(n+1) - id(n)$')
    plt.xlabel(r'timestamp',**hfont)
    #xticks(rotation='vertical')
    #formatter = ticker.ScalarFormatter(useMathText=True)
    #formatter.set_scientific(True) 
    #formatter.set_powerlimits((-1,1)) 
    #ax.xaxis.set_major_formatter(formatter) 
    plt.gcf().autofmt_xdate()
    ax.xaxis.grid(True)
    grid()
    ax.legend(loc='center left', bbox_to_anchor=(0.75, 0.92))
    plt.savefig(options.experiment+'-'+str(__file__).split('.')[0]+'.png')
    print "%d total"% (len(axis_x))
    plt.show()
