import FITS
import glob
from time import sleep
import numpy
import numpy as np

filenames = glob.glob('*.fits')
fits_file = filenames[-1]

for fits_file in filenames:
    print "%s " % (fits_file),
    data = FITS.Read(fits_file)
    print "%s ->" % str(data[1].dtype) ,
#    y=data[1].view('h')
    y=data[1].view(np.uint32)
    print " %s" % str(y.dtype)
    FITS.Write(y,fits_file)
