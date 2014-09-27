from datetime import datetime
import matplotlib.pyplot as plt
import numpy
from matplotlib import dates
from pylab import legend

cam76b0y = 820
cam76b0x = 557
cam76b1y = 700
cam76b1x = 333
cam76b2y = 913
cam76b2x = 320
cam76b3y = 810
cam76b3x = 88
cam77b0y = 256
cam77b0x = 190
cam77b1y = 200
cam77b1x = 302
cam77b2y = 306
cam77b2x = 308
cam77b3y = 254
cam77b3x = 422
#plotting
fig = plt.figure()
ax = plt.subplot(111)
b0 = 1
b1 = 1 
b2 = 1 
b3 = 1

b0color76 =  'go'
b1color76 =  'ro'
b2color76 =  'yo'
b3color76 =  'bo'
b0color77 =  'gx'
b1color77 =  'rx'
b2color77 =  'yx'
b3color77 =  'bx'
if b0 == 0:
    b0color76 = 'wx'
    b0color77 = 'wx'
if b1 == 0:
    b1color76 = 'wx'
    b1color77 = 'wx'
if b2 == 0:
    b2color76 = 'wx'
    b2color77 = 'wx'
if b3 == 0:
    b3color76 = 'wx'
    b3color77 = 'wx'

ax.plot(cam77b0x, cam77b0y, b0color77,label='b0')
ax.plot(cam77b1x, cam77b1y, b1color77, label='b1')
ax.plot(cam77b2x, cam77b2y, b2color77, label='b2')
ax.plot(cam77b3x, cam77b3y, b3color77, label='b3')
ax.plot(cam76b0x, cam76b0y, b0color76,label='b0')
ax.plot(cam76b1x, cam76b1y, b1color76, label='b1')
ax.plot(cam76b2x, cam76b2y, b2color76, label='b2')
ax.plot(cam76b3x, cam76b3y, b3color76, label='b3')

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
title = '77=o, 76=x b=%d%d%d%d = %d'% (b3,b2,b1,b0, b3*2**3+b2*2**2+b1*2**1+b0*2**0)
plt.title(title)
plt.ylabel('y')
plt.xlabel('x')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()             
