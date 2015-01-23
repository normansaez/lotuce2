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
    m = [[0,cam0-cam1,cam0-cam2,cam0-cam3],
    [cam1-cam0,0,cam1-cam2,cam1-cam3],
    [cam2-cam0,cam2-cam1,0,cam2-cam3],
    [cam3-cam0,cam3-cam1,cam3-cam2,0]]
    mtrx = numpy.matrix(m)
    matrix = matrix + mtrx
    c += 1
print c
print matrix
print matrix/c
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_aspect('equal')
plt.imshow(matrix/c, interpolation='nearest', cmap=plt.cm.hot_r)
plt.colorbar()
labels = range(0, len(m[0]))
plt.xticks(labels)
plt.yticks(labels)
plt.show()
