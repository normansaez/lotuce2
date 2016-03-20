#!/usr/bin/python
import os
import argparse
import pypruss

from math import ceil

if __name__ == '__main__':
    pru = 0
    firmware = "./clock.bin"
    pypruss.modprobe()                                  # This only has to be called once pr boot
    pypruss.init()                                      # Init the PRU
    pypruss.open(pru)                                   # Open PRU event <num> which is PRU<num>_ARM_INTERRUPT
    pypruss.pruintc_init()                              # Init the interrupt controller
    pypruss.exec_program(pru, firmware)                 # Load firmware on PRU <num>
    pypruss.wait_for_event(pru)                         # Wait for event <num> which is connected to PRU<num>_ARM_INTERRUPT
    pypruss.clear_event(pru)                            # Clear the event
    pypruss.pru_disable(pru)                            # Disable PRU <num>, this is already done by the firmware
    pypruss.exit()                                      # Exit, don't know what this does.


