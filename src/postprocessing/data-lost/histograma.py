#!/usr/bin/python
import sys
import os
from pylab import grid#imshow,show
import matplotlib.pyplot as plt
import argparse 
import numpy as np
from matplotlib.pylab import hist, show
import pandas as pd

if __name__=="__main__":
    usage = '''
    '''
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-f', '--filename', dest='filename', type=str, help='Path to get txt source', default=None)
    parser.add_argument('-s', '--sfilename', dest='sfilename', type=str, help='Path to get txt source', default=None)
    parser.add_argument('-l', '--limit', dest='limit', type=int, help='Default limit to plot', default=None)#131100)#393300)#786600)#None)

    (options, unknown) = parser.parse_known_args()

    if options.filename is None:
        print "No filename to be to analised, you need give a path for the filename"
        print "Use -f /path/to/the/filename"
        sys.exit(-1)

    exp = []
    m_cols = ['ts', 'id', 'cam0', 'cam1', 'cam2', 'cam3']
    #
    #
    #
    options.filename = os.path.normpath(options.filename)
    basename = os.path.basename(options.filename)
    filename = os.path.normpath(options.filename)
    print filename
    color_ = 'g'
    exp.append(filename.split('/')[-2])
    experiment = exp[0]
    filedata = pd.read_csv(options.filename, sep=' ', names=m_cols)
    runexec = basename.split('-')[3].replace('_','-').split('.')
    ids1 = filedata['id']
    # 
    #
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
        color_ = 'b'
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
    cmax = delta_ids1.max() 
    if cmax < delta_ids2.max():
            cmax = delta_ids2.max()
    bins = np.linspace(0,int(cmax+1),100)#20#range(0,3000,10)#[0,10,100,200,500,100,3000]#range(0,200,10)
    hist(delta_ids1, bins, normed=True, log=True, color=color_, label=exp[0], alpha=0.5)
    if options.sfilename is not None:
        hist(delta_ids2, bins, normed=True, log=True ,color='r', alpha=0.7, label=exp[1]) #histtype='stepfilled'
    runexec = basename.split('-')[3].replace('_','-').split('.')
    srunexec = sbasename.split('-')[3].replace('_','-').split('.')
    plt.title("Histograma: %s-%s"%(exp[0],exp[1]))
    plt.xlabel(r"$id(n)=id(n+1)-id(n)$")
    plt.ylabel("log(eventos)")
#    plt.legend(loc='upper right')
    plt.legend(loc='best', fancybox=True)#, bbox_to_anchor=(0.75, 0.92), fancybox=True)#, framealpha=0.8)
    plt.savefig(experiment+'-'+str(__file__).split('.')[0]+'.png',dpi=300)
    show()
