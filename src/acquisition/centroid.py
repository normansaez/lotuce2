import FITS
import darc
import time
import argparse 
from pprint import pprint
import numpy as np
import re
import os
import glob
from pylab import grid#imshow,show
import matplotlib.pyplot as plt

parse = argparse.ArgumentParser()
#parse.add_argument('-c', '--camera', dest='camera', type='str', help='Camera num: 0,1,2,3 etc', default="0")
parse.add_argument('-p', '--prefix', dest='prefix', type=str, help='Camera prefix: default all', default="all")
#parse.add_argument('-e', '--exptime', dest='exptime', type=int, help='Value for ExposureTimeAbs', default=1000)
parse.add_argument('-d', '--directory', dest='directory', type=str, help='directory to be store the images', default=None)
parse.add_argument('-t', '--adquisition_time', dest='adquisition_time', nargs='*', type=int, help='Image adquisition_time in seconds', default=[1])
(options, unknown) = parse.parse_known_args()

if len(options.adquisition_time) == 1:
    adquisition_time = options.adquisition_time[0]
else:
    adquisition_time = eval(str(options.adquisition_time).strip('[').rstrip(']').replace(',','*'))

print options.adquisition_time
print adquisition_time
if options.directory is None:
    path, fil = os.path.split(os.path.abspath(__file__))
    current =  str(time.strftime("%Y_%m_%d", time.gmtime()))
    current_dir = glob.glob(path+'/201*[0-90-9].*')
    current_dir.sort(key=os.path.getmtime)
    options.directory  = current_dir[-1].split('.log')[0]

    d=darc.Control(options.prefix)
    #takes camera pixels (x,y)
    pxlx =d.Get("npxlx")[0]
    pxly =d.Get("npxly")[0]
    img_to_take = int(options.adquisition_time[0])
    streamBlock = d.GetStreamBlock('%srtcCentBuf'%options.prefix,img_to_take,block=1,flysave=options.directory+'/img.fits')
    #streams = streamBlock['%srtcCentBuf'%prefix]
    #print len(streams)
    #print "###"
    #x0 = np.array([])
    #x1 = np.array([])
    #x2 = np.array([])
    #x3 = np.array([])
    #y0 = np.array([])
    #y1 = np.array([])
    #y2 = np.array([])
    #y3 = np.array([])
    #for stream in streams:
    #    print stream[0]
    #    print type(stream[0])
    #    print stream[0].shape
    #    data = stream[0]
    #    x0 = np.append(x0,data[0])
    #    y0 = np.append(x0,data[1])
    #
    #    x1 = np.append(x1,data[2])
    #    y1 = np.append(x1,data[3])
    #
    #    x2 = np.append(x2,data[4])
    #    y2 = np.append(x2,data[5])
    #
    #    x3 = np.append(x3,data[6])
    #    y3 = np.append(x3,data[7])
    #
    #cov_x = np.array([])
    #cov_x = np.append(cov_x, np.cov(x0,x1)[0][1]) 
    #cov_x = np.append(cov_x, np.cov(x0,x2)[0][1])
    #cov_x = np.append(cov_x, np.cov(x0,x3)[0][1])
    #cov_x = np.append(cov_x, np.cov(x1,x2)[0][1])
    #cov_x = np.append(cov_x, np.cov(x1,x3)[0][1])
    #cov_x = np.append(cov_x, np.cov(x2,x3)[0][1])
    #
    #cov_y = np.array([])
    #cov_y = np.append(cov_y, np.cov(y0,y1)[0][1]) 
    #cov_y = np.append(cov_y, np.cov(y0,y2)[0][1])
    #cov_y = np.append(cov_y, np.cov(y0,y3)[0][1])
    #cov_y = np.append(cov_y, np.cov(y1,y2)[0][1])
    #cov_y = np.append(cov_y, np.cov(y1,y3)[0][1])
    #cov_y = np.append(cov_y, np.cov(y2,y3)[0][1])
    #
    #
    #baselines = [2,10,15,20,50,120]
    #
    ##fig = plt.figure()
    ##ax = plt.subplot(111)
    ##ax.plot(baselines, cov_x,'ro-',label=r'$COV(X_{i},X_{i+1})$')
    ##ax.plot(baselines, cov_y,'bo-',label=r'$COV(Y_{i},Y_{i+1})$')
    ##x = ax.get_position()
    ##plt.title(r'COV(X,Y) v/s Baseline')
    ##plt.ylabel(r'$COV(XY_{i},XY_{i+1})$')
    ##plt.xlabel(r'baseline')
    ##ax.xaxis.grid(True)
    ##ax.yaxis.grid(True)
    ##ax.legend(loc='center left', bbox_to_anchor=(0.75, 0.92))
    ##plt.savefig('covx.png')
    ##plt.show()
    #
    #covariances = open('covariances.txt','w')
    #for i in range(0, len(cov_x)):
    #    covariances.write(str(cov_x[i]))
    #    covariances.write(' ')
    #    covariances.write(str(cov_y[i]))
    #    covariances.write(' ')
    #covariances.write('\n')
    #covariances.close()
    #
