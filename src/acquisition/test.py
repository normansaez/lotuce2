import numpy
from profilesaver import saver
a = numpy.array([1,3,9,875,26,22,88900,1,2,3,4,56,7,8,00])
print len(a)
saver(a,'test.dat')
