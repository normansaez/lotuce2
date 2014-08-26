from datetime import datetime
import matplotlib.pyplot as plt
import numpy
from matplotlib import dates
from pylab import legend

cam76ay = 820
cam76ax = 557
cam76by = 700
cam76bx = 333
cam76cy = 913
cam76cx = 320
cam76dy = 810
cam76dx = 88
cam77ay = 256
cam77ax = 190
cam77by = 200
cam77bx = 302
cam77cy = 306
cam77cx = 308
cam77dy = 254
cam77dx = 422
#plotting
fig = plt.figure()
ax = plt.subplot(111)

p1 = ax.plot(cam77ax, cam77ay,'go',label='b0')
p2 = ax.plot(cam77bx, cam77by,'ro', label='b1')
p3 = ax.plot(cam77cx, cam77cy,'yo', label='b2')
p4 = ax.plot(cam77dx, cam77dy,'bo', label='b3')
p1 = ax.plot(cam76ax, cam76ay,'gx',label='b0')
p2 = ax.plot(cam76bx, cam76by,'rx', label='b1')
p3 = ax.plot(cam76cx, cam76cy,'yx', label='b2')
p4 = ax.plot(cam76dx, cam76dy,'bx', label='b3')

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
plt.title('77=o, 76=x')
plt.ylabel('y')
plt.xlabel('x')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()             


