import matplotlib.pyplot as plt
from pylab import *
from mpl_toolkits.mplot3d.axes3d import Axes3D
import argparse 
import os
import numpy as np
import sys

if __name__=="__main__":
    print "Calibrating centroid pattern ..."
    usage = '''
    '''
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-d', '--filename', dest='filename', type=str, help='Path to get images', default=None)

    (options, unknown) = parser.parse_known_args()

    if options.filename is None:
        print "No directory with images to analisis is given, you need give a path with a directory with images"
        print "Use -d /path/directory/images/"
        sys.exit(-1)

    options.filename = os.path.normpath(options.filename)
    basename = os.path.basename(options.filename)

    filename = os.path.normpath(options.filename)
    f = open(filename,'r')
    filehandler = f.readlines()
    i = 0
    f.close()
    fnos = []
    
    for line in filehandler:
        line = line.rstrip('\n').split(' ')
        ts = float(line[0])
        fno= float(line[1])
        num_cam0 = float(line[2])
        num_cam1 = float(line[3])
        num_cam2 = float(line[4])
        num_cam3 = float(line[5])
        fnos.append(fno)
        i += 1
        break
    #
    #
    #
    def fun(x, y):
        return test[x][y]

    x = range(0,4)
    y = range(0,16)
    X,Y = np.meshgrid(x, y)
    print X
    print Y
    test = [[a for a in range(0, len(y))] for b in range(0, len(x))]
    print test
    zs = np.array([fun(x,y) for x,y in zip(np.ravel(X), np.ravel(Y))])
    print zs
#    Z = fnos
    Z = zs.reshape(X.shape)
    print Z
    sys.exit(0)
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(1,1,1, projection='3d')
    ax.plot_surface(X, Y, Z, rstride=4, cstride=4, alpha=0.25)
#    cset = ax.contour(X, Y, Z, zdir='z', offset=-pi, cmap=cm.coolwarm)
#    cset = ax.contour(X, Y, Z, zdir='x', offset=-pi, cmap=cm.coolwarm)
#    cset = ax.contour(X, Y, Z, zdir='y', offset=3*pi, cmap=cm.coolwarm)
#    ax.set_xlim3d(-pi, 2*pi);
#    ax.set_ylim3d(0, 3*pi);
#    ax.set_zlim3d(-pi, 2*pi);
    plt.show()
