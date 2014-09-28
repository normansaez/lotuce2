import FITS
import glob
import sys
import os
from pylab import grid#imshow,show
import matplotlib.pyplot as plt
import argparse 
import numpy as np
from skimage.measure import regionprops
from skimage.measure import label
from math import floor

#COLOR CONST
BLUE     = '\033[34m'
RED      = '\033[31m'
GREEN    = '\033[32m'
YELLOW   = '\033[33m'
BLACK    = '\033[30m'
CRIM     = '\033[36m'
NO_COLOR = '\033[0m'

def bit_check(x, y, img, threshold, width):
    intensity = img[y-width:y+width,x-width:x+width].mean()
    print "(%.0f >= %.0f)" % (intensity, threshold),
    if intensity >= threshold:
        print " ON" 
        return 1
    print 
    return 0

def get_centroid(img):
    label_img = label(img)
    regions = regionprops(label_img)
    
    for props in regions:
        y0, x0 = props.centroid
        return floor(y0), floor(x0)
    return -1, -1

if __name__=="__main__":
    print "Calibrating centroid pattern ..."
    usage = '''
    '''
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-r', '--reference', dest='reference', type=str, help='Path to get reference images', default=None)
    parser.add_argument('-d', '--dirname', dest='dirname', type=str, help='Path to get images', default=None)
    parser.add_argument('-t', '--threshold', dest='threshold', type=int, help='Threshold to filter image', default=4000)
    parser.add_argument('-i', '--init', dest='init', type=int, help='inital image to proces', default=0)
    parser.add_argument('-e', '--end', dest='end', type=int, help='final image to proces', default=29)
    parser.add_argument('-s', '--show', dest='show', action='store_true' , help='Enable show or not to show plots. default not shows')

    (options, unknown) = parser.parse_known_args()
    # camera coordinates according windows size
    xi_cam0 = 200
    xf_cam0 = 400
    yi_cam0 = 0
    yf_cam0 = 200

    xi_cam1 = 0
    xf_cam1 = 200 
    yi_cam1 = 0
    yf_cam1 = 200 
    
    #Padding in pixels to make closed shapes and get a correct centroid
    padding = 7
    #area to search intensity (mean) taking account centroid
    width = 5


    if options.reference is None:
        print "No reference directory is given, you need give a path with a directory with images as references"
        print "Use -r /path/directory/images/reference/"
        sys.exit(-1)

    if options.dirname is None:
        print "No directory with images to analisis is given, you need give a path with a directory with images"
        print "Use -d /path/directory/images/"
        sys.exit(-1)

    options.dirname = os.path.normpath(options.dirname)

    #XXX: image reference: this is according each windows size
    cam0_b0 = options.reference+'/img_000.fits'
    cam0_b1 = options.reference+'/img_001.fits'
    cam0_b2 = options.reference+'/img_003.fits'
    cam0_b3 = options.reference+'/img_007.fits'

    cam1_b0 = options.reference+'/img_001.fits'
    cam1_b1 = options.reference+'/img_002.fits'
    cam1_b2 = options.reference+'/img_004.fits'
    cam1_b3 = options.reference+'/img_008.fits'

    #Getting central coordinates
    b0_0 = FITS.Read(cam0_b0)[1][xi_cam0:xf_cam0,yi_cam0:yf_cam0]
    b1_0 = FITS.Read(cam0_b1)[1][xi_cam0:xf_cam0,yi_cam0:yf_cam0]
    b2_0 = FITS.Read(cam0_b2)[1][xi_cam0:xf_cam0,yi_cam0:yf_cam0]
    b3_0 = FITS.Read(cam0_b3)[1][xi_cam0:xf_cam0,yi_cam0:yf_cam0]

    b0_1 = FITS.Read(cam1_b0)[1][xi_cam1:xf_cam1,yi_cam1:yf_cam1]
    b1_1 = FITS.Read(cam1_b1)[1][xi_cam1:xf_cam1,yi_cam1:yf_cam1]
    b2_1 = FITS.Read(cam1_b2)[1][xi_cam1:xf_cam1,yi_cam1:yf_cam1]
    b3_1 = FITS.Read(cam1_b3)[1][xi_cam1:xf_cam1,yi_cam1:yf_cam1]

    #Fixed limit to not convert a binary image
    mask_b0_0 = np.where(b0_0 > 4000,1,0)
    mask_b1_0 = np.where(b1_0 > 4000,1,0)
    mask_b2_0 = np.where(b2_0 > 4000,1,0)
    mask_b3_0 = np.where(b3_0 > 4000,1,0)

    mask_b0_1 = np.where(b0_1 > 4000,1,0)
    mask_b1_1 = np.where(b1_1 > 4000,1,0)
    mask_b2_1 = np.where(b2_1 > 4000,1,0)
    mask_b3_1 = np.where(b3_1 > 4000,1,0)
    
    #Apply border (padding)
    border = np.ones(b0_0.shape)
    border[:padding,:] = 0
    border[:,:padding] = 0
    border[xf_cam0 - xi_cam0 - padding:,:] = 0
    border[:, xf_cam0 - xi_cam0 - padding:] = 0
    
    #(binary image )*(original image)*(border) = acurate centroid (in theory)  
    mask_b0_cam0 = mask_b0_0 * b0_0 * border
    mask_b1_cam0 = mask_b1_0 * b1_0 * border
    mask_b2_cam0 = mask_b2_0 * b2_0 * border
    mask_b3_cam0 = mask_b3_0 * b3_0 * border

    mask_b0_cam1 = mask_b0_1 * b0_1 * border
    mask_b1_cam1 = mask_b1_1 * b1_1 * border
    mask_b2_cam1 = mask_b2_1 * b2_1 * border
    mask_b3_cam1 = mask_b3_1 * b3_1 * border

    #Getting centroid
    y0_cam0, x0_cam0 = get_centroid(mask_b0_cam0)
    y1_cam0, x1_cam0 = get_centroid(mask_b1_cam0)
    y2_cam0, x2_cam0 = get_centroid(mask_b2_cam0)
    y3_cam0, x3_cam0 = get_centroid(mask_b3_cam0)

    y0_cam1, x0_cam1 = get_centroid(mask_b0_cam1)
    y1_cam1, x1_cam1 = get_centroid(mask_b1_cam1)
    y2_cam1, x2_cam1 = get_centroid(mask_b2_cam1)
    y3_cam1, x3_cam1 = get_centroid(mask_b3_cam1)

print "GO !!"
pattern_cam0 = []
pattern_cam1 = []
axis_x = []
sync_on = 0
sync_off = 0
check = False
for i in range(options.init, options.end+1):
    img = os.path.normpath(options.dirname + '/img_'+str(i).zfill(3)+'.fits')
    print img
    try:
        f = FITS.Read(img)[1]
        #check bits for cam0   
        print "-------------------------------------------------------------"
        print "cam0"
        cam_cam0 = f[xi_cam0:xf_cam0,yi_cam0:yf_cam0]
        b0_cam0 = bit_check(x0_cam0, y0_cam0, cam_cam0, options.threshold, width)
        b1_cam0 = bit_check(x1_cam0, y1_cam0, cam_cam0, options.threshold, width)
        b2_cam0 = bit_check(x2_cam0, y2_cam0, cam_cam0, options.threshold, width)
        b3_cam0 = bit_check(x3_cam0, y3_cam0, cam_cam0, options.threshold, width)
        num_cam0 = '0b'+str(b3_cam0)+str(b2_cam0)+str(b1_cam0)+str(b0_cam0)
        print num_cam0
        num_cam0 = eval(num_cam0)
        print num_cam0
        #################################
        if check is True:
            fig = plt.figure()
            #234 =     "2x3 grid, 4th subplot".
            ax = plt.subplot(111)
            ax.set_xlim(0,xf_cam0-xi_cam0)
            ax.set_ylim(0,yf_cam0-yi_cam0)
            ax.autoscale(False)
            ax.imshow(cam_cam0)
            ax.plot(x0_cam0, y0_cam0, 'x',label='b0')
            plt.show()
            break
        #-------------------------------------------------------------------
        #check bits for cam0   
        cam_cam1 = f[xi_cam1:xf_cam1,yi_cam1:yf_cam1]
        print "-------------"
        print "cam1"
        b0_cam1 = bit_check(x0_cam1, y0_cam1, cam_cam1, options.threshold, width)
        b1_cam1 = bit_check(x1_cam1, y1_cam1, cam_cam1, options.threshold, width)
        b2_cam1 = bit_check(x2_cam1, y2_cam1, cam_cam1, options.threshold, width)
        b3_cam1 = bit_check(x3_cam1, y3_cam1, cam_cam1, options.threshold, width)
        num_cam1 = '0b'+str(b3_cam1)+str(b2_cam1)+str(b1_cam1)+str(b0_cam1)
        print num_cam1
        num_cam1 = eval(num_cam1)
        print num_cam1
        if num_cam1 == num_cam0:
            sync_on += 1
        else:
            sync_off += 1
            print "%sNOT SYNC: %s %s" % (RED,img,NO_COLOR)
        print "-------------------------------------------------------------"
        pattern_cam0.append(num_cam0)
        pattern_cam1.append(num_cam1)

        axis_x.append(i)
    except Exception, e:
        print e
#Prepare graph
basename = os.path.basename(options.dirname)
on  = 100.*(sync_on*1./len(axis_x))
off = 100.*(sync_off*1./len(axis_x)) 
title = 'img v.s pat: %s\nsynchronized: YES: %.1f%% , NO: %.1f%%' % (basename, on, off)
#plot it
fig = plt.figure()
ax = plt.subplot(111)

ax.plot(axis_x, pattern_cam0, 'r-x',label='cam0')
ax.plot(axis_x, pattern_cam1, 'b-x', label='cam1')

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
plt.title(title)
plt.ylabel('pattern number')
plt.xlabel('image number')
ax.xaxis.grid(True)
grid()
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig(basename+'.png')
print "%.2f%% synchronized" % on
print "%.2f%% NOT synchronized" % off
print "%d total"% (len(axis_x))

if options.show is True:
    plt.show()

