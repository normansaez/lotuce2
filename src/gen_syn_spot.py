import numpy as np
from pylab import imshow,show
from math import pi
import FITS
from scipy import signal, misc
import matplotlib.pyplot as plt

rad = 15
subap = 50
y,x = np.ogrid[-subap: subap+1, -subap: subap+1]
mask = x**2+y**2 <= pi*rad**2
mask = mask*1
#plt.figure(1)
#imshow(mask)
#show()
f = FITS.Read('bob2000407.fits')[1]
print f.shape
manta76 = f[0:492,]
print manta76.shape
manta77 = f[492:984,]
print manta77.shape
#plt.figure(2)
#imshow(manta76)
#show()
#plt.figure(3)
#imshow(manta77)
#show()

correlacion = signal.fftconvolve(manta76,mask,mode='same')
#plt.figure(4)
#imshow(correlacion)
#show()
cy,cx = np.unravel_index(correlacion.argmax(),correlacion.shape)
print cy,cx
imshow(manta76)
plt.show()
