from multiprocessing import Process
import time
import signal
import os
import time
import sys

global pid

def receive_signal(signum, stack):
    print 'Received:', signum
    pid.terminate()
#    sys.exit(0)


signal.signal(signal.SIGINT, receive_signal)
print 'My PID is:', os.getpid()

def grabb(name):
#    for i in range(5):
    i = 0
    while True:
        print "grabb %d" % i 
        time.sleep(0.5)
        i += 1

def daemon(name):
    i = 0
    while True:
        print "daemon %d" % i 
        i += 1
        time.sleep(1)

if __name__ == '__main__':
    p = Process(target=grabb, args=('',))
    p.start()
    pid = p
    print "l1"

    p1 = Process(target=daemon, args=('',))
    p1.start()

    print "l2"
    p.join()
    if p.is_alive() is False:
        p1.terminate()
        print "finish because finish"
