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
    parser.add_argument('-e', '--experiment', dest='experiment', type=str, help='Experiment name', default='A')
    parser.add_argument('-l', '--limit', dest='limit', type=int, help='Default limit to plot', default=None)#131100)#393300)#786600)#None)
    parser.add_argument('--hertz', dest='hertz', type=int, help='Herzt to be plotted', default=220)

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
    counter = 0
    x = []
    y = []
    freq = 1./options.hertz
    for line in filehandler:
        line = line.rstrip('\n').split(' ')
        ts = float(line[0])
        fno= float(line[1])
        if counter == 0:
            d = datetime.datetime.fromtimestamp(ts)
        else:
            d = d + datetime.timedelta(0,freq)
        y.append(d)
        x.append(fno)
        counter += 1
        if counter == options.limit:
            break
    np_x = np.array(x)
    np_x = np_x/np_x.max()
    x = np_x.tolist()
    runexec = basename.split('-')[3].replace('_','-').split('.')
    fig = plt.figure()
    ax = plt.subplot(111)
    #print len(diff)
    ax.plot(y,x,'r-',label=r'$id(n)$')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    plt.title(r'time v.s $id(n)$ %s:%s' % (runexec[0], runexec[1]))
    plt.ylabel(r'$id(n)$')
    plt.xlabel(r'time')
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True) 
    formatter.set_powerlimits((-1,1)) 
    ax.yaxis.set_major_formatter(formatter) 
    ax.xaxis.grid(True)
    grid()
    plt.gcf().autofmt_xdate()
#    ax.legend(loc='center left', bbox_to_anchor=(0.75, 0.92))
    plt.savefig(options.experiment+'-'+str(__file__).split('.')[0]+'.png')
    plt.show()
    
