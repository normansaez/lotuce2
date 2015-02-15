#!/usr/bin/python
import sys
import os
from pylab import grid
import matplotlib.pyplot as plt
import argparse 
import datetime
import numpy as np
import pandas as pd


if __name__=="__main__":
    usage = '''
    '''
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-f', '--filename', dest='filename', type=str, help='Path to get txt source', default=None)
    parser.add_argument('-s', '--sfilename', dest='sfilename', type=str, help='Path to get txt source', default=None)
    parser.add_argument('-l', '--limit', dest='limit', type=int, help='Default limit to plot', default=None)#131100)#393300)#786600)#None)
    parser.add_argument('--hertz', dest='hertz', type=int, help='Herzt to be plotted', default=220)

    (options, unknown) = parser.parse_known_args()

    if options.filename is None:
        print "No filename to be to analised, you need give a path for the filename"
        print "Use -f /path/to/the/filename"
        sys.exit(-1)

    exp = []
    freq = 1./options.hertz
    m_cols = ['ts', 'id', 'cam0', 'cam1', 'cam2', 'cam3']


    options.filename = os.path.normpath(options.filename)
    basename = os.path.basename(options.filename)
    filename = os.path.normpath(options.filename)
    print filename
    color = 'g.'
    exp.append(filename.split('/')[-2])
    experiment = exp[0]
    filedata = pd.read_csv(options.filename, sep=' ', names=m_cols)
    runexec = basename.split('-')[3].replace('_','-').split('.')
    ids1 = filedata['id']
    #
    #Calculating deriv
    #
    np_ids1 = np.array(ids1)
    delta_ids1 = np_ids1[1:]-np_ids1[:-1]
    #
    #Calculating deriv
    #
    np_ids1 = np.array(ids1)
    delta_ids1 = np_ids1[1:]-np_ids1[:-1]
    #
    #
    #
    if options.sfilename is not None:
        options.sfilename = os.path.normpath(options.sfilename)
        sbasename = os.path.basename(options.sfilename)
        sfilename = os.path.normpath(options.sfilename)
        print sfilename
        exp.append(sfilename.split('/')[-2])
        sfiledata = pd.read_csv(options.sfilename, sep=' ', names=m_cols)
        srunexec = sbasename.split('-')[3].replace('_','-').split('.')
        ids2 = sfiledata['id']
        color = 'b.'
        experiment= exp[0]+'-'+exp[1]
        #
        #Calculating deriv
        #
        np_ids2 = np.array(ids2)
        delta_ids2 = np_ids2[1:]-np_ids2[:-1]
        #
        #Calculating deriv
        #
        np_ids2 = np.array(ids2)
        delta_ids2 = np_ids2[1:]-np_ids2[:-1]
        #
        #
        #
    axis_x = []
    ts1 = filedata['ts']
    d = datetime.datetime.fromtimestamp(ts1[0])
    axis_x.append(d)
    if options.sfilename is not None:
        if len(delta_ids1) > len(delta_ids2):
            axis_len = len(delta_ids2)
            drops = len(delta_ids1) - len(delta_ids2)
            delta_ids1 = delta_ids1[:axis_len]
            print "using ids2 , dropping : %d from ids1" % (drops)
        else:
            axis_len = len(delta_ids1)
            drops = len(delta_ids2) - len(delta_ids1)
            delta_ids2 = delta_ids2[:axis_len]
            print "using ids1 , dropping : %d from ids2" % (drops)
    else:
        axis_len = len(delta_ids1)

    #
    #
    #
    axis_x = [d + datetime.timedelta(0, freq*x) for x in range(0, axis_len)]
    #print "---------stats----------"
    #print "dataset ---- %s:%s:%s ----" % (exp[0], runexec[0], runexec[1])
    #print "dataset ---- %s:%s:%s ----" % (exp[1], srunexec[0], srunexec[1])
    #print "-----------------------"
    #print """Muestra & min & max & std & mean & mediam & mode \\"""
    #print "%s & %.2f & %.2f & %.2f & %.2f & %.2f & %.2f \\" % (exp[0], delta_ids1.min(), delta_ids1.max(), delta_ids1.std(), delta_ids1.mean(), np.median(delta_ids1),0)
    #print "%s & %.2f & %.2f & %.2f & %.2f & %.2f & %.2f \\" % (exp[1], delta_ids2.min(), delta_ids2.max(), delta_ids2.std(), delta_ids2.mean(), np.median(delta_ids2),0)
    #
    #
    #
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.plot(axis_x, delta_ids1, color, label='%s '%(exp[0])+r'$\Delta id(n)$', alpha= 0.5)
    if options.sfilename is not None:
        ax.plot(axis_x, delta_ids2,'r.', label='%s '%(exp[1])+r'$\Delta id(n)$', alpha= 0.5)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
#    csfont = {'fontname':'Comic Sans MS'}
#    hfont = {'fontname':'Helvetica'}
    plt.title(r'time v.s $\Delta id(n)$')#, **hfont)#**csfont)
    plt.ylabel(r'$\Delta id(n) = id(n+1) - id(n)$')
    plt.xlabel(r'time')#,**hfont)
    plt.gcf().autofmt_xdate()
    ax.xaxis.grid(True)
    grid()
#    ax.legend(loc='center left', bbox_to_anchor=(0.75, 0.92), fancybox=False, framealpha=0.2)
    ax.legend(loc='best', fancybox=True)#, bbox_to_anchor=(0.75, 0.92), fancybox=True)#, framealpha=0.8)
    plt.savefig(experiment+'-'+str(__file__).split('.')[0]+'.png',dpi=300) # format='eps'
#    plt.show()
