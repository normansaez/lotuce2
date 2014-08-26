import FITS
import glob
import time
from pylab import imshow,show
import matplotlib.pyplot as plt
import argparse 
import sys

if __name__=="__main__":
    usage = '''
    '''
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-p', '--path', dest='path', type=str, help='Path to get images', default=None)
    (options, unknown) = parser.parse_known_args()
    if options.path is None:
        print "give a image source path"
        sys.exit(-1)
    images = glob.glob(options.path+'/img_*')
    imgages = sorted(images)
    plt.ion()
    plt.figure()
    for i in images:
        print i
        f = FITS.Read(i)[1]
        plt.imshow(f)
        plt.draw()
        time.sleep(1)
    
