import numpy as np
from pylab import imshow,show
from math import pi
import FITS
from scipy import signal, misc
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import time

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

def get_centroid(img, mask):
    correlation = signal.fftconvolve(img,mask,mode='same')
    #Getting max 
    cy, cx = np.unravel_index(correlation.argmax(),correlation.shape)
    return cy,cx

def get_mask_spot(radio=5, kernel=20):
    # syntetic img to be convolved
    y,x = np.ogrid[-kernel: kernel+1, -kernel: kernel+1]
    mask = x**2+y**2 <= pi*radio**2
    mask = mask*1
    return mask

if __name__ == '__main__':
    start_time = time.time()
    #getting img to be convolved
    f = FITS.Read('bob2000407.fits')[1]
    #split img per camera
    manta76 = f[0:492,]
    manta77 = f[492:984,]
    weight = 120
    height = weight
    subap = 60
    radio = 5
    kernel = 20
    #get mask
    mask = get_mask_spot(radio,kernel)
    #img1
    img = manta77
    cy, cx = get_centroid(img, mask)
    #plt.scatter([cx], [cy],c='b',s=10)
    patch = get_square(cx,cy,subap)
    plt.gca().add_patch(patch)
    patch = get_square(cx,cy,height,color='green')
    plt.gca().add_patch(patch)
    imshow(img)
########################################
    plt.figure(2)
    #img1
    img = manta76
    cy, cx = get_centroid(img, mask)
    #plt.scatter([cx], [cy],c='b',s=10)
    patch = get_square(cx,cy,subap)
    plt.gca().add_patch(patch)
    patch = get_square(cx,cy,height,color='green')
    plt.gca().add_patch(patch)
    imshow(img)
    print time.time() - start_time, "seconds"
    plt.show()
