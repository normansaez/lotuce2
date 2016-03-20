#!/usr/bin/env python
import sys
import os
import datetime
import argparse

if __name__ == '__main__':
    a = datetime.datetime
    now = a.now()
    parse = argparse.ArgumentParser()
    parse.add_argument('--hertz', dest='hertz', type=int, help='Value for clock in Hertz', default=None)
    (options, unknown) = parse.parse_known_args()
    
    hz = options.hertz
    if hz is None:
        print "\n\n\nFREQUENCY DOES NOT SET !\n\n\nUsage: %s --hertz <num>\n\nexample:\n\n%s --hertz 80" % (__file__,__file__)
        sys.exit(0)

    print "Hertz to reach: %d" % options.hertz
    user = "root"
    ipadd = "192.168.0.16"
    home ="/%s" % user

    cmd1 = """ssh %s@%s 'sudo date -s "%s"'""" % (user, ipadd, now.strftime("%d %b %Y %H:%M:%S"))
    cmd2 =   'ssh %s@%s "sudo python %s/lotuce2/src/beagleclock/beagleclock.py --hertz %s"' % (user, ipadd, home, hz)

    print cmd1
    print cmd2
    os.system(cmd1)
    os.system(cmd2)

