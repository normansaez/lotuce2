#!/usr/bin/python
import datetime
from pylab import grid#imshow,show
import matplotlib.pyplot as plt
from matplotlib import ticker
import argparse 
import sys
import os
import numpy as np
import pandas as pd

if __name__=="__main__":
    usage = '''
    '''
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-f', '--filename', dest='filename', type=str, help='Path to get txt source', default=None)
    parser.add_argument('-s', '--sfilename', dest='sfilename', type=str, help='Path to get txt source', default=None)
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
    exp = []
    exp.append(filename.split('/')[-2])
    exp.append(sfilename.split('/')[-2])
    freq = 1./options.hertz
    m_cols = ['ts', 'id', 'cam0', 'cam1', 'cam2', 'cam3']
    filedata = pd.read_csv(options.filename, sep=' ', names=m_cols)
    sfiledata = pd.read_csv(options.sfilename, sep=' ', names=m_cols)
    runexec = basename.split('-')[3].replace('_','-').split('.')
    srunexec = sbasename.split('-')[3].replace('_','-').split('.')
    #
    #
    #
    ids1 = filedata['id']
    ids2 = sfiledata['id']
    axis_x = []
    ts1 = filedata['ts']
    d = datetime.datetime.fromtimestamp(ts1[0])
    axis_x.append(d)
    #
    #Fixing axis x
    #
    if len(ids1) > len(ids2):
        axis_len = len(ids2)
        drops = len(ids1) - len(ids2)
        ids1 = ids1[:axis_len]
        print "using ids2 , dropping : %d from ids1" % (drops)
    else:
        axis_len = len(ids1)
        drops = len(ids2) - len(ids1)
        ids2 = ids2[:axis_len]
        print "using ids1 , dropping : %d from ids2" % (drops)
    #
    #Fixing axis y
    #
    ids1_ = ids1[0]
    ids2_ = ids2[0]
    if ids1_ > ids2_:
        delta = ids1_ - ids2_
        ids1 = ids1 - delta
    else:
        delta = ids2_ - ids1_
        ids2 = ids2 - delta
    #
    #
    #
    axis_x = [d + datetime.timedelta(0, freq*x) for x in range(0, axis_len)]
    #
    # PLOT
    #
    fig = plt.figure()
    ax = plt.subplot(111)
    #print len(diff)
    ax.plot(axis_x, ids1,'b.', label='%s '%(exp[0])+r'$id(n)$', alpha= 0.5)
    ax.plot(axis_x, ids2,'r.', label='%s '%(exp[1])+r'$id(n)$', alpha= 0.5)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    plt.title(r'time v.s $id(n)$')
    plt.ylabel(r'$id(n)$')
    plt.xlabel(r'time')
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True) 
    formatter.set_powerlimits((-1,1)) 
    ax.yaxis.set_major_formatter(formatter) 
    ax.xaxis.grid(True)
    grid()
    ax.legend(loc='best', fancybox=True)#, bbox_to_anchor=(0.75, 0.92), fancybox=True)#, framealpha=0.8)
    plt.gcf().autofmt_xdate()
    plt.savefig(exp[0]+'-'+exp[1]+'-'+str(__file__).split('.')[0]+'.png',dpi=300) # format='eps'
#    plt.show()
    
