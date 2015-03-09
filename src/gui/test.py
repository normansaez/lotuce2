import darc
value = 90000
d = darc.Control("all")
cam = "aravisCmd%d" % 3
parameter = 'ExposureTimeAbs'
cmd = '%s=%s;' % (parameter, str(value))
d.Set(cam, cmd)

