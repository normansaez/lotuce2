#!/usr/bin/python
import os
import argparse

from math import ceil

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('--hertz', dest='hertz', type=int, help='Value for clock in Hertz', default=100)
    (options, unknown) = parse.parse_known_args()

    print "Hertz to reach: %d" % options.hertz
    hertz = options.hertz
    max_hertz = 200e6 #PRU clock max frequency
    filename = 'clock.p'
    constant = int(ceil((max_hertz - hertz*5)/(hertz*4.)))
    print "Constant to reach %d hertz: %d" % (hertz, constant)

    generate_code = """.origin 0
.entrypoint START

#include "clock.hp"

#ifdef DELAY_TIME
START:
    SET r30.t14
    MOV r0, DELAY_TIME 

DELAY: 
    SUB r0,r0,1
    QBNE DELAY, r0,0
    
    CLR r30.t14

    MOV r0, DELAY_TIME

DELAY2:
    SUB r0, r0, %d
    QBNE DELAY2, r0, 0

    JMP START

#else
START:
    SET r30.t14
    CLR r30.t14
    JMP START

#endif""" % constant

    if os.path.exists(filename):
        os.remove(filename)
    else:
        fp = file(filename, 'w')
        fp.write(generate_code)
        fp.close()

    os.system('make -C . clean all run')
