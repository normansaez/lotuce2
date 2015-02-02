#!/usr/bin/python
import datetime
from pylab import grid#imshow,show
import matplotlib.pyplot as plt
import matplotlib.cm as cm

#filename = 'lotuce2-run-results-2015_01_27.16.txt'#os.path.normpath(options.filename)
#filename = 'lotuce2-run-results-2015_01_25.20.txt'
#filename = 'lotuce2-run-results-2014_11_02.5.txt'
#filename = 'lotuce2-run-results-2015_01_24.13.txt'
filename = '/Users/nsaez/datasets/A/lotuce2-run-results-2015_01_23.11.txt'#'/home/lotuce2/lotuce2/src/acquisition/lotuce2-run-results-2015_01_22.6.txt'#os.path.normpath(options.filename)
print filename
f = open(filename,'r')
filehandler = f.readlines()
f.close()
d0 = None#datetime.datetime.fromtimestamp(1421959082.652726)
diff = []
fnos = []
counter = 20
x = []
y = []
hz = 0
for line in filehandler:
    line = line.rstrip('\n').split(' ')
    ts = float(line[0])
    fno= float(line[1])
    d = datetime.datetime.fromtimestamp(ts)
    y.append(d)
    x.append(fno)
    if counter == 0:
        break
    counter -= 1
fig = plt.figure()
ax = plt.subplot(111)
print len(x)
print len(y)
#print len(diff)
ax.plot(y,x,'r-',label='')
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.xaxis.grid(True)
grid()
plt.show()

