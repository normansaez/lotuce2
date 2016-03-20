#!/usr/bin/python
import os
import argparse
import pypruss

from math import ceil

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('--hertz', dest='hertz', type=int, help='Value for clock in Hertz', default=100)
    (options, unknown) = parse.parse_known_args()

    print "Hertz to reach: %d" % options.hertz
    hertz = options.hertz
    max_hertz = 200e6 #PRU clock max frequency
    filename = 'clock.p'
    path, fil = os.path.split(os.path.abspath(os.path.realpath(__file__)))
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
    fp = file(filename, 'w')
    fp.write(generate_code)
    fp.close()
    cmd = "make -C %s clean all" % path
    print cmd
    os.system(cmd)

    pypruss.modprobe()                                  # This only has to be called once pr boot
    pypruss.init()                                      # Init the PRU
    pypruss.open(0)                                     # Open PRU event 0 which is PRU0_ARM_INTERRUPT
    pypruss.pruintc_init()                              # Init the interrupt controller
    pypruss.exec_program(0, "./clock.bin")              # Load firmware "clock.bin" on PRU 0
#    pypruss.wait_for_event(0)                           # Wait for event 0 which is connected to PRU0_ARM_INTERRUPT
#    pypruss.clear_event(0)                              # Clear the event
#    pypruss.pru_disable(0)                              # Disable PRU 0, this is already done by the firmware
#    pypruss.exit()                                      # Exit, don't know what this does.
    print "Constant to reach %d hertz: %d" % (hertz, constant)

