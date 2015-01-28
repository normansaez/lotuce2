#!/usr/bin/python
import datetime
from pylab import grid#imshow,show
import matplotlib.pyplot as plt
import matplotlib.cm as cm

#filename = 'lotuce2-run-results-2015_01_27.16.txt'#os.path.normpath(options.filename)
#filename = 'lotuce2-run-results-2015_01_25.20.txt'
#filename = 'lotuce2-run-results-2014_11_02.5.txt'
filename = 'lotuce2-run-results-2015_01_24.13.txt'
print filename
f = open(filename,'r')
filehandler = f.readlines()
f.close()
d0 = None#datetime.datetime.fromtimestamp(1421959082.652726)
diff = []
fnos = []
counter = -500
x = []
y = []
hz = 0
for line in filehandler:
    line = line.rstrip('\n').split(' ')
    ts = float(line[0])
    fno= float(line[1])
    d = datetime.datetime.fromtimestamp(ts)
    if d0 == None:
        hz = fno
    else:
        hz =  fno#d + datetime.timedelta(0,0.01)
#        d0 = d - datetime.timedelta(0,0.01)
#    sec_diff = (d - d0).total_seconds()
#    diff.append(sec_diff)
#    fnos.append(fno)
    d0 = d
    y.append(d)
    x.append(hz)
    
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

