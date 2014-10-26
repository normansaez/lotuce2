import darc
import sys
import signal
import time

class DarcAravis:
    def __init__(self, prefix):
        pass
#        signal.signal(signal.SIGALRM, self.handler)
#        signal.alarm(5)
#        self.darc_instance = darc.Control(prefix)
#        time.sleep(10)               

#    def handler(self, signum, frame):
#        raise Exception("timeout getting darc!")

    def set(self, camera, parameter, value):
        cam = "aravisCmd%d" % camera
        cmd = '%s=%s;' % (parameter, str(value))
        self.darc_instance.Set(cam, cmd)
        print sys._getframe().f_code.co_name,
        print "Cam%d => %s: %s" % (camera, parameter, str(value))
    
    def get(self, camera, parameter):
        cmd = "?%d:%s" % (camera, parameter)
        self.darc_instance.Set('aravisGet',cmd)
        try:
            result = int(self.darc_instance.Get("aravisGet"))
        except ValueError, e:
            result = self.darc_instance.Get("aravisGet")
            print sys._getframe().f_code.co_name,
            print "Cam%d => %s: %s" % (cam, parameter, result)
            return result
        print sys._getframe().f_code.co_name,
        print "Cam%d => %s: %d" % (cam, parameter, result)
        return result
