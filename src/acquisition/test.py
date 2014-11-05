import numpy
from profilesaver import saver
a = numpy.array([11,22,9,875,26,22,88900,1,2,3,4,56,7,8,00])
print "%d => file should be %d" %(len(a), (len(a))*8)
saver(a,'test.bin')
print "######################"
from profilesaver import hydrate
b = hydrate('test.bin')
print b
