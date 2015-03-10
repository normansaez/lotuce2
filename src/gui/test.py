import darc
import sys

value = int(sys.argv[1])
d = darc.Control("all")
cam = "aravisCmd%d" % int(sys.argv[2])
parameter = 'ExposureTimeAbs'
cmd = '%s=%s;' % (parameter, str(value))
d.Set(cam, cmd)

