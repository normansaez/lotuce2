import time
import os
import multiprocessing as mp
import datetime
import glob
import signal
import sys
import argparse 

parse = argparse.ArgumentParser()
parse.add_argument('-d', '--directory', dest='directory', type=str, help='directory to be store the images', default=None)
(options, unknown) = parse.parse_known_args()

def move_files(filenames, dst):
    t0 = datetime.datetime.utcnow() 
    filenames = glob.glob(src_dirname+'/*')
    if not os.path.exists(dst_dirname) and len(filenames)>1:
        os.makedirs(dst_dirname)
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

    src_dirname = options.directory
    dst_dirname = os.path.split(os.path.abspath(__file__))[0]
    filenames = []
    sts = mp.Queue()
    signal.signal(signal.SIGINT, signal_handler)
    count = 0
    while(count <= 1):
        dst_dirname = dst_dirname+'/'+str(time.strftime("%Y_%m_%dT%H_%M", time.localtime()))
        dst_dirname = os.path.normpath(dst_dirname)
        filenames=None
        p = mp.Process(target=move_files, args=(filenames, dst_dirname))
        p.start()
        p.join()
        print sts.get().total_seconds()
        dst_dirname = os.path.split(os.path.abspath(__file__))[0]
        count += 1
