import FITS
import glob
import time
from pylab import imshow,show
import matplotlib.pyplot as plt
import argparse 
import sys
import numpy as np
from skimage.measure import regionprops
#from skimage.morphology import label
from skimage.measure import label
if __name__=="__main__":
    usage = '''
    '''
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-p', '--path', dest='path', type=str, help='Path to get images', default=None)
    parser.add_argument('-t', '--template', dest='template', action='store_true', help='obtains template to convolution.', default=False)
    (options, unknown) = parser.parse_known_args()
    path = '/Users/nsaez/Downloads/run1/'
    xi76 = 493
    xf76 = 984
    yi76 = 0
    yf76 = 656

    xi77 = 0
    xf77 = 492
    yi77 = 0
    yf77 = 656

    limit = 1500
    #76
    mask76_00 = np.where(FITS.Read(glob.glob(path+'/img_003*.fits')[0])[1][xi76:xf76,yi76:yf76]> limit,1,0)  
    mask76_01 = np.where(FITS.Read(glob.glob(path+'/img_004*.fits')[0])[1][xi76:xf76,yi76:yf76]> limit,1,0) 
    mask76_02 = np.where(FITS.Read(glob.glob(path+'/img_005*.fits')[0])[1][xi76:xf76,yi76:yf76]> limit,1,0)
    mask76_03 = np.where(FITS.Read(glob.glob(path+'/img_006*.fits')[0])[1][xi76:xf76,yi76:yf76]> limit,1,0)
    mask76_04 = np.where(FITS.Read(glob.glob(path+'/img_007*.fits')[0])[1][xi76:xf76,yi76:yf76]> limit,1,0)
    mask76_05 = np.where(FITS.Read(glob.glob(path+'/img_008*.fits')[0])[1][xi76:xf76,yi76:yf76]> limit,1,0)
    mask76_06 = np.where(FITS.Read(glob.glob(path+'/img_024*.fits')[0])[1][xi76:xf76,yi76:yf76]> limit,1,0)
    mask76_07 = np.where(FITS.Read(glob.glob(path+'/img_009*.fits')[0])[1][xi76:xf76,yi76:yf76]> limit,1,0)
    mask76_08 = np.where(FITS.Read(glob.glob(path+'/img_010*.fits')[0])[1][xi76:xf76,yi76:yf76]> limit,1,0)
    mask76_09 = np.where(FITS.Read(glob.glob(path+'/img_011*.fits')[0])[1][xi76:xf76,yi76:yf76]> limit,1,0)
    mask76_10 = np.where(FITS.Read(glob.glob(path+'/img_012*.fits')[0])[1][xi76:xf76,yi76:yf76]> limit,1,0)
    mask76_11 = np.where(FITS.Read(glob.glob(path+'/img_013*.fits')[0])[1][xi76:xf76,yi76:yf76]> limit,1,0)
    mask76_12 = np.where(FITS.Read(glob.glob(path+'/img_014*.fits')[0])[1][xi76:xf76,yi76:yf76]> limit,1,0)
    mask76_13 = np.where(FITS.Read(glob.glob(path+'/img_015*.fits')[0])[1][xi76:xf76,yi76:yf76]> limit,1,0)
    mask76_14 = np.where(FITS.Read(glob.glob(path+'/img_016*.fits')[0])[1][xi76:xf76,yi76:yf76]> limit,1,0)
    mask76_15 = np.where(FITS.Read(glob.glob(path+'/img_017*.fits')[0])[1][xi76:xf76,yi76:yf76]> limit,1,0)
    #77 
    mask77_00 = np.where(FITS.Read(glob.glob(path+'/img_004*.fits')[0])[1][xi77:xf77,yi77:yf77]> limit,1,0)
    mask77_01 = np.where(FITS.Read(glob.glob(path+'/img_005*.fits')[0])[1][xi77:xf77,yi77:yf77]> limit,1,0) 
    mask77_02 = np.where(FITS.Read(glob.glob(path+'/img_006*.fits')[0])[1][xi77:xf77,yi77:yf77]> limit,1,0)
    mask77_03 = np.where(FITS.Read(glob.glob(path+'/img_007*.fits')[0])[1][xi77:xf77,yi77:yf77]> limit,1,0)
    mask77_04 = np.where(FITS.Read(glob.glob(path+'/img_008*.fits')[0])[1][xi77:xf77,yi77:yf77]> limit,1,0)
    mask77_05 = np.where(FITS.Read(glob.glob(path+'/img_024*.fits')[0])[1][xi77:xf77,yi77:yf77]> limit,1,0)
    mask77_06 = np.where(FITS.Read(glob.glob(path+'/img_009*.fits')[0])[1][xi77:xf77,yi77:yf77]> limit,1,0)
    mask77_07 = np.where(FITS.Read(glob.glob(path+'/img_010*.fits')[0])[1][xi77:xf77,yi77:yf77]> limit,1,0)
    mask77_08 = np.where(FITS.Read(glob.glob(path+'/img_011*.fits')[0])[1][xi77:xf77,yi77:yf77]> limit,1,0)
    mask77_09 = np.where(FITS.Read(glob.glob(path+'/img_012*.fits')[0])[1][xi77:xf77,yi77:yf77]> limit,1,0)
    mask77_10 = np.where(FITS.Read(glob.glob(path+'/img_013*.fits')[0])[1][xi77:xf77,yi77:yf77]> limit,1,0)
    mask77_11 = np.where(FITS.Read(glob.glob(path+'/img_014*.fits')[0])[1][xi77:xf77,yi77:yf77]> limit,1,0)
    mask77_12 = np.where(FITS.Read(glob.glob(path+'/img_015*.fits')[0])[1][xi77:xf77,yi77:yf77]> limit,1,0)
    mask77_13 = np.where(FITS.Read(glob.glob(path+'/img_016*.fits')[0])[1][xi77:xf77,yi77:yf77]> limit,1,0)
    mask77_14 = np.where(FITS.Read(glob.glob(path+'/img_017*.fits')[0])[1][xi77:xf77,yi77:yf77]> limit,1,0)
    mask77_15 = np.where(FITS.Read(glob.glob(path+'/img_018*.fits')[0])[1][xi77:xf77,yi77:yf77]> limit,1,0)
        
#    plt.imshow(mask77_15,origin='lower') #to make it fit with ds9
#    plt.show()

#    if options.path is None:
#        print "give a image source path"
#        sys.exit(-1)
#    images = glob.glob(options.path+'/img_*')
#    images = sorted(images)
#    plt.ion()
#    plt.figure()
#    for i in images:
#        print i
#        f = FITS.Read(i)[1]
#        plt.imshow(f)
#        plt.draw()
#        time.sleep(1)
#        
label_img = label(mask76_15)
regions = regionprops(label_img)

for props in regions:
    y0, x0 = props.centroid
    print y0, x0 

#for i in range(1,83+1):
#    img = path+'img_'+str(i).zfill(3)+'*.fits'
#    print img
#    f = FITS.Read(glob.glob(img)[0])[1]
#    cam76 = f[xi76:xf76,yi76:yf76]
#    plt.imshow(cam76, origin='lower')
#    plt.show()
#    for j in range(0,15+1):
#        mask = eval('mask76_%s' % str(j).zfill(2))
#        print str(j).zfill(2)
#        #correlation = signal.fftconvolve(cam76,mask,mode='same')
#        correlation = mask*cam76
#        plt.imshow(correlation, origin='lower')
#        plt.show()
#    break
