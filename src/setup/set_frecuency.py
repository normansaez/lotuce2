import sys
import os

if __name__ == '__main__':
    hz = sys.argv[1]
    if hz.isdigit():
        cmd =   'ssh ubuntu@192.168.0.203 "sudo python /home/ubuntu/bbb-pru-clock/blinkled.py %s"' % hz
        os.system(cmd)
