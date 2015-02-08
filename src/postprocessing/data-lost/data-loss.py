#!/usr/bin/python
import pandas as pd
import argparse 
import os

if __name__=="__main__":
    usage = '''
    '''
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-f', '--filename', dest='filename', type=str, help='Path to get txt source', default=None)
    parser.add_argument('-e', '--experiment', dest='experiment', type=str, help='Experiment name', default='A')
    parser.add_argument('-l', '--limit', dest='limit', type=int, help='Default limit to plot', default=None)#131100)#393300)#786600)#None)
    parser.add_argument('--hertz', dest='hertz', type=int, help='Herzt to be plotted', default=220)

    (options, unknown) = parser.parse_known_args()

    if options.filename is None:
        print "No filename to be to analised, you need give a path for the filename"
        print "Use -f /path/to/the/filename"
        sys.exit(-1)

    options.filename = os.path.normpath(options.filename)
    basename = os.path.basename(options.filename)

    m_cols = ['ts', 'id', 'cam0', 'cam1', 'cam2', 'cam3']
    data = pd.read_csv(options.filename, sep=' ', names=m_cols)
    total = len(data) - 1 
    id_i = data['id'][0]
    id_f = data['id'][total]
    id_t = (id_i + total)
#    print options.filename
#    print "id_i %d" % id_i
#    print "id_f %d" % id_f
#    print "id_t %d" % id_t
#    print "f - t: %d" % (id_f - id_t)
#    print "(f - t)/f: %f" % (((id_f - id_t)/(id_f*1.))*100.)
    print "%s: %f" % (options.experiment, ((id_f - id_t)/(id_f*1.))*100.)
