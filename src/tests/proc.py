from multiprocessing import Process
import time
import signal
import os
import sys
from subprocess import Popen, PIPE

global pid

def receive_signal(signum, stack):
    print 'Received:', signum
    pid.terminate()
#    sys.exit(0)


signal.signal(signal.SIGINT, receive_signal)
print 'My PID is:', os.getpid()

def grabb(name):
    cmd = 'while true; do echo "grabbing"; sleep 1; done'
    process = Popen(cmd , stdout=PIPE , stderr=PIPE , shell=True)
    print process.pid
    process.wait()

def daemon(name):
    cmd = 'while true; do echo "daemon"; sleep 2; done'
    process = Popen(cmd , stdout=PIPE , stderr=PIPE , shell=True)
    print process.pid
    process.terminate()
    process.wait()

if __name__ == '__main__':
    p = Process(target=grabb, args=('',))
    p.start()
    pid = p

    p1 = Process(target=daemon, args=('',))
    p1.start()
    print pid
    p.join()
    if p.is_alive() is False:
        p1.terminate()
        print "finish because finish"

