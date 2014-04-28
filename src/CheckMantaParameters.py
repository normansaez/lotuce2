import darc
from optparse import OptionParser

if __name__ == '__main__':
    parse = OptionParser()
    parse.add_option('-c', '--camera', dest='camera', type='str', help='Camera num: 0,1,2,3 etc', default="0")
    parse.add_option('-p', '--prefix', dest='prefix', type='str', help='Camera prefix: default both', default="both")
    parse.add_option('-g', '--get', dest='get', action='store_true', help='get', default=False)
    parse.add_option('-s', '--set', dest='set', action='store_true', help='get', default=True)
    parse.add_option('-v', '--value', dest='value', type=int, help='Value for set', default=None)

    (options , argv) = parse.parse_args()
    c = darc.Control(options.prefix)
    cmd = "?%s:ExposureTimeAbs" % options.camera
    c.Set("aravisGet", cmd)
    if options.get is True:
        print cmd
        print c.Get("aravisGet")
    elif options.value is not None:
        print cmd
        c.Set("aravisCmd%s"%options.camera, "ExposureTimeAbs=%d;" % options.value)
        print "Last command sent: ExposureTimeAbs=%d" % options.value
        print "Getting from camera:"
        c.Set("aravisGet", cmd)
        print c.Get("aravisGet")
        
        
