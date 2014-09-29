import FITS
import glob
#from pylab import imshow,show
import matplotlib.pyplot as plt
import argparse 
import numpy as np
from skimage.measure import regionprops
from skimage.measure import label
from math import floor
import sys

def get_centroid(img):
    label_img = label(img)
    regions = regionprops(label_img)
    
    for props in regions:
        y0, x0 = props.centroid
        return floor(y0), floor(x0)
    return -1, -1

if __name__=="__main__":
    usage = '''
    '''
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-c', '--camera', dest='camera', type=int, help='Camera', default=1)
    parser.add_argument('-r', '--reference', dest='reference', type=str, help='Path to get reference images', default=None)
    parser.add_argument('-d', '--dirname', dest='dirname', type=str, help='Path to get images', default=None)
    parser.add_argument('-t', '--threshold', dest='threshold', type=int, help='Threshold to filter image', default=4000)
    parser.add_argument('-l', '--lookpattern', dest='lookpattern', action='store_true' ,help='lookpattern')
    (options, unknown) = parser.parse_known_args()
    # vars
    if options.camera == 0:
        xi_cam = 492#200
        xf_cam = 984#400
        yi_cam = 0#0
        yf_cam = 656#200

    if options.camera == 1:
        xi_cam = 0#0
        xf_cam = 492#200 
        yi_cam = 0#0
        yf_cam = 656#200 

    if options.reference is None:
        print "No reference directory is given, you need give a path with a directory with images as references"
        print "Use -r /path/directory/images/reference/"
        sys.exit(-1)

    if options.dirname is None:
        print "No directory with images to analisis is given, you need give a path with a directory with images"
        print "Use -d /path/directory/images/"
        sys.exit(-1)
    #cam1
    if options.lookpattern is True:
        images = glob.glob(options.reference+'/*.fits')
        for img in images:
            f = FITS.Read(img)[1][xi_cam:xf_cam,yi_cam:yf_cam]
            fig = plt.figure()
            ax = plt.subplot(111)
            ax.set_xlim(0,xf_cam-xi_cam)
            ax.set_ylim(0,yf_cam-yi_cam)
            ax.autoscale(False)
            ax.imshow(f)
            print img
            plt.show()
    else:
        padding = 5

        b0 = options.reference+'/img_026.fits'
        f = FITS.Read(b0)[1][xi_cam:xf_cam,yi_cam:yf_cam]
        print f.shape
        fig = plt.figure()
        #234 =     "2x3 grid, 4th subplot".
        ax = plt.subplot(121)
        ax.set_xlim(0,xf_cam-xi_cam)
        ax.set_ylim(0,yf_cam-yi_cam)
        ax.autoscale(False)
        ax.imshow(f)
        #Doing mask
        mask_01 = np.where(f > options.threshold,1,0)
        border = np.ones(f.shape)
        border[:padding,:] = 0
        border[:,:padding] = 0
        border[xf_cam - xi_cam - padding:,:] = 0
        border[:, xf_cam - xi_cam - padding:] = 0
        mask = mask_01 * f * border
        #get centroid
        y0_cam, x0_cam = get_centroid(mask)
        print x0_cam
        print y0_cam
        ax.plot(x0_cam, y0_cam, 'x',label='b0')
        ax2 = plt.subplot(122)
        ax2.set_xlim(0,xf_cam-xi_cam)
        ax2.set_ylim(0,yf_cam-yi_cam)
        ax2.autoscale(False)
        ax2.imshow(mask)
        plt.show()
#box = ax.get_position()
#ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
#title = 'reference centroid'
#plt.title(title)
#plt.ylabel('pattern number')
#plt.xlabel('image number')
#ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#plt.savefig(dirname+'.png')
#plt.show()

