import numpy as np
from pylab import imshow,show
from math import pi
import FITS
from scipy import signal, misc
import matplotlib.pyplot as plt

# syntetic img to be convolved
rad = 10
subap = 20
y,x = np.ogrid[-subap: subap+1, -subap: subap+1]
mask = x**2+y**2 <= pi*rad**2
mask = mask*1

#getting img to be convolved
f = FITS.Read('bob2000407.fits')[1]
#split img per camera
manta76 = f[0:492,]
manta77 = f[492:984,]

correlation = signal.fftconvolve(manta76,mask,mode='same')
#Getting max 
cy76,cx76 = np.unravel_index(correlation.argmax(),correlation.shape)
print cy76,cx76
# put a blue dot at (10, 20)
plt.scatter([cx76], [cy76],c='r',s=40)

# put a red dot, size 40, at 2 locations:
#plt.scatter(x=[30, 40], y=[50, 60], c='r', s=40)

imshow(manta76)
plt.show()
