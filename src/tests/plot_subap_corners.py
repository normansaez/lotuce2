import numpy as np
from pprint import pprint
from matplotlib import pyplot as plt


sizeY = 656#200
sizeX = 492
#subap = [  4, 196,   1,  24, 176,   1]
subap = [4, 488,   1,  24, 632,   1]
# [ystart, yend, ystep, xstart, xend, xstep].
matrix = np.zeros(sizeX*sizeY).reshape(sizeX,sizeY)
#print (subap[3], subap[0])
#print (subap[4], subap[1])
#matrix[subap[3],subap[0]] = 1
#matrix[subap[4],subap[1]] = 1
matrix[subap[0],:] = 1
matrix[subap[1],:] = 1
matrix[:,subap[3]] = 1
matrix[:,subap[4]] = 1
print 200- 4
print 200- 24
print 200- 196
print 200- 176
plt.imshow(matrix, interpolation='nearest')
plt.show()
