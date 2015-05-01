import time
import os
import multiprocessing as mp
import datetime
import glob
import signal
import sys
import argparse 

parse = argparse.ArgumentParser()
#parse.add_argument('-c', '--camera', dest='camera', type='str', help='Camera num: 0,1,2,3 etc', default="0")
parse.add_argument('-p', '--prefix', dest='prefix', type=str, help='Camera prefix: default all', default="all")
#parse.add_argument('-e', '--exptime', dest='exptime', type=int, help='Value for ExposureTimeAbs', default=1000)
parse.add_argument('-d', '--directory', dest='directory', type=str, help='directory to be store the images', default=None)
parse.add_argument('-t', '--adquisition_time', dest='adquisition_time', nargs='*', type=int, help='Image adquisition_time in seconds', default=[1])
(options, unknown) = parse.parse_known_args()


def move_files(filenames, dst):
    t0 = datetime.datetime.utcnow() 
    for src in filenames:
        try:
            cmd = "mv %s %s" % (src, dst)
            print cmd
            os.system(cmd)
        except Exception, e:
            print e
    t1 = datetime.datetime.utcnow()
    sts.put(t1 - t0)

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

if __name__ == '__main__':

    src_dirname = '/home/lotuce2/lotuce2/src/acquisition/2015_04_23.13/'
    dst_dirname = os.path.split(os.path.abspath(__file__))[0]
    filenames = []
    sts = mp.Queue()
    signal.signal(signal.SIGINT, signal_handler)
    while(True):
        dst_dirname = dst_dirname+'/'+str(time.strftime("%Y_%m_%dT%H_%M", time.localtime()))
        dst_dirname = os.path.normpath(dst_dirname)
        filenames = glob.glob(src_dirname+'/*')
        if not os.path.exists(dst_dirname) and len(filenames)>1:
            os.makedirs(dst_dirname)
        p = mp.Process(target=move_files, args=(filenames, dst_dirname))
        p.start()
        p.join()
        print sts.get().total_seconds()
        dst_dirname = os.path.split(os.path.abspath(__file__))[0]
        
