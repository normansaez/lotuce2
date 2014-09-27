import FITS
import glob
#from pylab import imshow,show
import matplotlib.pyplot as plt
import argparse 
import numpy as np
from skimage.measure import regionprops
from skimage.measure import label
from math import floor

def bit_check(x, y, img, limit):
    intensity = img[y,x]
    if intensity >= limit:
        return 1
    return 0

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
    parser.add_argument('-c', '--camera', dest='camera', type=int, help='Camera', default=0)
    parser.add_argument('-r', '--reference', dest='reference', type=str, help='Path to get reference images', default='ref_200Hz_200plx/')
    parser.add_argument('-d', '--dirname', dest='dirname', type=str, help='Path to get images', default='200Hz_200plx_run1')
    parser.add_argument('-t', '--threshold', dest='threshold', type=int, help='Threshold to filter image', default=3000)
    (options, unknown) = parser.parse_known_args()
    # vars
    if options.camera == 0:
        xi_cam = 201
        xf_cam = 400
        yi_cam = 0
        yf_cam = 200
    if options.camera == 1:
        xi_cam = 0
        xf_cam = 200
        yi_cam = 0
        yf_cam = 200
    
    #cam1
    print "Search pattern b1"
    images = glob.glob(options.reference+'/*.fits')
    for img in images:
        FITS.Read(img)[1][xi_cam:xf_cam,yi_cam:yf_cam] 
        print img    
#    y0_cam, x0_cam = get_centroid(mask_cam1_01)

#fig = plt.figure()
#ax = plt.subplot(111)

#ax.plot(x0_cam0, y0_cam0, 'r-x',label='b1')

#box = ax.get_position()
#ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
#title = 'reference centroid'
#plt.title(title)
#plt.ylabel('pattern number')
#plt.xlabel('image number')
#ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#plt.savefig(dirname+'.png')
#plt.show()

