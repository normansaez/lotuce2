import FITS
import glob
import sys
from pylab import grid#imshow,show
import matplotlib.pyplot as plt
import argparse 
import numpy as np
from skimage.measure import regionprops
from skimage.measure import label
from math import floor

def bit_check(x, y, img, threshold):
    width = 3
    intensity = img[y-width:y+width,x-width:x+width].mean()
    if intensity >= threshold:
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
    print "Calibrating centroid pattern ..."
    usage = '''
    '''
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-r', '--reference', dest='reference', type=str, help='Path to get reference images', default=None)
    parser.add_argument('-d', '--dirname', dest='dirname', type=str, help='Path to get images', default=None)
    parser.add_argument('-t', '--threshold', dest='threshold', type=int, help='Threshold to filter image', default=4000)
    parser.add_argument('-i', '--init', dest='init', type=int, help='inital image to proces', default=0)
    parser.add_argument('-e', '--end', dest='end', type=int, help='final image to proces', default=29)
    (options, unknown) = parser.parse_known_args()
    # vars
    xi_cam0 = 200
    xf_cam0 = 400
    yi_cam0 = 0
    yf_cam0 = 200

    xi_cam1 = 0
    xf_cam1 = 200 
    yi_cam1 = 0
    yf_cam1 = 200 

    if options.reference is None:
        print "No reference directory is given, you need give a path with a directory with images as references"
        print "Use -r /path/directory/images/reference/"
        sys.exit(-1)

    if options.dirname is None:
        print "No directory with images to analisis is given, you need give a path with a directory with images"
        print "Use -d /path/directory/images/"
        sys.exit(-1)

    cam0_b0 = options.reference+'/img_000.fits'
    cam0_b1 = options.reference+'/img_001.fits'
    cam0_b2 = options.reference+'/img_002.fits'
    cam0_b3 = options.reference+'/img_003.fits'

    cam1_b0 = options.reference+'/img_001.fits'
    cam1_b1 = options.reference+'/img_002.fits'
    cam1_b2 = options.reference+'/img_004.fits'
    cam1_b3 = options.reference+'/img_008.fits'

    b0_0 = FITS.Read(cam0_b0)[1][xi_cam0:xf_cam0,yi_cam0:yf_cam0]
    b1_0 = FITS.Read(cam0_b1)[1][xi_cam0:xf_cam0,yi_cam0:yf_cam0]
    b2_0 = FITS.Read(cam0_b2)[1][xi_cam0:xf_cam0,yi_cam0:yf_cam0]
    b3_0 = FITS.Read(cam0_b3)[1][xi_cam0:xf_cam0,yi_cam0:yf_cam0]

    b0_1 = FITS.Read(cam1_b0)[1][xi_cam1:xf_cam1,yi_cam1:yf_cam1]
    b1_1 = FITS.Read(cam1_b1)[1][xi_cam1:xf_cam1,yi_cam1:yf_cam1]
    b2_1 = FITS.Read(cam1_b2)[1][xi_cam1:xf_cam1,yi_cam1:yf_cam1]
    b3_1 = FITS.Read(cam1_b3)[1][xi_cam1:xf_cam1,yi_cam1:yf_cam1]

    mask_b0_0 = np.where(b0_0 > options.threshold,1,0)
    mask_b1_0 = np.where(b1_0 > options.threshold,1,0)
    mask_b2_0 = np.where(b2_0 > options.threshold,1,0)
    mask_b3_0 = np.where(b3_0 > options.threshold,1,0)

    mask_b0_1 = np.where(b0_1 > options.threshold,1,0)
    mask_b1_1 = np.where(b1_1 > options.threshold,1,0)
    mask_b2_1 = np.where(b2_1 > options.threshold,1,0)
    mask_b3_1 = np.where(b3_1 > options.threshold,1,0)

    padding = 5
    border = np.ones(b0_0.shape)
    border[:padding,:] = 0
    border[:,:padding] = 0
    border[xf_cam0 - xi_cam0 - padding:,:] = 0
    border[:, xf_cam0 - xi_cam0 - padding:] = 0

    mask_b0_cam0 = mask_b0_0 * b0_0 * border
    mask_b1_cam0 = mask_b1_0 * b1_0 * border
    mask_b2_cam0 = mask_b2_0 * b2_0 * border
    mask_b3_cam0 = mask_b3_0 * b3_0 * border

    mask_b0_cam1 = mask_b0_1 * b0_1 * border
    mask_b1_cam1 = mask_b1_1 * b1_1 * border
    mask_b2_cam1 = mask_b2_1 * b2_1 * border
    mask_b3_cam1 = mask_b3_1 * b3_1 * border

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
good = 0
bad = 0
for i in range(options.init, options.end+1):
    img = options.reference + '/img_'+str(i).zfill(3)+'.fits'
    print img
    try:
        f = FITS.Read(glob.glob(img)[0])[1]
        cam_cam0 = f[xi_cam0:xf_cam0,yi_cam0:yf_cam0]
        b0_cam0 = bit_check(x0_cam0, y0_cam0, cam_cam0, options.threshold)
        b1_cam0 = bit_check(x1_cam0, y1_cam0, cam_cam0, options.threshold)
        b2_cam0 = bit_check(x2_cam0, y2_cam0, cam_cam0, options.threshold)
        b3_cam0 = bit_check(x3_cam0, y3_cam0, cam_cam0, options.threshold)
        num_cam0 = '0b'+str(b3_cam0)+str(b2_cam0)+str(b1_cam0)+str(b0_cam0)
        print num_cam0
        num_cam0 = eval(num_cam0)
        print num_cam0
        cam_cam1 = f[xi_cam1:xf_cam1,yi_cam1:yf_cam1]
        b0_cam1 = bit_check(x0_cam1, y0_cam1, cam_cam1, options.threshold)
        b1_cam1 = bit_check(x1_cam1, y1_cam1, cam_cam1, options.threshold)
        b2_cam1 = bit_check(x2_cam1, y2_cam1, cam_cam1, options.threshold)
        b3_cam1 = bit_check(x3_cam1, y3_cam1, cam_cam1, options.threshold)
        num_cam1 = '0b'+str(b3_cam1)+str(b2_cam1)+str(b1_cam1)+str(b0_cam1)
        print num_cam1
        num_cam1 = eval(num_cam1)
        print num_cam1
        if num_cam1 == num_cam0:
            good += 1
        else:
            bad += 1
        pattern_cam0.append(num_cam0)
        pattern_cam1.append(num_cam1)

        axis_x.append(i)
    except IndexError, e:
        print e
fig = plt.figure()
ax = plt.subplot(111)

ax.plot(axis_x, pattern_cam0, 'r-x',label='camera_cam0')
ax.plot(axis_x, pattern_cam1, 'b-x', label='camera_cam1')

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
title = '#images v/s #patterns. %.1f%% bad, %.1f%% good' % (100.*(bad*1./len(axis_x)) , 100.*(good*1./len(axis_x)))
plt.title(title)
plt.ylabel('pattern number')
plt.xlabel('image number')
ax.xaxis.grid(True)
grid()
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#plt.savefig(dirname+'.png')
print "%.2f%% good" % ( 100.*(good*1./len(axis_x)))
print "%.2f%% bad" % ( 100.*(bad*1./len(axis_x)))
print "%d total"% (len(axis_x))
plt.show()

