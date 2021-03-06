import FITS
import glob
import sys
import os
from pylab import grid#imshow,show
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import argparse 
import numpy as np
from skimage.measure import regionprops
from skimage.measure import label
from math import floor
import matplotlib.patches as patches
from matplotlib.path import Path

#COLOR CONST
BLUE     = '\033[34m'
RED      = '\033[31m'
GREEN    = '\033[32m'
YELLOW   = '\033[33m'
BLACK    = '\033[30m'
CRIM     = '\033[36m'
NO_COLOR = '\033[0m'

def get_square(cx, cy, side, color='red'):
    verts = [
        (cx-side, cy-side), # left, bottom
        (cx-side, cy+side), # left, top
        (cx+side, cy+side), # right, top
        (cx+side, cy-side), # right, bottom
        (cx, cy), # ignored
        ]
    
    codes = [Path.MOVETO,
             Path.LINETO,
             Path.LINETO,
             Path.LINETO,
             Path.CLOSEPOLY,
             ]
    
    path = Path(verts, codes)
    
    patch = patches.PathPatch(path, facecolor='none', EdgeColor=color, lw=1)
    return patch


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
    parser.add_argument('-t', '--threshold', dest='threshold', type=int, help='Threshold to filter image', default=2000)
    parser.add_argument('-i', '--init', dest='init', type=int, help='inital image to proces', default=0)
    parser.add_argument('-e', '--end', dest='end', type=int, help='final image to proces', default=29)
    parser.add_argument('-s', '--show', dest='show', action='store_true' , help='Enable show plots')
    parser.add_argument('-n', '--nosave', dest='nosave', action='store_true' , help='Disable save plots')
    parser.add_argument('-c', '--check', dest='check', action='store_true' , help='Enable check bit area/th')

    (options, unknown) = parser.parse_known_args()

    if options.reference is None:
        print "No reference directory is given, you need give a path with a directory with images as references"
        print "Use -r /path/directory/images/reference/"
        sys.exit(-1)

    if options.dirname is None:
        print "No directory with images to analisis is given, you need give a path with a directory with images"
        print "Use -d /path/directory/images/"
        sys.exit(-1)

    options.dirname = os.path.normpath(options.dirname)
    basename = os.path.basename(options.dirname)

    # camera coordinates according windows size
    #XXX commented for 200x200 
    xi_cam0 = 200#492#200
    xf_cam0 = 400#984#400
    yi_cam0 = 0#0
    yf_cam0 = 200#656#200

    xi_cam1 = 0#0
    xf_cam1 = 200#492#200 
    yi_cam1 = 0#0
    yf_cam1 = 200#656#200 
    
    xi_cam2 = 400#0
    yi_cam2 = 0#0
    xf_cam2 = 600#492#200 
    yf_cam2 = 200#656#200 

    xi_cam3 = 600#0
    yi_cam3 = 0#0
    xf_cam3 = 800#492#200 
    yf_cam3 = 200#656#200 
    #Padding in pixels to make closed shapes and get a correct centroid
    padding = 5#7
    #area to search intensity (mean) taking account centroid
    width = 3#5

    #XXX: image reference: this is according each windows size
    #XXX commented for 200x200
    cam0_b0 = options.reference+'/img_001.fits'
    cam0_b1 = options.reference+'/img_002.fits'
    cam0_b2 = options.reference+'/img_004.fits'
    cam0_b3 = options.reference+'/img_008.fits'

    cam1_b0 = options.reference+'/img_001.fits'
    cam1_b1 = options.reference+'/img_002.fits'
    cam1_b2 = options.reference+'/img_004.fits'
    cam1_b3 = options.reference+'/img_008.fits'

    cam2_b0 = options.reference+'/img_001.fits'
    cam2_b1 = options.reference+'/img_002.fits'
    cam2_b2 = options.reference+'/img_004.fits'
    cam2_b3 = options.reference+'/img_008.fits'

    cam3_b0 = options.reference+'/img_001.fits'
    cam3_b1 = options.reference+'/img_002.fits'
    cam3_b2 = options.reference+'/img_004.fits'
    cam3_b3 = options.reference+'/img_008.fits'

    #Getting central coordinates
    b0_0 = FITS.Read(cam0_b0)[1][xi_cam0:xf_cam0,yi_cam0:yf_cam0]
    b1_0 = FITS.Read(cam0_b1)[1][xi_cam0:xf_cam0,yi_cam0:yf_cam0]
    b2_0 = FITS.Read(cam0_b2)[1][xi_cam0:xf_cam0,yi_cam0:yf_cam0]
    b3_0 = FITS.Read(cam0_b3)[1][xi_cam0:xf_cam0,yi_cam0:yf_cam0]

    b0_1 = FITS.Read(cam1_b0)[1][xi_cam1:xf_cam1,yi_cam1:yf_cam1]
    b1_1 = FITS.Read(cam1_b1)[1][xi_cam1:xf_cam1,yi_cam1:yf_cam1]
    b2_1 = FITS.Read(cam1_b2)[1][xi_cam1:xf_cam1,yi_cam1:yf_cam1]
    b3_1 = FITS.Read(cam1_b3)[1][xi_cam1:xf_cam1,yi_cam1:yf_cam1]

    b0_2 = FITS.Read(cam2_b0)[1][xi_cam2:xf_cam2,yi_cam2:yf_cam2]
    b1_2 = FITS.Read(cam2_b1)[1][xi_cam2:xf_cam2,yi_cam2:yf_cam2]
    b2_2 = FITS.Read(cam2_b2)[1][xi_cam2:xf_cam2,yi_cam2:yf_cam2]
    b3_2 = FITS.Read(cam2_b3)[1][xi_cam2:xf_cam2,yi_cam2:yf_cam2]

    b0_3 = FITS.Read(cam3_b0)[1][xi_cam3:xf_cam3,yi_cam3:yf_cam3]
    b1_3 = FITS.Read(cam3_b1)[1][xi_cam3:xf_cam3,yi_cam3:yf_cam3]
    b2_3 = FITS.Read(cam3_b2)[1][xi_cam3:xf_cam3,yi_cam3:yf_cam3]
    b3_3 = FITS.Read(cam3_b3)[1][xi_cam3:xf_cam3,yi_cam3:yf_cam3]

    #Fixed limit to not convert a binary image
    mask_b0_0 = np.where(b0_0 > 4000,1,0)
    mask_b1_0 = np.where(b1_0 > 4000,1,0)
    mask_b2_0 = np.where(b2_0 > 4000,1,0)
    mask_b3_0 = np.where(b3_0 > 4000,1,0)

    mask_b0_1 = np.where(b0_1 > 4000,1,0)
    mask_b1_1 = np.where(b1_1 > 4000,1,0)
    mask_b2_1 = np.where(b2_1 > 4000,1,0)
    mask_b3_1 = np.where(b3_1 > 4000,1,0)
    
    mask_b0_2 = np.where(b0_2 > 4000,1,0)
    mask_b1_2 = np.where(b1_2 > 4000,1,0)
    mask_b2_2 = np.where(b2_2 > 4000,1,0)
    mask_b3_2 = np.where(b3_2 > 4000,1,0)
    
    mask_b0_3 = np.where(b0_3 > 4000,1,0)
    mask_b1_3 = np.where(b1_3 > 4000,1,0)
    mask_b2_3 = np.where(b2_3 > 4000,1,0)
    mask_b3_3 = np.where(b3_3 > 4000,1,0)
    
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

    mask_b0_cam2 = mask_b0_2 * b0_2 * border
    mask_b1_cam2 = mask_b1_2 * b1_2 * border
    mask_b2_cam2 = mask_b2_2 * b2_2 * border
    mask_b3_cam2 = mask_b3_2 * b3_2 * border

    mask_b0_cam3 = mask_b0_3 * b0_3 * border
    mask_b1_cam3 = mask_b1_3 * b1_3 * border
    mask_b2_cam3 = mask_b2_3 * b2_3 * border
    mask_b3_cam3 = mask_b3_3 * b3_3 * border

    #Getting centroid
    y0_cam0, x0_cam0 = get_centroid(mask_b0_cam0)
    y1_cam0, x1_cam0 = get_centroid(mask_b1_cam0)
    y2_cam0, x2_cam0 = get_centroid(mask_b2_cam0)
    y3_cam0, x3_cam0 = get_centroid(mask_b3_cam0)

    y0_cam1, x0_cam1 = get_centroid(mask_b0_cam1)
    y1_cam1, x1_cam1 = get_centroid(mask_b1_cam1)
    y2_cam1, x2_cam1 = get_centroid(mask_b2_cam1)
    y3_cam1, x3_cam1 = get_centroid(mask_b3_cam1)

    y0_cam2, x0_cam2 = get_centroid(mask_b0_cam2)
    y1_cam2, x1_cam2 = get_centroid(mask_b1_cam2)
    y2_cam2, x2_cam2 = get_centroid(mask_b2_cam2)
    y3_cam2, x3_cam2 = get_centroid(mask_b3_cam2)

    y0_cam3, x0_cam3 = get_centroid(mask_b0_cam3)
    y1_cam3, x1_cam3 = get_centroid(mask_b1_cam3)
    y2_cam3, x2_cam3 = get_centroid(mask_b2_cam3)
    y3_cam3, x3_cam3 = get_centroid(mask_b3_cam3)

print "GO !!"
pattern_cam0 = []
pattern_cam1 = []
diff = []
axis_x = []
sync_on = 0
sync_off = 0
if options.nosave is False:
    text_file = open(basename+'.txt','w')
    text_file.write('basename img_name cam0 cam1\n')
end = 0
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
        #check bits for cam1 
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
        #################################
        #check bits for cam2 
        cam_cam2 = f[xi_cam2:xf_cam2,yi_cam2:yf_cam2]
        print "-------------"
        print "cam2"
        b0_cam2 = bit_check(x0_cam2, y0_cam2, cam_cam2, options.threshold, width)
        b1_cam2 = bit_check(x1_cam2, y1_cam2, cam_cam2, options.threshold, width)
        b2_cam2 = bit_check(x2_cam2, y2_cam2, cam_cam2, options.threshold, width)
        b3_cam2 = bit_check(x3_cam2, y3_cam2, cam_cam2, options.threshold, width)
        num_cam2 = '0b'+str(b3_cam2)+str(b2_cam2)+str(b1_cam2)+str(b0_cam2)
        print num_cam2
        num_cam2 = eval(num_cam2)
        print num_cam2
        #################################
        #check bits for cam3 
        cam_cam3 = f[xi_cam3:xf_cam3,yi_cam3:yf_cam3]
        print "-------------"
        print "cam3"
        b0_cam3 = bit_check(x0_cam3, y0_cam3, cam_cam3, options.threshold, width)
        b1_cam3 = bit_check(x1_cam3, y1_cam3, cam_cam3, options.threshold, width)
        b2_cam3 = bit_check(x2_cam3, y2_cam3, cam_cam3, options.threshold, width)
        b3_cam3 = bit_check(x3_cam3, y3_cam3, cam_cam3, options.threshold, width)
        num_cam3 = '0b'+str(b3_cam3)+str(b2_cam3)+str(b1_cam3)+str(b0_cam3)
        print num_cam3
        num_cam3 = eval(num_cam3)
        print num_cam3
        #################################
        if options.check is True:
            cam_cam0 = f[xi_cam0:xf_cam0,yi_cam0:yf_cam0]
            cam_cam1 = f[xi_cam1:xf_cam1,yi_cam1:yf_cam1]
            cam_cam2 = f[xi_cam2:xf_cam2,yi_cam2:yf_cam2]
            cam_cam3 = f[xi_cam3:xf_cam3,yi_cam3:yf_cam3]
            fig = plt.figure()
            #234 =     "2x3 grid, 4th subplot".
            ax = plt.subplot(411)
            ax.set_xlim(0,xf_cam0-xi_cam0)
            ax.set_ylim(0,yf_cam0-yi_cam0)
            ax.autoscale(False)
            ax.imshow(cam_cam0, cmap =cm.Greys_r)
            ax.plot(x0_cam0, y0_cam0, 'x',label='b0')
            ax.plot(x1_cam0, y1_cam0, 'x',label='b1')
            ax.plot(x2_cam0, y2_cam0, 'x',label='b2')
            ax.plot(x3_cam0, y3_cam0, 'x',label='b3')
            patch = get_square(x0_cam0, y0_cam0, width)
            plt.gca().add_patch(patch)
            patch = get_square(x1_cam0, y1_cam0, width)
            plt.gca().add_patch(patch)
            patch = get_square(x2_cam0, y2_cam0, width)
            plt.gca().add_patch(patch)
            patch = get_square(x3_cam0, y3_cam0, width)
            plt.gca().add_patch(patch)
            title = 'cam0'
            plt.title(title)
            #-----
            ax = plt.subplot(412)
            ax.set_xlim(0,xf_cam1-xi_cam1)
            ax.set_ylim(0,yf_cam1-yi_cam1)
            ax.autoscale(False)
            ax.imshow(cam_cam1, cmap =cm.Greys_r)
            ax.plot(x0_cam1, y0_cam1, 'x',label='b0')
            ax.plot(x1_cam1, y1_cam1, 'x',label='b1')
            ax.plot(x2_cam1, y2_cam1, 'x',label='b2')
            ax.plot(x3_cam1, y3_cam1, 'x',label='b3')
            patch = get_square(x0_cam1, y0_cam1, width)
            plt.gca().add_patch(patch)
            patch = get_square(x1_cam1, y1_cam1, width)
            plt.gca().add_patch(patch)
            patch = get_square(x2_cam1, y2_cam1, width)
            plt.gca().add_patch(patch)
            patch = get_square(x3_cam1, y3_cam1, width)
            plt.gca().add_patch(patch)
            title = 'cam1'
            plt.title(title)
            #-----
            ax = plt.subplot(413)
            ax.set_xlim(0,xf_cam2-xi_cam2)
            ax.set_ylim(0,yf_cam2-yi_cam2)
            ax.autoscale(False)
            ax.imshow(cam_cam2, cmap =cm.Greys_r)
            ax.plot(x0_cam2, y0_cam2, 'x',label='b0')
            ax.plot(x1_cam2, y1_cam2, 'x',label='b1')
            ax.plot(x2_cam2, y2_cam2, 'x',label='b2')
            ax.plot(x3_cam2, y3_cam2, 'x',label='b3')
            patch = get_square(x0_cam2, y0_cam2, width)
            plt.gca().add_patch(patch)
            patch = get_square(x1_cam2, y1_cam2, width)
            plt.gca().add_patch(patch)
            patch = get_square(x2_cam2, y2_cam2, width)
            plt.gca().add_patch(patch)
            patch = get_square(x3_cam2, y3_cam2, width)
            plt.gca().add_patch(patch)
            title = 'cam2'
            plt.title(title)
            #-----
            ax = plt.subplot(414)
            ax.set_xlim(0,xf_cam3-xi_cam3)
            ax.set_ylim(0,yf_cam3-yi_cam3)
            ax.autoscale(False)
            ax.imshow(cam_cam3, cmap =cm.Greys_r)
            ax.plot(x0_cam3, y0_cam3, 'x',label='b0')
            ax.plot(x1_cam3, y1_cam3, 'x',label='b1')
            ax.plot(x2_cam3, y2_cam3, 'x',label='b2')
            ax.plot(x3_cam3, y3_cam3, 'x',label='b3')
            patch = get_square(x0_cam3, y0_cam3, width)
            plt.gca().add_patch(patch)
            patch = get_square(x1_cam3, y1_cam3, width)
            plt.gca().add_patch(patch)
            patch = get_square(x2_cam3, y2_cam3, width)
            plt.gca().add_patch(patch)
            patch = get_square(x3_cam3, y3_cam3, width)
            plt.gca().add_patch(patch)
            title = 'cam3'
            plt.title(title)
            plt.show()
        #-------------------------------------------------------------------
        #plot diff
        dif = num_cam0 - num_cam1
        if num_cam1 == num_cam0:
            sync_on += 1
        else:
            sync_off += 1
            print "%sNOT SYNC: %s %s" % (RED,img,NO_COLOR)
        print "-------------------------------------------------------------"
        pattern_cam0.append(num_cam0)
        pattern_cam1.append(num_cam1)
        diff.append(dif)
        axis_x.append(i)
        if options.nosave is False:
            text_file.write('%s %s %d %d\n'%(basename, img, num_cam0, num_cam1))
        end += 1
    except Exception, e:
        print e
options.end = end
#Prepare graph
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
if options.nosave is False:
    plt.savefig(basename+'-from-%d-to-%d-pattern.png'%(options.init, options.end))
print "%.2f%% synchronized" % on
print "%.2f%% NOT synchronized" % off
print "%d total"% (len(axis_x))
if options.show is True:
    plt.show()
############### line plot #######################
plt.clf()
ax2 = plt.subplot(111)
ax2.plot(axis_x, diff, 'r-x',label='cam0 - cam1')
box = ax2.get_position()
ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
plt.ylabel('pattern diff')
plt.xlabel('image number')
title = 'img v.s pat diff: %s\nsynchronized: YES: %d , NO: %d' % (basename, sync_on, sync_off)
plt.title(title)
ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
if options.nosave is False:
    plt.savefig(basename+'-from-%d-to-%d-diff.png'%(options.init, options.end))

if options.show is True:
    plt.show()

