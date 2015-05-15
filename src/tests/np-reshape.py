#!/usr/bin/env python

import numpy as np

if __name__ == '__main__':
    pxly = 3
    pxlx = 5

    data = np.array(range(0,pxly*pxlx))
    
    index = 0
    col = 0
    px = 0

    for i in range(0,pxlx):
        py = 0
        for j in range(0,pxly):
            py = py + data[pxlx*j+i]
            px = px + data[index]
            col += 1
            if col >= pxlx:
                print "x>%d" % px
                col = 0
                px = 0
            index += 1
        print "  %d<y" % py
