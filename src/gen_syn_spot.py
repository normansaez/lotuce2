import numpy as np
from pylab import imshow,show
from math import pi
import FITS
from scipy import signal, misc
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

# syntetic img to be convolved
rad = 5
kernel = 20
y,x = np.ogrid[-kernel: kernel+1, -kernel: kernel+1]
mask = x**2+y**2 <= pi*rad**2
mask = mask*1

#getting img to be convolved
f = FITS.Read('bob2000407.fits')[1]
#split img per camera
manta76 = f[0:492,]
manta77 = f[492:984,]

correlation = signal.fftconvolve(manta77,mask,mode='same')
#Getting max 
cy77,cx77 = np.unravel_index(correlation.argmax(),correlation.shape)
print cy77,cx77
plt.scatter([cx77], [cy77],c='b',s=10)
imshow(manta77)
#Put subap
subap = 60
verts = [
    (cx77-subap, cy77-subap), # left, bottom
    (cx77-subap, cy77+subap), # left, top
    (cx77+subap, cy77+subap), # right, top
    (cx77+subap, cy77-subap), # right, bottom
    (cx77, cy77), # ignored
    ]

codes = [Path.MOVETO,
         Path.LINETO,
         Path.LINETO,
         Path.LINETO,
         Path.CLOSEPOLY,
         ]

path = Path(verts, codes)

patch = patches.PathPatch(path, facecolor='none', EdgeColor='red', lw=1)
plt.gca().add_patch(patch)
plt.show()
