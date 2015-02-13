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
import pandas as pd


if __name__=="__main__":
    usage = '''
    '''
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-f', '--filename', dest='filename', type=str, help='Path to get txt source', default=None)
    parser.add_argument('-s', '--sfilename', dest='sfilename', type=str, help='Path to get txt source', default=None)
    parser.add_argument('-e', '--experiment', dest='experiment', type=str, help='Experiment name', default='A')
    parser.add_argument('-l', '--limit', dest='limit', type=int, help='Default limit to plot', default=None)#131100)#393300)#786600)#None)
    parser.add_argument('--hertz', dest='hertz', type=int, help='Herzt to be plotted', default=220)

    (options, unknown) = parser.parse_known_args()

    if options.filename is None:
        print "No filename to be to analised, you need give a path for the filename"
        print "Use -f /path/to/the/filename"
        sys.exit(-1)

    if options.sfilename is None:
        print "No sfilename to be to analised, you need give a path for the sfilename"
        print "Use -f /path/to/the/sfilename"
        sys.exit(-1)

    options.filename = os.path.normpath(options.filename)
    basename = os.path.basename(options.filename)
    options.sfilename = os.path.normpath(options.sfilename)
    sbasename = os.path.basename(options.sfilename)
    filename = os.path.normpath(options.filename)
    sfilename = os.path.normpath(options.sfilename)
    print filename
    print sfilename
    #
    # Hz
    #
    freq = 1./options.hertz
    #
    #
    #
    m_cols = ['ts', 'id', 'cam0', 'cam1', 'cam2', 'cam3']
    filedata = pd.read_csv(options.filename, sep=' ', names=m_cols)
    sfiledata = pd.read_csv(options.sfilename, sep=' ', names=m_cols)
    #
    #
    #
    runexec = basename.split('-')[3].replace('_','-').split('.')
    srunexec = sbasename.split('-')[3].replace('_','-').split('.')
    #
    #
    #
    ids1 = filedata['id']
    ids2 = sfiledata['id']
    #
    #Calculating deriv
    #
    np_ids1 = np.array(ids1)
    np_ids2 = np.array(ids2)
    delta_ids1 = np_ids1[1:]-np_ids1[:-1]
    delta_ids2 = np_ids2[1:]-np_ids2[:-1]
    print "dataset ---- %s:%s ----" % (runexec[0], runexec[1])
    print delta_ids1.max()
    print delta_ids1.min()
    print len(delta_ids1)
    print "dataset ---- %s:%s ----" % (srunexec[0], srunexec[1])
    print delta_ids2.max()
    print delta_ids2.min()
    print len(delta_ids2)
    print "-----------------------"
    #
    #
    #
    axis_x = []
    ts1 = filedata['ts']
    d = datetime.datetime.fromtimestamp(ts1[0])
    axis_x.append(d)
    if len(delta_ids1) > len(delta_ids2):
        axis_len = len(delta_ids2)
        drops = len(delta_ids1) - len(delta_ids2)
        delta_ids1 = delta_ids1[:axis_len]
        print "using ids2 , dropping : %d from ids1" % (drops)
    else:
        axis_len = len(delta_ids1)
        drops = len(delta_ids2) - len(delta_ids1)
        delta_ids2 = delta_ids2[:axis_len]
        print "using ids1 , dropping : %d from ids2" % (drops)

    for i in range(0,axis_len):
        d = d + datetime.timedelta(0,freq)
        axis_x.append(d)
    axis_x = date2num(axis_x)
    print "delta_ids1 len: %d" % len(delta_ids1)
    print "delta_ids2 len: %d" % len(delta_ids2)
    print "axis_len      : %d" % axis_len
    delta_ids1 = delta_ids1.tolist()
    delta_ids2 = delta_ids2.tolist()
    #
    #
    #
    print 
    #
    #
    #

    fig = plt.figure()
    ax = plt.subplot(111)
    ax.plot(axis_x, delta_ids1,'r.', label=r'$\Delta id(n)$')
    ax.plot(axis_x, delta_ids2,'b.', label=r'$\Delta id(n)$')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    csfont = {'fontname':'Comic Sans MS'}
    hfont = {'fontname':'Helvetica'}
    plt.title(r'time v.s $\Delta id(n)$'+'\n'+ r'$%s:%s:%s$' % (options.experiment, runexec[0], runexec[1]), **hfont)#**csfont)
    plt.ylabel(r'$\Delta id(n) = id(n+1) - id(n)$')
    plt.xlabel(r'time',**hfont)
    plt.gcf().autofmt_xdate()
    ax.xaxis.grid(True)
    grid()
    ax.legend(loc='center left', bbox_to_anchor=(0.75, 0.92))
    plt.savefig(options.experiment+'-'+str(__file__).split('.')[0]+'.png',dpi=300) # format='eps'
    print "%d total"% (len(axis_x))
    plt.show()
