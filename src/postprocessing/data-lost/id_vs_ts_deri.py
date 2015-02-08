#!/usr/bin/python
import datetime
from pylab import grid#imshow,show
import matplotlib.pyplot as plt
from matplotlib import ticker
import matplotlib.cm as cm
import argparse 
import os
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
    parser.add_argument('-e', '--experiment', dest='experiment', type=str, help='Experiment name', default='A')
    parser.add_argument('-l', '--limit', dest='limit', type=int, help='Default limit to plot', default=None)#131100)#393300)#786600)#None)

    (options, unknown) = parser.parse_known_args()

    if options.filename is None:
        print "No filename to be to analised, you need give a path for the filename"
        print "Use -f /path/to/the/filename"
        sys.exit(-1)

    options.filename = os.path.normpath(options.filename)
    basename = os.path.basename(options.filename)
    filename = options.filename
    print filename
    f = open(filename,'r')
    filehandler = f.readlines()
    f.close()
    d0 = None#datetime.datetime.fromtimestamp(1421959082.652726)
    y = []
    fnos = []
    delta_ts = []
    counter = 0
    for line in filehandler:
        line = line.rstrip('\n').split(' ')
        ts = float(line[0])
        fno= float(line[1])
        d = datetime.datetime.fromtimestamp(ts)
        y.append(d)
        fnos.append(fno)
        if counter == options.limit:
            break
        counter += 1
    np_y = np.array(y)
    for j in range(0,counter-1):
        d_ts = (np_y[j+1] - np_y[j]).total_seconds()
#        print d_ts
        delta_ts.append(d_ts)
    del fnos[-1]
    print len(fnos)
    print len(delta_ts)
    np_delta_ts = np.array(delta_ts)
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
    ax.plot(fnos, delta_ts,'r-',label=r'$\Delta timestamp(n)')
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
    plt.savefig(options.experiment+'-'+str(__file__).split('.')[0]+'.png')
    thread1.join()
    mostfrequent = res[0][0]
    print "--------------------------------------"
    print "mode: %f" % mostfrequent[0]
    print "1/mode: %f" % (1./mostfrequent[0])
    plt.show()
