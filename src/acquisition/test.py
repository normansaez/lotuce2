import numpy
from profilesaver import saver
a = numpy.array([1,3,9,875,26,22,88900,1,2,3,4,56,7,8,00])
#a = numpy.array([1])
print "%d => file should be %d" %(len(a), (len(a))*8)
saver(a,'test.dat')
