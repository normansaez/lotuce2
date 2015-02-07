import numpy
import matplotlib.pylab as plt

filename = '/home/lotuce2/lotuce2/src/acquisition/lotuce2-run-results-2015_01_22.6.txt'#os.path.normpath(options.filename)
print filename
f = open(filename,'r')
filehandler = f.readlines()
f.close()
d0 = None#datetime.datetime.fromtimestamp(1421959082.652726)
diff = []
fnos = []
counter = -70
m = [[0,0,0,0],
[0,0,0,0],
[0,0,0,0],
[0,0,0,0]]
matrix = numpy.matrix(m)
c = 0
c01 = [] 
c02 = [] 
c03 = [] 

c10 = [] 
c12 = [] 
c13 = [] 

c20 = [] 
c21 = [] 
c23 = [] 

c30 = [] 
c31 = [] 
c32 = []

for line in filehandler:
    line = line.rstrip('\n').split(' ')
    ts = float(line[0])
    fno= float(line[1])
    cam0= float(line[2])
    cam1= float(line[3])
    cam2= float(line[4])
    cam3= float(line[5])
    if counter == 0:
        break
    counter -= 1
    c01.append(cam0-cam1) 
    c02.append(cam0-cam2)
    c03.append(cam0-cam3)

    c10.append(cam1-cam0)
    c12.append(cam1-cam2)
    c13.append(cam1-cam3)

    c20.append(cam2-cam0)
    c21.append(cam2-cam1)
    c23.append(cam2-cam3)

    c30.append(cam3-cam0)
    c31.append(cam3-cam1)
    c32.append(cam3-cam2)

    c += 1

c01 = numpy.array(c01)  
c02 = numpy.array(c02)
c03 = numpy.array(c03)

c10 = numpy.array(c10)
c12 = numpy.array(c12)
c13 = numpy.array(c13)

c20 = numpy.array(c20)
c21 = numpy.array(c21)
c23 = numpy.array(c23)

c30 = numpy.array(c30)
c31 = numpy.array(c31)
c32 = numpy.array(c32)

m = [[0,c01.mean(),c02.mean(),c03.mean()],
[c10.mean(),0,c12.mean(),c13.mean()],
[c20.mean(),c21.mean(),0,c23.mean()],
[c30.mean(),c31.mean(),c32.mean(),0]]
matrix = numpy.matrix(m)
print matrix
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_aspect('equal')
plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.hot_r)
plt.colorbar()
labels = range(0, len(m[0]))
plt.xticks(labels)
plt.yticks(labels)
plt.show()
