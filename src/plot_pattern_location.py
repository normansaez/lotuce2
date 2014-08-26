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
ax.plot(b0*cam77b0x, b0*cam77b0y,'go',label='b0')
ax.plot(b1*cam77b1x, b1*cam77b1y,'ro', label='b1')
ax.plot(b2*cam77b2x, b2*cam77b2y,'yo', label='b2')
ax.plot(b3*cam77b3x, b3*cam77b3y,'bo', label='b3')
ax.plot(b0*cam76b0x, b0*cam76b0y,'gx',label='b0')
ax.plot(b1*cam76b1x, b1*cam76b1y,'rx', label='b1')
ax.plot(b2*cam76b2x, b2*cam76b2y,'yx', label='b2')
ax.plot(b3*cam76b3x, b3*cam76b3y,'bx', label='b3')

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
title = '77=o, 76=x b=%d%d%d%d = %d'% (b3,b2,b1,b0, b3*2**3+b2*2**2+b1*2**1+b0*2**0)
plt.title(title)
plt.ylabel('y')
plt.xlabel('x')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()             
