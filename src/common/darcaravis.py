import darc
import sys
import signal
import time
import glob

class DarcAravis:
    def __init__(self, prefix):

        if self.is_darc_running(prefix):
            self.darc_instance = darc.Control(prefix)
        else:
            raise Exception("DARC instance is not running with prefix: %s" % prefix)

    def is_darc_running(self, prefix):
        darc_lists = glob.glob('/dev/shm/*rtcParam1')
        for ins in darc_lists:
            if ins.split('rtcParam1')[0] != "":
                return True
        return False
            
    def get_darc_prefix(self, prefix):
        darc_lists = glob.glob('/dev/shm/*rtcParam1')
        for ins in darc_lists:
            if ins.split('rtcParam1')[0] != "":
                return ins.split('rtcParam1')[0]
        return None
            
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
            print "Cam%d => %s: %s" % (camera, parameter, result)
            return result
        print sys._getframe().f_code.co_name,
        print "Cam%d => %s: %d" % (camera, parameter, result)
        return result
