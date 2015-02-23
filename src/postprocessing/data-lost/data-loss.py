#!/usr/bin/python
import pandas as pd
import argparse 
import os
import pandas as pd
import numpy as np
import glob
import multiprocessing as mp
import sys

def data_stats(filename, stat):
    exp = []
    freq = 1./220.
    m_cols = ['ts', 'id', 'cam0', 'cam1', 'cam2', 'cam3']
    filename = os.path.normpath(filename)
    basename = os.path.basename(filename)
    runexec = basename.split('-')[3].replace('_','-').split('.')
    exp.append(filename.split('/')[-2])

    filedata = pd.read_csv(filename, sep=' ', names=m_cols)
    ids1 = filedata['id']
    np_ids1 = np.array(ids1)
    delta_ids1 = np_ids1[1:]-np_ids1[:-1]

    total = len(filedata) - 1 
    id_i = filedata['id'][0]
    id_f = filedata['id'][total]
    id_t = (id_i + total)
    lost = ((id_f - id_t)/(id_f*1.))*100.
    print "%s - %s:%s: %f  %% data lost" % (exp[0], runexec[0], runexec[1], lost)
#    print "---------stats----------"
#    print "dataset ---- %s:%s:%s ----" % (exp[0], runexec[0], runexec[1])
#    print """Muestra & min & max & std & mean & median & mode \\"""
    results = "%s & %d & %d & %.2f & %.2f & %.2f & %.2f & %f \\%% %s:%s \\\\" % \
                (exp[0], delta_ids1.min(), delta_ids1.max(), delta_ids1.std(), delta_ids1.mean(), np.median(delta_ids1), mode(delta_ids1)[0], lost, runexec[0], runexec[1])
#    print "-----------------------"
    stat.put(results)
    
    

def wrapper(func, args, res):
        res.append(func(*args))
 
def mode(a, axis=0):
    scores = np.unique(np.ravel(a))       # get ALL unique values
    testshape = list(a.shape)
    testshape[axis] = 1
    oldmostfreq = np.zeros(testshape)
    oldcounts = np.zeros(testshape)

    for score in scores:
        template = (a == score)
        counts = np.expand_dims(np.sum(template, axis),axis)
        mostfrequent = np.where(counts > oldcounts, score, oldmostfreq)
        oldcounts = np.maximum(counts, oldcounts)
        oldmostfreq = mostfrequent

    return mostfrequent, oldcounts

if __name__=="__main__":
    usage = '''
    '''
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-d', '--dirname', dest='dirname', type=str, help='Path dir to get txt source', default=None)

    (options, unknown) = parser.parse_known_args()

    if options.dirname is None:
        print "No filename to be to analised, you need give a path for the filename"
        print "Use -f /path/to/the/filename"
        sys.exit(-1)

    options.dirname = os.path.normpath(options.dirname)
    dirlist = glob.glob(options.dirname+'/*')
    processes = []
    stat = mp.Queue()
    for dirname in dirlist:
        if os.path.isdir(dirname) is True:
            filenames = glob.glob(dirname+'/*')
            for filename in filenames:
                processes.append(mp.Process(target=data_stats, args=(filename, stat)))

    for p in processes:
        p.start()

    for p in processes:
        p.join()
    
    print """
\\begin{tabular}{lllllllll}
\\toprule
Muestra & min & max & std & promedio & mediana & moda & perdidas \% & fecha:ejec \\\\
\\midrule 
    """
    for p in processes:
        print stat.get()
    print """
\\bottomrule
\\end{tabular}
"""
#    m_cols = ['ts', 'id', 'cam0', 'cam1', 'cam2', 'cam3']
#    data = pd.read_csv(options.filename, sep=' ', names=m_cols)
#    total = len(data) - 1 
#    id_i = data['id'][0]
#    id_f = data['id'][total]
#    id_t = (id_i + total)
#    print "%s: %f" % (options.experiment, ((id_f - id_t)/(id_f*1.))*100.)
