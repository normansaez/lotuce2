import numpy as np
from pprint import pprint
from matplotlib import pyplot as plt


size = 200
subap = [  4, 196,   1,  24, 176,   1]
# [ystart, yend, ystep, xstart, xend, xstep].
matrix = np.zeros(size*size).reshape(size,size)
#print (subap[3], subap[0])
#print (subap[4], subap[1])
matrix[subap[3],subap[0]] = 1
matrix[subap[4],subap[1]] = 1

plt.imshow(matrix, interpolation='nearest')
plt.show()
