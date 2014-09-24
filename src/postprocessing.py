import FITS
import glob
#from pylab import imshow,show
import matplotlib.pyplot as plt
#import argparse 
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
    print "Calibrating centroid pattern ..."
    usage = '''
    '''
#    parser = argparse.ArgumentParser(usage=usage)
#    parser.add_argument('-p', '--path', dest='path', type=str, help='Path to get images', default=None)
#    parser.add_argument('-t', '--template', dest='template', action='store_true', help='obtains template to convolution.', default=False)
#    (options, unknown) = parser.parse_known_args()
    # vars
    dirname = "200Hz_200plx_run1" 
    ref_path = '/home/lotuce2/lotuce2/src/ref_200Hz_200plx/'
    path = '/home/lotuce2/lotuce2/src/' + dirname

    xi76 = 201
    xf76 = 400
    yi76 = 0
    yf76 = 200

    xi77 = 0
    xf77 = 200
    yi77 = 0
    yf77 = 200

    limit = 3000

    #77 
    mask77_01 = np.where(FITS.Read(glob.glob(ref_path+'/img_000*.fits')[0])[1][xi77:xf77,yi77:yf77]> limit,1,0) 
    mask77_02 = np.where(FITS.Read(glob.glob(ref_path+'/img_001*.fits')[0])[1][xi77:xf77,yi77:yf77]> limit,1,0)
    mask77_04 = np.where(FITS.Read(glob.glob(ref_path+'/img_003*.fits')[0])[1][xi77:xf77,yi77:yf77]> limit,1,0)
    mask77_08 = np.where(FITS.Read(glob.glob(ref_path+'/img_007*.fits')[0])[1][xi77:xf77,yi77:yf77]> limit,1,0)
    #76
    mask76_01 = np.where(FITS.Read(glob.glob(ref_path+'/img_001*.fits')[0])[1][xi76:xf76,yi76:yf76]> limit,1,0) 
    mask76_02 = np.where(FITS.Read(glob.glob(ref_path+'/img_002*.fits')[0])[1][xi76:xf76,yi76:yf76]> limit,1,0)
    mask76_04 = np.where(FITS.Read(glob.glob(ref_path+'/img_004*.fits')[0])[1][xi76:xf76,yi76:yf76]> limit,1,0)
    mask76_08 = np.where(FITS.Read(glob.glob(ref_path+'/img_008*.fits')[0])[1][xi76:xf76,yi76:yf76]> limit,1,0)
    
    y0_76, x0_76 = get_centroid(mask76_01)
    y1_76, x1_76 = get_centroid(mask76_02)
    y2_76, x2_76 = get_centroid(mask76_04)
    y3_76, x3_76 = get_centroid(mask76_08)

    y0_77, x0_77 = get_centroid(mask77_01)
    y1_77, x1_77 = get_centroid(mask77_02)
    y2_77, x2_77 = get_centroid(mask77_04)
    y3_77, x3_77 = get_centroid(mask77_08)
print "GO !!"
pattern76 = []
pattern77 = []
axis_x = []
good = 0
bad = 0
for i in range(1,500+1):
    img = path+'/img_'+str(i).zfill(3)+'*.fits'
    print img
    try:
        f = FITS.Read(glob.glob(img)[0])[1]
        cam76 = f[xi76:xf76,yi76:yf76]
        b0_76 = bit_check(x0_76, y0_76, cam76, limit)
        b1_76 = bit_check(x1_76, y1_76, cam76, limit)
        b2_76 = bit_check(x2_76, y2_76, cam76, limit)
        b3_76 = bit_check(x3_76, y3_76, cam76, limit)
        num76 = '0b'+str(b3_76)+str(b2_76)+str(b1_76)+str(b0_76)
        print num76
        num76 = eval(num76)
        print num76
        cam77 = f[xi77:xf77,yi77:yf77]
        b0_77 = bit_check(x0_77, y0_77, cam77, limit)
        b1_77 = bit_check(x1_77, y1_77, cam77, limit)
        b2_77 = bit_check(x2_77, y2_77, cam77, limit)
        b3_77 = bit_check(x3_77, y3_77, cam77, limit)
        num77 = '0b'+str(b3_77)+str(b2_77)+str(b1_77)+str(b0_77)
        print num77
        num77 = eval(num77)
        print num77
        if num77 == num76:
            good += 1
        else:
            bad += 1
        pattern76.append(num76)
        pattern77.append(num77)

        axis_x.append(i)
    except IndexError, e:
        print e
fig = plt.figure()
ax = plt.subplot(111)

ax.plot(axis_x, pattern76, 'r-x',label='camera76')
ax.plot(axis_x, pattern77, 'b-x', label='camera77')

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
title = '#images v/s #patterns. %s %.1f%% bad, %.1f%% good' % (dirname, 100.*(bad*1./len(axis_x)) , 100.*(good*1./len(axis_x)))
plt.title(title)
plt.ylabel('pattern number')
plt.xlabel('image number')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig(dirname+'.png')
print "%.2f%% good" % ( 100.*(good*1./len(axis_x)))
print "%.2f%% bad" % ( 100.*(bad*1./len(axis_x)))
print "%d total"% (len(axis_x))
plt.show()

