import FITS
import glob
from time import sleep
import numpy
#import numpy as np

filenames = glob.glob('14avril2014/*/*/*.fits')
fits_file = filenames[-1]

for fits_file in filenames:
    print "%s " % (fits_file)
    data = FITS.Read(fits_file)
    print "from %s at %s" % (str(data[1].shape) ,str(data[1].dtype))
    #print "%s :" % str(data[1].shape) +'at '+str(data[1].dtype),
    y=data[1].astype('int32')
    #print "%s ->" % str(y.shape) +'at '+str(y.dtype)
    print "to %s at %s" % (str(y.shape), str(y.dtype))
    FITS.Write(y,fits_file)
