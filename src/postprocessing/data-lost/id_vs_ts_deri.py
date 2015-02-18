#!/usr/bin/python
import datetime
from pylab import grid#imshow,show
import matplotlib.pyplot as plt
from matplotlib import ticker
import matplotlib.cm as cm
import argparse 
import os
import pandas as pd
import numpy as np
from subprocess import Popen, PIPE
from threading import Thread
from Queue import Queue

def wrapper(func, args, res):
        res.append(func(*args))
 
def mode(a, axis=0):
    scores = np.unique(np.ravel(a))       # get ALL unique values
    testshape = list(a.shape)
    testshape[axis] = 1
    oldmostfreq = np.zeros(testshape)
    oldcounts = np.zeros(testshape)

    for score in scores:
        template = (a == score)
        counts = np.expand_dims(np.sum(template, axis),axis)
        mostfrequent = np.where(counts > oldcounts, score, oldmostfreq)
        oldcounts = np.maximum(counts, oldcounts)
        oldmostfreq = mostfrequent

    return mostfrequent, oldcounts

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

    exp = []
    m_cols = ['ts', 'id', 'cam0', 'cam1', 'cam2', 'cam3']


    options.filename = os.path.normpath(options.filename)
    basename = os.path.basename(options.filename)
    filename = os.path.normpath(options.filename)
    print filename
    color = 'g.'
    exp.append(filename.split('/')[-2])
    experiment = exp[0]
    filedata = pd.read_csv(options.filename, sep=' ', names=m_cols)
    runexec = basename.split('-')[3].replace('_','-').split('.')

    tss = filedata['ts'] # delta Y

    np_tss = np.array(tss)
    np_delta_ts = np_tss[1:]-np_tss[:-1]
    print np_delta_ts
    #np_delta_ts = np_delta_ts[:len(np_delta_ts)-1] 
    print "min  %f" % np_delta_ts.min()
    print "max  %f" % np_delta_ts.max()
    print "mean %f" % np_delta_ts.mean()
    print "std  %f" % np_delta_ts.std()
    print "median: %f" % np.median(np_delta_ts)
    res = []
    thread1 = Thread(target=wrapper,args=(mode, (np_delta_ts,), res))
    thread1.start()
    print "1/min  %f" % (1./np_delta_ts.min())
    print "1/max  %f" % (1./np_delta_ts.max())
    print "1/mean %f" % (1./np_delta_ts.mean())
    print "1/std  %f" % (1./np_delta_ts.std())
    print "1/median: %f" % (1./np.median(np_delta_ts))
    runexec = basename.split('-')[3].replace('_','-').split('.')
    fig = plt.figure()
    ax = plt.subplot(111)
    print len(np_delta_ts)
    freq = 1/220.
    d = datetime.datetime.fromtimestamp(tss[0])
    axis_x = []
    axis_x.append(d)
    axis_x = [d + datetime.timedelta(0, freq*x) for x in range(0, len(np_delta_ts))]
    print len(axis_x)

    ax.plot(axis_x, np_delta_ts,'r-',label=r'$\Delta timestamp(n)$')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 1, box.height])
    plt.title(r'id(n) vs $\Delta timestamp(n)$ %s:%s' % (runexec[0], runexec[1]))
    plt.ylabel(r'$\Delta timestamp(n) = timestamp(n+1) - timestamp(n)$')
    plt.xlabel(r'id')
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True) 
    formatter.set_powerlimits((-1,1)) 
    ax.xaxis.set_major_formatter(formatter) 
#    ax.yaxis.set_major_formatter(formatter) 
    ax.xaxis.grid(True)
    grid()
    ax.legend(loc='center left', bbox_to_anchor=(0.75, 0.92))
    plt.savefig(exp[0]+'-'+str(__file__).split('.')[0]+'.png')
    thread1.join()
    mostfrequent = res[0][0]
    print "--------------------------------------"
    print "mode: %f" % mostfrequent[0]
    print "1/mode: %f" % (1./mostfrequent[0])
    plt.show()
