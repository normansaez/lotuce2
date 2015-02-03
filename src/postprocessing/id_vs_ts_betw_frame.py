#!/usr/bin/python
import datetime
from pylab import grid#imshow,show
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import argparse 
import os

if __name__=="__main__":
    print "Calibrating centroid pattern ..."
    usage = '''
    '''
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-d', '--filename', dest='filename', type=str, help='Path to get images', default=None)
    parser.add_argument('-l', '--limit', dest='limit', type=int, help='Default limit to plot', default=None)#131100)#393300)#786600)#None)

    (options, unknown) = parser.parse_known_args()

    if options.filename is None:
        print "No directory with images to analisis is given, you need give a path with a directory with images"
        print "Use -d /path/directory/images/"
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
    counter = -5
    for line in filehandler:
        line = line.rstrip('\n').split(' ')
        ts = float(line[0])
        fno= float(line[1])
        d = datetime.datetime.fromtimestamp(ts)
        print d,
        print " ---> %d" % fno
        if d0 == None:
            d0 = d - datetime.timedelta(0,0.0045)
        sec_diff = (d - d0).total_seconds()
        print sec_diff
        diff.append(sec_diff)
        fnos.append(fno)
        d0 = d
        if counter == 0:
            break
        counter -= 1
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.plot(fnos, diff,'r-',label='')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.xaxis.grid(True)
    grid()
    plt.show()
    
