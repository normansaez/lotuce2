#!/usr/bin/env python
import sys
import os
import datetime
import platform

if __name__ == '__main__':
    a = datetime.datetime
    now = a.now()
    hz = sys.argv[1]
    if hz.isdigit():
        user = "ubuntu"
        ipadd = "192.168.0.203"
        home = "/home/%s" % user

        if platform.dist()[0] == 'debian':
            user = "root"
            ipadd = "192.168.0.16"
            home ="/%s" % user

        cmd1 = """ssh %s@%s 'sudo date -s "%s"'""" % (user, ipadd, now.strftime("%d %b %Y %H:%M:%S"))
        cmd2 =   'ssh %s@%s "sudo python %s/lotuce2/src/beagleclock/beagleclock.py --hertz %s"' % (user, ipadd, home, hz)
#        print cmd1
#        print cmd2
        os.system(cmd1)
        os.system(cmd2)

