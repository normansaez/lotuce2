from pylab import *
from math import pi
#fig = figure()
#axe = fig.gca(polar=True)
#thetas = linspace(0,2*pi,200)
#rhos = 3+cos(5*thetas)
#axe.plot(thetas, rhos)
#fig.show()


#filename = 'lotuce2-run-results-2015_01_25.20.txt'
filename = 'lotuce2-run-results-2015_01_24.16.txt'
f = open(filename,'r')
filehandler = f.readlines()
f.close()


fig=plt.figure()
axe=fig.gca(polar=True)
c0_rhos = []
c0_thetas = []

c1_rhos = []
c1_thetas = []

c2_rhos = []
c2_thetas = []

c3_rhos = []
c3_thetas = []

cam0s = []
cam1s = []
cam2s = []
cam3s = []
count = 0

limit = 50
fni = None
deg2rad = 22.5*(pi/180.)
for line in filehandler:
    line = line.rstrip('\n').split(' ')
    ts = float(line[0])
    fno= float(line[1])
    cam0= float(line[2])
    cam1= float(line[3])
    cam2= float(line[4])
    cam3= float(line[5])
    if fni is None:
        fni = fno
        fno = 0
    else:
        fno = fno - fni
    c0_thetas.append(cam0*deg2rad)
    c0_rhos.append(fno)
    cam0s.append(cam0)

    c1_thetas.append(cam1*deg2rad)
    c1_rhos.append(fno)
    cam1s.append(cam1)

    c2_thetas.append(cam2*deg2rad)
    c2_rhos.append(fno)
    cam2s.append(cam2)

    c3_thetas.append(cam3*deg2rad)
    c3_rhos.append(fno)
    cam3s.append(cam3)

    if count == limit:
        break
    count += 1
for i in range(0, limit):
    print "c0: t(%.1f) r(%.1f) c(%d)" % (c0_thetas[i],c0_rhos[i],cam0s[i])
    print "c1: t(%.1f) r(%.1f) c(%d)" % (c1_thetas[i],c1_rhos[i],cam1s[i])
    print "c2: t(%.1f) r(%.1f) c(%d)" % (c2_thetas[i],c2_rhos[i],cam2s[i])
    print "c3: t(%.1f) r(%.1f) c(%d)" % (c3_thetas[i],c3_rhos[i],cam3s[i])
    print

axe.plot(c0_thetas, c0_rhos,'r')
axe.plot(c1_thetas, c1_rhos,'b')
axe.plot(c2_thetas, c2_rhos,'y')
axe.plot(c3_thetas, c3_rhos,'g')
xT=  [i*deg2rad for i in range(0,16)]
#xL=['0',r'$\frac{\pi}{4}$',r'$\frac{\pi}{2}$',r'$\frac{3\pi}{4}$',r'$\pi$',r'$\frac{5\pi}{4}$',r'$\frac{3\pi}{2}$',r'$\frac{7\pi}{4}$']
xL=['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']
plt.xticks(xT, xL)
plt.show()
