#!/usr/bin/python
import datetime
from pylab import grid#imshow,show
import matplotlib.pyplot as plt
from matplotlib import ticker
import matplotlib.cm as cm
import argparse 
import os

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
    filename = options.filename
    print filename
    f = open(filename,'r')
    filehandler = f.readlines()
    f.close()
    d0 = None#datetime.datetime.fromtimestamp(1421959082.652726)
    diff = []
    fnos = []
    counter = 0
    for line in filehandler:
        line = line.rstrip('\n').split(' ')
        ts = float(line[0])
        fno= float(line[1])
        d = datetime.datetime.fromtimestamp(ts)
#        print d,
#        print " ---> %d" % fno
        if d0 == None:
            d0 = d - datetime.timedelta(0,0.008)
        sec_diff = (d - d0).total_seconds()
#        print sec_diff
        diff.append(sec_diff)
        fnos.append(fno)
        d0 = d
        if counter == options.limit:
            break
        counter += 1
    runexec = basename.split('-')[3].replace('_','-').split('.')
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.plot(fnos, diff,'r-',label=r'$\Delta timestamp(n)')
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
#    ax.legend(loc='center left', bbox_to_anchor=(0.75, 0.92))
    plt.savefig(str(__file__).split('.')[0]+'.png')
    plt.show()
    
