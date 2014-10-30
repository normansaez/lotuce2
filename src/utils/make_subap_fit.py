import FITS
import numpy

#cam0
y0_cam0 = 140
x0_cam0 = 190
y1_cam0 = 132
x1_cam0 = 143
y2_cam0 =127
x2_cam0 = 71
y3_cam0 =147
x3_cam0 = 5
#cam1
y0_cam1 = 115
x0_cam1 = 8
y1_cam1 = 108
x1_cam1 = 54
y2_cam1 = 105
x2_cam1 = 125
y3_cam1 = 120 
x3_cam1 = 192

x_side = 3
y_side = 3

b0 = numpy.array([[y0_cam0 - y_side , y0_cam0 + y_side, 1, x0_cam0 - x_side, x0_cam0 + x_side, 1]])
b1 = numpy.array([[y1_cam0 - y_side , y1_cam0 + y_side, 1, x1_cam0 - x_side, x1_cam0 + x_side, 1]])
b2 = numpy.array([[y2_cam0 - y_side , y2_cam0 + y_side, 1, x2_cam0 - x_side, x2_cam0 + x_side, 1]])
b3 = numpy.array([[y3_cam0 - y_side , y3_cam0 + y_side, 1, x3_cam0 - x_side, x3_cam0 + x_side, 1]])
cam0_subap = numpy.concatenate((b0,b1,b2,b3),0) 
FITS.Write(cam0_subap, 'cam0_subap.fits', writeMode='w')

b0 = numpy.array([[y0_cam1 - y_side , y0_cam1 + y_side, 1, x0_cam1 - x_side, x0_cam1 + x_side, 1]])
b1 = numpy.array([[y1_cam1 - y_side , y1_cam1 + y_side, 1, x1_cam1 - x_side, x1_cam1 + x_side, 1]])
b2 = numpy.array([[y2_cam1 - y_side , y2_cam1 + y_side, 1, x2_cam1 - x_side, x2_cam1 + x_side, 1]])
b3 = numpy.array([[y3_cam1 - y_side , y3_cam1 + y_side, 1, x3_cam1 - x_side, x3_cam1 + x_side, 1]])
cam1_subap = numpy.concatenate((b0,b1,b2,b3),0)
FITS.Write(cam1_subap, 'cam1_subap.fits', writeMode='w')

