#!/usr/bin/env python
import sys
import os
import datetime
if __name__ == '__main__':
    a = datetime.datetime
    now = a.now()
    hz = sys.argv[1]
    if hz.isdigit():
        cmd = """ssh ubuntu@192.168.0.203 'sudo date -s "%s"'""" % now.strftime("%d %b %Y %H:%M:%S")
        os.system(cmd)
        cmd =   'ssh ubuntu@192.168.0.203 "sudo python /home/ubuntu/lotuce2/src/beagleclock/beagleclock.py --hertz %s"' % hz
        os.system(cmd)
