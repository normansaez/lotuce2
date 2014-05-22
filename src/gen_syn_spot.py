import numpy as np
from pylab import imshow,show
from math import pi
import FITS
from scipy import signal, misc
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import time

def get_subap_square(cx, cy, subap,color='red'):
    verts = [
        (cx-subap, cy-subap), # left, bottom
        (cx-subap, cy+subap), # left, top
        (cx+subap, cy+subap), # right, top
        (cx+subap, cy-subap), # right, bottom
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

def get_mask(rad=5, kernel=20):
    # syntetic img to be convolved
    rad = 5
    kernel = 20
    y,x = np.ogrid[-kernel: kernel+1, -kernel: kernel+1]
    mask = x**2+y**2 <= pi*rad**2
    mask = mask*1
    return mask

if __name__ == '__main__':
    start_time = time.time()
    #getting img to be convolved
    f = FITS.Read('bob2000407.fits')[1]
    #split img per camera
    manta76 = f[0:492,]
    manta77 = f[492:984,]
    #get mask
    mask = get_mask(rad=5,kernel=20)
    #img1
    subap = 60
    img = manta77
    cy, cx = get_centroid(img, mask)
    plt.scatter([cx], [cy],c='b',s=10)
    patch = get_subap_square(cx,cy,subap)
    plt.gca().add_patch(patch)
    patch = get_subap_square(cx,cy,subap+20,color='green')
    plt.gca().add_patch(patch)
    imshow(img)
    plt.figure(2)
    subap = 60
    img = manta76
    cy, cx = get_centroid(img, mask)
    plt.scatter([cx], [cy],c='b',s=10)
    patch = get_subap_square(cx,cy,subap)
    plt.gca().add_patch(patch)
    patch = get_subap_square(cx,cy,subap+20,color='green')
    plt.gca().add_patch(patch)
    imshow(img)
    print time.time() - start_time, "seconds"
    plt.show()
