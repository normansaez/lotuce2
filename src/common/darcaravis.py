import darc
import sys

class DarcAravis:
    def __init__(self, prefix):
#        try:
#            darc_instance = darc.Control(prefix)
#        except Exception, e:
#            print e
        pass

    def set(self, camera, parameter, value):
        cam = "aravisCmd%d" % camera
        cmd = '%s=%s;' % (parameter, str(value))
        darc_instance.Set(cam, cmd)
        print sys._getframe().f_code.co_name,
        print "Cam%d => %s: %s" % (camera, parameter, str(value))
    
    def get(self, camera, parameter):
        cmd = "?%d:%s" % (camera, parameter)
        darc_instance.Set('aravisGet',cmd)
        try:
            result = int(darc_instance.Get("aravisGet"))
        except ValueError, e:
            result = darc_instance.Get("aravisGet")
            print sys._getframe().f_code.co_name,
            print "Cam%d => %s: %s" % (cam, parameter, result)
            return result
        print sys._getframe().f_code.co_name,
        print "Cam%d => %s: %d" % (cam, parameter, result)
        return result
