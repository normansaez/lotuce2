import matplotlib.pyplot as plt
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
    num_cam0s = []
    num_cam1s = []
    num_cam2s = []
    num_cam3s = []
    for line in filehandler:
        line = line.rstrip('\n').split(' ')
        ts = float(line[0])
        fno= float(line[1])
        num_cam0 = float(line[2])
        num_cam1 = float(line[3])
        num_cam2 = float(line[4])
        num_cam3 = float(line[5])
        fnos.append(fno)
        num_cam0s.append(num_cam0)
        num_cam1s.append(num_cam1)
        num_cam2s.append(num_cam2)
        num_cam3s.append(num_cam3)
        i += 1
        if i == 20:
            break
    #
    #
    #


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for c, z in zip(['r', 'g', 'b', 'y'], [30, 20, 10, 0]):
        if z == 0:
            xs = range(0,i)
            ys = num_cam0s
        if z == 10:
            xs = range(0,i)
            ys = num_cam1s
    

        if z == 20:
            xs = range(0,i)
            ys = num_cam2s
    

        if z == 30:
            xs = range(0,i)
            ys = num_cam3s
    
        print len(xs)
        print len(ys)
        cs = [c] * len(xs)
#        cs[0] = 'c'
        ax.bar(xs, ys, zs=z, zdir='y', color=cs, alpha=0.8)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    plt.show()
