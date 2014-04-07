#! /usr/bin/env python

import FITS
import os
import time
import sys
import ConfigParser
from optparse import OptionParser
import glob
import logging
import re

from logging import ERROR
from logging import WARNING 
from logging import INFO
from logging import DEBUG

BRAND2DARC = {"pulnix":"main","guppy":"sci","pike":"ShackHartmann","manta76":"bob","manta77":"bob2"}
LEVEL = { 1: ERROR, 2: WARNING, 3: INFO, 4:DEBUG }
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')

class Camera:
    def __init__(self, camera_name=None):
        self.camera_name = camera_name
        self.logger = logging.getLogger(__name__)
        #Read from configuration file
        configfile='camera_conf.cfg'
        self.config = ConfigParser.ConfigParser()
        self.config.read(configfile)
        try: 
            self.camera_name = self.config.get(self.camera_name, 'camera_name')
            self.npxlx = self.config.getint(self.camera_name, 'npxlx')
            self.npxly = self.config.getint(self.camera_name, 'npxly')
            self.exp_time_init = self.config.getint(self.camera_name, 'exp_time_init')
            self.exp_time_step = self.config.getint(self.camera_name, 'exp_time_step')
            self.exp_time_end = self.config.getint(self.camera_name, 'exp_time_end')
            self.brightness   = self.config.getint(self.camera_name, 'brightness') 
            self.shutter_init = self.config.getint(self.camera_name, 'shutter_init')  
            self.shutter_step = self.config.getint(self.camera_name, 'shutter_step')
            self.shutter_end  = self.config.getint(self.camera_name, 'shutter_end')
            self.timebase     = self.config.getint(self.camera_name, 'timebase') 
            self.gain         = self.config.getint(self.camera_name, 'gain')
            self.image_path = os.path.normpath(self.config.get(self.camera_name, 'image_path'))
            self.sequence_dir = None
        except Exception, e:
            self.logger.log(ERROR,e)
            self.logger.log(ERROR,"The camara passed by parameter is not configured in configuration file!")
            sys.exit(-1)
        #Take control of the camera
        try:
            import darc
            self.darc_instance = darc.Control(BRAND2DARC[self.camera_name])
            npxlx    = self.darc_instance.Get("npxlx")[0]
            npxly    = self.darc_instance.Get("npxly")[0]
        except Exception, e:
            self.logger.log(ERROR,e)
            self.logger.log(ERROR,"Error trying to get Camera instance from Darc ... is Darc running?")
            sys.exit(-1)
        #Cross check: read config file, read darc configuration before do something
        if not (npxlx == self.npxlx):
            self.logger.log(ERROR,"Problem in definition of PIXEL X %s: darc says: %d, configuration file says: %d" % (self.camera_name, self.npxlx, npxlx))
            self.logger.log(ERROR,"Fix one of them before continue!")
            sys.exit(-1)

        if not (npxly == self.npxly):
            self.logger.log(ERROR,"Problem in definition of PIXEL Y %s: darc says: %d, configuration file says: %d" % (self.camera_name, self.npxly, npxly))
            self.logger.log(ERROR,"Fix one of them before continue!")
            sys.exit(-1)

    def take_images(self, sec_dir, img_prefix, img_number):
        fitsname = sec_dir+"/" + img_prefix + str(img_number).zfill(3) + '.fits'
        self.logger.log(INFO,"Image name: " +fitsname)
        bg=self.darc_instance.SumData('rtcPxlBuf',1,'f')[0]/1. #acquisition from the camera
        data = bg.reshape(self.npxly, self.npxlx) #reorganizing lines and columns
        FITS.Write(data, fitsname, writeMode='a') #writing fits file

    def set_shutter(self, shutter):
        if self.camera_name is "pulnix":
            self.logger.log(INFO, "Shutter Register Value: %d " % shutter)
            self.darc_instance.Set("fwShutter",shutter)
        elif self.camera_name is "manta76":
            self.logger.log(INFO, "Shutter Register Value: %d " % shutter)
            self.darc_instance.Set("aravisCmd0",'ProgFrameTimeEnable=true;ProgFrameTimeAbs=50000;ExposureTimeAbs=%d;'%shutter)

        elif self.camera_name is "manta77":
            self.logger.log(INFO, "Shutter Register Value: %d " % shutter)
            self.darc_instance.Set("aravisCmd1",'ProgFrameTimeEnable=true;ProgFrameTimeAbs=50000;ExposureTimeAbs=%d;'%shutter)

        else:
            self.logger.log(INFO, "Shutter Register Value: %d " % shutter)
            self.logger.log(INFO, "Shutter*TimeBase + Offset= %d*%d [ms]+ %d [ms] = %.3f [ms]" % (shutter,self.timebase,71,shutter*self.timebase + 71.0))
            self.darc_instance.Set("fwShutter",shutter)
        if shutter >= self.shutter_end:
            self.logger.log(WARNING, "Shutter reach maximum limit : %d" % self.shutter_end)
            shutter = self.shutter_end
            self.log.log(WARNING, "Shutter set to : %d" % self.shutter_end)

    def set_gain(self, gain):
        if self.camera_name is "pulnix":
            self.logger.log(INFO, "Gain: %d " % gain)
            self.darc_instance.Set("fwGain",gain)
        else:
            self.logger.log(INFO, "Gain: %d " % gain)
            self.darc_instance.Set("fwGain", gain)

    def set_brightness(self, brightness):
        if self.camera_name is "pulnix":
            self.logger.log(INFO, "Brightness: %d " % brightness)
            self.darc_instance.Set("fwBrightness",brightness)
        else:
            self.logger.log(INFO, "Brightness: %d " % brightness)
            self.darc_instance.Set("fwBrightness", brightness)

    def make_sequence_dir(self):
        # creates initial path
        if not os.path.exists(self.image_path):
            os.mkdir(self.image_path)
        #current sequence:
        current  =  self.camera_name+ "_" + str(time.strftime("%Y_%m_%d", time.gmtime()))
        #very first day:
        dir_name = current+'.0'
        if not os.path.exists(os.path.normpath(self.image_path+"/"+dir_name)):
            sequence_dir = os.path.normpath(self.image_path+"/"+dir_name)
            self.logger.log(LEVEL[3],'Secuence Directory Name: %s'% (sequence_dir))
            os.mkdir(sequence_dir)
            return sequence_dir
        #Get dir and sort by date:    
        current_dir = glob.glob(self.image_path+'/*')
        current_dir.sort(key=lambda x: os.path.getmtime(x)) 
        
        #Get the last one:
        last = current_dir[-1]
        
        #Check if is the first sequence:
        if last.split('/')[-1].split('.')[0] == current:
            adquisition_number = int(last.split('/')[-1].split('.')[1]) + 1
            dir_name = current+'.'+ str(adquisition_number)
        else:
            dir_name = current+'.0'
        sequence_dir = os.path.normpath(self.image_path+"/"+dir_name)
        self.logger.log(LEVEL[3],'Secuence Directory Name: %s'% (sequence_dir))
        os.mkdir(sequence_dir)
        return sequence_dir

    def get_status(self):
        data,ftime,fno=self.darc_instance.GetStream(BRAND2DARC[self.camera_name]+"rtcStatusBuf")
        self.logger.log(DEBUG, "Frame time: %s " % re.search('[0-9]*.[0-9]*Hz',data.tostring()).group(0))
        self.logger.log(DEBUG,data.tostring())
        #return data

    def acquiring_images(self):
        shutter = self.shutter_init
        for sec in range(1, options.sequences+1):
            self.sequence_dir = self.make_sequence_dir()
            self.logger.log(DEBUG,"sec:%d stored in %s" % (sec, self.sequence_dir))
            t0 = time.clock() #initialize time
            self.set_shutter(shutter)
#            self.set_gain(self.gain)
#            self.set_brightness(self.brightness)
            for n_img in range(1, options.images+1):
                self.logger.log(DEBUG,"sec:%d -> img num: %d" % (sec, n_img))
                self.take_images(self.sequence_dir, self.camera_name, n_img)
                #self.get_status()
            msg = 'Frame rate=' + str(options.images/(time.clock() - t0)) + ' fps'
            self.logger.log(INFO, msg)
            shutter += self.shutter_step


if __name__ == '__main__':
    usage_message = """
    CameraAdquisition.py --<OPTIONS>

    Cameras available: pike, guppy and pulnix
    Example:
    python CameraAdquisition.py --camera pike --images 5 --sequences 10

    Therefore, it will takes 10 sequences with 5 images each one: 
    10*5 = 50 images
    10 directories
    5 images per directory


    The directory is configured in camera_conf.cfg file, one per camera:

    Inside that directory, each secuence will create a new directory:
    Example:
    
    pulnix_2013_11_29.27
    ^        ^        ^  
    |        |        `--
    `-camera |           |
             `-day date  |
                         `- secuence number of that day
    """
    #Options in the script:
    cams_available = ["pike","guppy","pulnix","manta76","manta77"]

    parser = OptionParser(usage=usage_message)
    parser.add_option('-c', '--camera', dest='camera', default=None, help='Set a camera to be used: %s' % ', '.join(map(str,cams_available)))
    parser.add_option('-i', '--images', dest='images', default=1, type="int", help='Set a number of images per sequence. Default = 1')
    parser.add_option('-s', '--sequences', dest='sequences', default=1, type="int", help='Set a number of sequence. Default = 1')
    parser.add_option("-v", action="count", dest="verbosity", default=3, help="Be verbose and display detailed information, -vv very verbose, -vvv even more verbose")

    (options, args) = parser.parse_args()
    #Some restriction to prevent errors:
    if options.camera is None:
        print "It is mandatory use --camera , to set a camera.\nFor help use: %s -h" % __file__
        sys.exit(-1)
    if not options.camera in ["pike","guppy","pulnix","manta76","manta77"]:
        print "Use one of these cameras: %s\nFor help use: %s -h" % (', '.join(map(str,cams_available)), __file__)
        sys.exit(-1)

    #If all is OK, then get a camera:
    camera = Camera(options.camera)
    #Set log LEVEL
    level = LEVEL.get(options.verbosity, INFO)
    camera.logger.setLevel(level)
    fh = logging.FileHandler(camera.camera_name+ "_" + str(time.strftime("%Y_%m_%d", time.gmtime()))+'.log')
    fh.setLevel(level)
    fh_format = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')
    fh.setFormatter(fh_format)
    camera.logger.addHandler(fh)
    ##
    camera.logger.log(INFO, "Parameters for these set of imagess:")
    camera.logger.log(INFO, "Camera:                        %s" % camera.camera_name)
    camera.logger.log(INFO, "X pixel:                       %s" % camera.npxlx)
    camera.logger.log(INFO, "Y pixel:                       %s" % camera.npxly)
    camera.logger.log(INFO, "Exposure time min:             %s" % camera.exp_time_init)
    camera.logger.log(INFO, "Exposure time increase step:   %s" % camera.exp_time_step)
    camera.logger.log(INFO, "Exposure time max:             %s" % camera.exp_time_end)
    camera.logger.log(INFO, "Path to be store images:       %s" % camera.image_path)
    #Routine to get a full set of images:
    camera.acquiring_images()
    #Some data from darc
    camera.logger.log(DEBUG,"----------------")
    camera.logger.log(DEBUG,"Parameters controllables using DARC")
    camera.logger.log(DEBUG,'%s' % ', '.join(map(str, camera.darc_instance.GetLabels())))
