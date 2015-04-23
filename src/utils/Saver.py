#darc, the Durham Adaptive optics Real-time Controller.
#Copyright (C) 2010 Alastair Basden.

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as
#published by the Free Software Foundation, either version 3 of the
#License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.

#You should have received a copy of the GNU Affero General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
import numpy
#import mmap
import FITS
import os
import sys
import traceback
import time
import string
#from skimage.measure import regionprops
#from skimage.measure import label
from math import floor
import profilesaver
import pyaio

def bit_check(x, y, img, threshold, width):
    intensity = img[y-width:y+width,x-width:x+width].mean()
    if intensity >= threshold:
        return 1
    return 0

class Saver:
    """Class to implement saving of RTC streams"""
    def __init__(self,name,mode="a"):
        self.name=name
        self.mode=mode
        if name[-5:]==".fits":
            self.asfits=1
        else:
            self.asfits=0
        self.initialised=0
        self.finalise=0
        self.info=numpy.zeros((8,),numpy.int32)
        self.cov_counter = 0
        self.cent_counter = 0
        self.fitsname = None
        self.x0 = numpy.array([])
        self.x1 = numpy.array([])
        self.x2 = numpy.array([])
        self.x3 = numpy.array([])
        self.y0 = numpy.array([])
        self.y1 = numpy.array([])
        self.y2 = numpy.array([])
        self.y3 = numpy.array([])

    def write(self,data,ftime,fno):
#        def aio_callback(rt, errno):
#            '''
#            call back for Async write
#            '''
#            if rt > 0:
#                pass
#                #print "Wrote %d bytes" % rt
#            else:
#                print "Got error: %d" % errno

        # local vars ?
        pxly = 200
        pxlx = 200

#        threshold = 2000

        #
        # camera coordinates according windows size.
        #
        xi_cam0 = 0*pxly
        xf_cam0 = 1*pxly
        yi_cam0 = 0*pxlx
        yf_cam0 = 1*pxlx
    
        xi_cam1 = 1*pxly
        xf_cam1 = 2*pxly
        yi_cam1 = 0*pxlx
        yf_cam1 = 1*pxlx
    
        xi_cam2 = 2*pxly
        xf_cam2 = 3*pxly
        yi_cam2 = 0*pxlx
        yf_cam2 = 1*pxlx
    
        xi_cam3 = 3*pxly
        xf_cam3 = 4*pxly
        yi_cam3 = 0*pxlx
        yf_cam3 = 1*pxlx
    
        #        
        # Padding in pixels to make closed shapes and get a correct centroid
        #
        #padding = 5#7

        #
        # area to search intensity (mean) taking account centroid
        #
#        width = 3#5

        #
        #Getting centroid: Now is hardcoded to save time
        #
        #y0_cam0, x0_cam0 = get_centroid(mask_b0_cam0)
#        x0_cam0 = 191
#        y0_cam0 = 109
#        x1_cam0 = 144
#        y1_cam0 = 93
#        x2_cam0 = 73
#        y2_cam0 = 89
#        x3_cam0 = 6
#        y3_cam0 = 116
#        #y0_cam1, x0_cam1 = get_centroid(mask_b0_cam1)
#        x0_cam1 = 8
#        y0_cam1 = 104
#        x1_cam1 = 52
#        y1_cam1 = 88
#        x2_cam1 = 121
#        y2_cam1 = 85
#        x3_cam1 = 194
#        y3_cam1 = 108 
#        #y0_cam2, x0_cam2 = get_centroid(mask_b0_cam2)
#        x0_cam2 = 192
#        y0_cam2 = 110
#        x1_cam2 = 147
#        y1_cam2 = 101
#        x2_cam2 = 75
#        y2_cam2 = 99
#        x3_cam2 = 6
#        y3_cam2 = 120
#        #y0_cam3, x0_cam3 = get_centroid(mask_b0_cam3)
#        x0_cam3 = 6
#        y0_cam3 = 109
#        x1_cam3 = 52
#        y1_cam3 = 101
#        x2_cam3 = 123
#        y2_cam3 = 98
#        x3_cam3 = 191
#        y3_cam3 = 119 

        #
        # Getting string names
        #
        fitsname = self.name.split('.fits')[0]+'_profile_'+str(fno)+'.fits'
#        fitsname_c0 = self.name.split('.fits')[0]+'_cent_cam0_'+str(fno)+'.fits'
#        fitsname_c1 = self.name.split('.fits')[0]+'_cent_cam1_'+str(fno)+'.fits'
#        fitsname_c2 = self.name.split('.fits')[0]+'_cent_cam2_'+str(fno)+'.fits'
#        fitsname_c3 = self.name.split('.fits')[0]+'_cent_cam3_'+str(fno)+'.fits'

        #
        # Reshape data to be analized
        #
        mydata = None
        try:
            mydata = data.reshape((4*pxly,pxlx))
        except:
            if self.cent_counter == 0:
                self.fitsname = self.name.split('.fits')[0]+'_cent_'+str(fno)+'.txt'
                self.cent_counter = 1
            else:
                if self.cent_counter <= 300:
                    self.cent_counter += 1
                else:
                    self.cent_counter = 0    
            print self.cent_counter
            text_file = open(self.fitsname,'a') # normal open file
    
            self.x0 = numpy.append(self.x0,data[0])
            self.y0 = numpy.append(self.x0,data[1])

            self.x1 = numpy.append(self.x1,data[2])
            self.y1 = numpy.append(self.x1,data[3])

            self.x2 = numpy.append(self.x2,data[4])
            self.y2 = numpy.append(self.x2,data[5])

            self.x3 = numpy.append(self.x3,data[6])
            self.y3 = numpy.append(self.x3,data[7])

            text_file.write('%f %f %f %f %f %f %f %f %f\n'% (ftime, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]))
            text_file.close()
            if self.cov_counter == 100:
#                print self.cov_counter
                fitsname_c = self.name.split('.fits')[0]+'_covs.txt'
                text_file_c = open(fitsname_c,'a') # normal open file
                x0x1 = numpy.cov(self.x0, self.x1)[0][1] 
                x0x2 = numpy.cov(self.x0, self.x2)[0][1]
                x0x3 = numpy.cov(self.x0, self.x3)[0][1]
                x1x2 = numpy.cov(self.x1, self.x2)[0][1]
                x1x3 = numpy.cov(self.x1, self.x3)[0][1]
                x2x3 = numpy.cov(self.x2, self.x3)[0][1]
                      
                y0y1 = numpy.cov(self.y0, self.y1)[0][1] 
                y0y2 = numpy.cov(self.y0, self.y2)[0][1]
                y0y3 = numpy.cov(self.y0, self.y3)[0][1]
                y1y2 = numpy.cov(self.y1, self.y2)[0][1]
                y1y3 = numpy.cov(self.y1, self.y3)[0][1]
                y2y3 = numpy.cov(self.y2, self.y3)[0][1]

                self.x0 = numpy.array([])
                self.x1 = numpy.array([])
                self.x2 = numpy.array([])
                self.x3 = numpy.array([])
                self.y0 = numpy.array([])
                self.y1 = numpy.array([])
                self.y2 = numpy.array([])
                self.y3 = numpy.array([])
             
                text_file_c.write('%f %f %f %f %f %f %f %f %f %f %f %f %f\n'% (ftime, x0x1,x0x2,x0x3,x1x2,x1x3,x2x3,y0y1,y0y2,y0y3,y1y2,y1y3,y2y3))
                text_file_c.close()
                self.cov_counter = 0
            self.cov_counter += 1 
            return        
        #
        # Checking bits for cameras, and getting patterns
        #
        cam_cam0 = mydata[xi_cam0:xf_cam0,yi_cam0:yf_cam0]
#        b0_cam0 = bit_check(x0_cam0, y0_cam0, cam_cam0, threshold, width)
#        b1_cam0 = bit_check(x1_cam0, y1_cam0, cam_cam0, threshold, width)
#        b2_cam0 = bit_check(x2_cam0, y2_cam0, cam_cam0, threshold, width)
#        b3_cam0 = bit_check(x3_cam0, y3_cam0, cam_cam0, threshold, width)
#        num_cam0 = '0b'+str(b3_cam0)+str(b2_cam0)+str(b1_cam0)+str(b0_cam0)
#        num_cam0 = eval(num_cam0)
        #
        cam_cam1 = mydata[xi_cam1:xf_cam1,yi_cam1:yf_cam1]
#        b0_cam1 = bit_check(x0_cam1, y0_cam1, cam_cam1, threshold, width)
#        b1_cam1 = bit_check(x1_cam1, y1_cam1, cam_cam1, threshold, width)
#        b2_cam1 = bit_check(x2_cam1, y2_cam1, cam_cam1, threshold, width)
#        b3_cam1 = bit_check(x3_cam1, y3_cam1, cam_cam1, threshold, width)
#        num_cam1 = '0b'+str(b3_cam1)+str(b2_cam1)+str(b1_cam1)+str(b0_cam1)
#        num_cam1 = eval(num_cam1)
        #
        cam_cam2 = mydata[xi_cam2:xf_cam2,yi_cam2:yf_cam2]
#        b0_cam2 = bit_check(x0_cam2, y0_cam2, cam_cam2, threshold, width)
#        b1_cam2 = bit_check(x1_cam2, y1_cam2, cam_cam2, threshold, width)
#        b2_cam2 = bit_check(x2_cam2, y2_cam2, cam_cam2, threshold, width)
#        b3_cam2 = bit_check(x3_cam2, y3_cam2, cam_cam2, threshold, width)
#        num_cam2 = '0b'+str(b3_cam2)+str(b2_cam2)+str(b1_cam2)+str(b0_cam2)
#        num_cam2 = eval(num_cam2)
        #
        cam_cam3 = mydata[xi_cam3:xf_cam3,yi_cam3:yf_cam3]
#        b0_cam3 = bit_check(x0_cam3, y0_cam3, cam_cam3, threshold, width)
#        b1_cam3 = bit_check(x1_cam3, y1_cam3, cam_cam3, threshold, width)
#        b2_cam3 = bit_check(x2_cam3, y2_cam3, cam_cam3, threshold, width)
#        b3_cam3 = bit_check(x3_cam3, y3_cam3, cam_cam3, threshold, width)
#        num_cam3 = '0b'+str(b3_cam3)+str(b2_cam3)+str(b1_cam3)+str(b0_cam3)
#        num_cam3 = eval(num_cam3)

        #XXX
        # Writing data: timestamp fno(id) pattern_cam0 pattern_cam1 pattern_cam2 pattern_cam3
        #
        #pyaio.aio_write(fd,b'%f %d %d %d %d %d\n'%(ftime, fno, num_cam0, num_cam1, num_cam2, num_cam3), 200, aio_callback)
        # 
        #Open file wich will save: timestamp fno(id) pattern_cam0 pattern_cam1 pattern_cam2 pattern_cam3
        #
#        res = self.name.split('.fits')[0]+'_'+'lotuce2-run-results.txt'
#        resname = 'lotuce2-run-results-'+res.split('/')[-2]+'.txt'
#        text_file = open(resname,'a') # normal open file
#        #fd = os.open(resname, os.O_WRONLY| os.O_CREAT | os.O_TRUNC | os.O_NONBLOCK)
##        text_file.write('%f %d %d %d %d %d\n'%(ftime, fno, num_cam0, num_cam1, num_cam2, num_cam3))
#        text_file.close()

        #
        # Profiles: reducing data before store it.
        # 
        c0_x = cam_cam0.sum(0)
        c0_y = cam_cam0.sum(1)
        col_cam0 = numpy.append(c0_x,c0_y,0)

        c1_x = cam_cam1.sum(0)
        c1_y = cam_cam1.sum(1)
        col_cam1 = numpy.append(c1_x,c1_y,0)

        c2_x = cam_cam2.sum(0)
        c2_y = cam_cam2.sum(1)
        col_cam2 = numpy.append(c2_x,c2_y,0)

        c3_x = cam_cam2.sum(0)
        c3_y = cam_cam2.sum(1)
        col_cam3 = numpy.append(c3_x,c3_y,0)

        #
        # Concatenate all profiles in one array
        #
        myprofile = numpy.append(col_cam0, col_cam1,0)
        myprofile = numpy.append(myprofile, col_cam2,0)
        myprofile = numpy.append(myprofile, col_cam3,0)

        #XXX
        # Saving profiles using async write
        #
        #fd1 = os.open(fitsname, os.O_WRONLY| os.O_CREAT | os.O_TRUNC | os.O_NONBLOCK)
        #pyaio.aio_write(fd1, b'%s'%str(myprofile), len(myprofile), aio_callback)
        #FITS.Write(myprofile, fitsname, writeMode='w')
        profilesaver.saver(myprofile, fitsname)

        #XXX
        # Centroids: Calculating before store them
        # Classic way to calculate.
        #
#        cent = numpy.zeros(8)
#        totalmass = float(cam_cam0.sum())
#        Xgrid,Ygrid = numpy.meshgrid(numpy.arange(cam_cam0.shape[1]),numpy.arange(cam_cam0.shape[0]))
#        cent[1] = numpy.sum(Ygrid*cam_cam0)/totalmass
#        cent[0] = numpy.sum(Xgrid*cam_cam0)/totalmass
#        #
#        totalmass = float(cam_cam1.sum())
#        Xgrid,Ygrid = numpy.meshgrid(numpy.arange(cam_cam1.shape[1]),numpy.arange(cam_cam1.shape[0]))
#        cent[2] = numpy.sum(Ygrid*cam_cam1)/totalmass
#        cent[3] = numpy.sum(Xgrid*cam_cam1)/totalmass
#        #
#        totalmass = float(cam_cam2.sum())
#        Xgrid,Ygrid = numpy.meshgrid(numpy.arange(cam_cam2.shape[1]),numpy.arange(cam_cam2.shape[0]))
#        cent[4] = numpy.sum(Ygrid*cam_cam2)/totalmass
#        cent[5] = numpy.sum(Xgrid*cam_cam2)/totalmass
#        #
#        totalmass = float(cam_cam3.sum())
#        Xgrid,Ygrid = numpy.meshgrid(numpy.arange(cam_cam3.shape[1]),numpy.arange(cam_cam3.shape[0]))
#        cent[6] = numpy.sum(Ygrid*cam_cam3)/totalmass
#        cent[7] = numpy.sum(Xgrid*cam_cam3)/totalmass
#        #fd_c1 = os.open(fitsname_c1, os.O_WRONLY| os.O_CREAT | os.O_TRUNC)
#        #pyaio.aio_write(fd_c1, b"%s"%str(cent), len(myprofile), aio_callback)
#        #FITS.Write(cent, fitsname_c0, writeMode='w')
#        profilesaver.saver(cent, fitsname_c0)

        return
        #TODO: End of the fix, should be removed
        if self.asfits:
            if self.initialised==0:#Initialise the header
                self.finalise=1
                self.initialised=1
                self.hdustart=self.fd.tell()
                shape=[1]+list(data.shape)
                FITS.WriteHeader(self.fd,shape,data.dtype.char,firstHeader=(self.hdustart==0))
                self.fdfno=open(self.name+"fno","w+")
                self.fdtme=open(self.name+"tme","w+")
                FITS.WriteHeader(self.fdfno,[1,],"i",firstHeader=0)
                FITS.WriteHeader(self.fdtme,[1,],"d",firstHeader=0)
                self.dtype=data.dtype.char
                self.shape=data.shape
                self.datasize=data.size*data.itemsize
            if self.shape!=data.shape or self.dtype!=data.dtype.char:
                print self.fd
                #print self.shape
                #print data.shape
                #Have to start a new fits HDU
                self.fitsFinalise()#So, finalise existing
                self.finalise=1
                self.fd.seek(0,2)#move to end of file.
                self.hdustart=self.fd.tell()
                shape=[1]+list(data.shape)
                FITS.WriteHeader(self.fd,shape,data.dtype.char,firstHeader=0)
                self.fdfno=open(self.name+"fno","w+")
                self.fdtme=open(self.name+"tme","w+")
                FITS.WriteHeader(self.fdfno,[1,],"i",firstHeader=0)
                FITS.WriteHeader(self.fdtme,[1,],"d",firstHeader=0)
                self.dtype=data.dtype.char
                self.shape=data.shape
            #and now write the data.
            self.fd.write(data.byteswap().data)
            print self.fd
            self.fdfno.write(numpy.array([fno]).astype(numpy.int32).byteswap().data)
            self.fdtme.write(numpy.array([ftime]).astype(numpy.float64).byteswap().data)
                
        else:
            self.info[0]=(self.info.size-1)*self.info.itemsize+data.size*data.itemsize#number of bytes to follow (excluding these 4)
            self.info[1]=fno
            self.info[2:4].view(numpy.float64)[0]=ftime
            self.info.view("c")[16]=data.dtype.char
            self.fd.write(self.info.data)
            self.fd.write(data.data)
    def writeRaw(self,data):#data should be of the correct format... ie same as that written by self.write()
        if self.asfits:
            if type(data)==type(""):
                data=numpy.fromstring(data,dtype="b")
            data.data.view("b")
            d=data.view("b")[32:].astype(data[16])
            fno=int(data[4:8].view(numpy.int32)[0])
            ftime=float(data[8:16].view(numpy.float64)[0])
            d=d.astype(data[16])
            self.write(d,ftime,fno)
        else:
            if type(data)==type(""):
                self.fd.write(data)
            else:
                self.fd.write(data.data)

    def fitsFinalise(self):
        """finalise a saved on fly fits file..."""
        if self.asfits and self.finalise:
            self.finalise=0
            self.fd.seek(0,2)
            pos=self.fd.tell()
            self.fd.seek(self.hdustart)
            nbytes=pos-2880-self.hdustart
            n=nbytes/self.datasize
            FITS.updateLastAxis(None,n,self.fd)
            self.fd.seek(0,2)#go to end
            extra=2880-pos%2880
            if extra<2880:
                self.fd.write(" "*extra)
            #Now add the frame numbers and timestamps.
            self.fdfno.seek(0)
            FITS.updateLastAxis(None,n,self.fdfno)
            self.fdfno.seek(0)
            self.fd.write(self.fdfno.read())
            pos=self.fd.tell()
            extra=2880-pos%2880
            if extra<2880:
                self.fd.write(" "*extra)
            self.fdtme.seek(0)
            FITS.updateLastAxis(None,n,self.fdtme)
            self.fdtme.seek(0)
            self.fd.write(self.fdtme.read())
            pos=self.fd.tell()
            extra=2880-pos%2880
            if extra<2880:
                self.fd.write(" "*extra)
            self.fdtme.close()
            self.fdfno.close()
            try:
                os.unlink(self.name+"fno")
                os.unlink(self.name+"tme")
            except:
                pass

    def close(self):
        if self.asfits:
            self.fitsFinalise()
#        self.fd.close()
    def read(self,readdata=1,ffrom=None,fto=None,tfrom=None,tto=None):
        data=[]
        frame=None
        while 1:
            hdr=self.fd.read(self.info.size*self.info.itemsize)
            if hdr=="":#end of file...
                return data
            elif len(hdr)<self.info.size*self.info.itemsize:
                print "Didn't read all of header"
                return data
            info=numpy.fromstring(hdr,numpy.int32)
            fno=int(info[1])
            ftime=float(info[2:4].view("d"))
            databytes=info[0]-(self.info.size-1)*self.info.itemsize
            fok=tok=0
            #print fno,ffrom,fto
            if (ffrom==None or fno>=ffrom) and (fto==None or fno<=fto):
                #print fno
                fok=1
            if (tfrom==None or ftime>=tfrom) and (tto==None or ftime<=tto):
                tok=1
            if readdata==1 and fok==1 and tok==1:
                frame=self.fd.read(databytes)
                if len(frame)!=databytes:
                    print "Didn't read all of frame"
                    return data
                frame=numpy.fromstring(frame,chr(info[4]))
                data.append((fno,ftime,frame))
            else:
                #skip the data.
                self.fd.seek(databytes-1,1)
                if self.fd.read(1)=="":#read the last byte to check we've not reached end of file.
                    print "Didn't read all of frame"
                    return data

                frame=None
    def tofits(self,fname,ffrom=None,fto=None,tfrom=None,tto=None):
        curshape=None
        curdtype=None
        fheader=None
        nentries=0
        tlist=[]
        flist=[]
        ffits=open(fname,"w")
        firstHeader=1
        while 1:
            hdr=self.fd.read(self.info.size*self.info.itemsize)
            if hdr=="":
                break
            elif len(hdr)<self.info.size*self.info.itemsize:
                print "Didn't read all of header"
                break
            info=numpy.fromstring(hdr,numpy.int32)
            fno=int(info[1])
            ftime=float(info[2:4].view("d"))
            databytes=info[0]-(self.info.size-1)*self.info.itemsize
            fok=tok=0
            if (ffrom==None or fno>=ffrom) and (fto==None or fno<=fto):
                #print fno
                fok=1
            if (tfrom==None or ftime>=tfrom) and (tto==None or ftime<=tto):
                tok=1
            if fok==1 and tok==1:
                frame=self.fd.read(databytes)
                if len(frame)!=databytes:
                    print "Didn't read all of frame"
                    break
                frame=numpy.fromstring(frame,chr(info[4])).byteswap()
                #can it be put into the existing HDU?  If not, finalise current, and start a new one.
                if curshape!=databytes or curdtype!=chr(info[4]):
                    #end the current HDU
                    FITS.End(ffits)
                    #Update FITS header
                    if fheader!=None:
                        FITS.updateLastAxis(None,nentries,fheader)
                        del(fheader)
                        #fheader.close()
                        fheader=None
                    #now write the frame number and time.
                    ffits.close()
                    if firstHeader==0:
                        FITS.Write(numpy.array(flist).astype("i"),fname,writeMode="a")
                        FITS.Write(numpy.array(tlist),fname,writeMode="a")
                    ffits=open(fname,"a+")
                    FITS.WriteHeader(ffits,[1,databytes/numpy.zeros((1,),chr(info[4])).itemsize],chr(info[4]),firstHeader=firstHeader)
                    ffits.flush()
                    firstHeader=0
                    fheader=numpy.memmap(fname,dtype="c",mode="r+",offset=ffits.tell()-2880)
                    flist=[]
                    tlist=[]
                    nentries=0
                    curshape=databytes
                    curdtype=chr(info[4])
                #now write the data
                ffits.write(frame)
                nentries+=1
                flist.append(fno)
                tlist.append(ftime)
            else:
                #skip the data
                self.fd.seek(databytes-1,1)
                if self.rd.read(1)=="":
                    print "Didn't read all of the frame"
                    break
        #now finalise the file.
        FITS.End(ffits)
        if fheader!=None:
            FITS.updateLastAxis(None,nentries,fheader)
            #fheader.close()
            del(fheader)
            fheader=None
        #now write the frame number and time.
        ffits.close()
        FITS.Write(numpy.array(flist).astype("i"),fname,writeMode="a")
        FITS.Write(numpy.array(tlist),fname,writeMode="a")

class Extractor:
    def __init__(self,name):
        """For extracting data from a large FITS file."""
        self.bpdict={8:numpy.uint8,
                     16:numpy.int16,
                     32:numpy.int32,
                     -32:numpy.float32,
                     -64:numpy.float64,
                     -16:numpy.uint16
                     }

        self.name=name
        self.fd=open(self.name,"r")
        self.HDUoffset=0
        self.hdr=FITS.ReadHeader(self.fd)["parsed"]
        self.nd=int(self.hdr["NAXIS"])
        dims=[]
        for i in range(self.nd):
            dims.append(int(self.hdr["NAXIS%d"%(i+1)]))
        dims.reverse()
        self.dims=numpy.array(dims)
        self.bitpix=int(self.hdr["BITPIX"])
        self.dataOffset=self.fd.tell()
        dsize=self.getDataSize(self.hdr)
        #Now get the frame list - move to the frame list HDU
        self.fd.seek(dsize,1)
        try:
            self.frameno=FITS.Read(self.fd,allHDU=0)[1]
        except:
            print "Unable to read frame numbers"
            traceback.print_exc()
        try:
            self.timestamp=FITS.Read(self.fd,allHDU=0)[1]
        except:
            print "Unable to read timestamps"
            traceback.print_exc()
        self.nextHDUoffset=self.fd.tell()

    def getDataSize(self,hdr,full=1):
        nd=int(hdr["NAXIS"])
        bytes=abs(int(hdr["BITPIX"]))/8
        for i in range(nd):
            bytes*=int(hdr["NAXIS%d"%(i+1)])
        if full:
            bytes=((bytes+2779)//2880)*2880
        return bytes

    def getIndexByTime(self,tm):
        indx=0
        while indx<self.timestamp.shape[0] and self.timestamp[indx]<tm:
            indx+=1
        if indx==self.timestamp.shape[0]:
            indx=None
        return indx
    def getIndexByFrame(self,fno):
        indx=0
        while indx<self.frameno.shape[0] and self.frameno[indx]<fno:
            indx+=1
        if indx==self.frameno.shape[0]:#not found
            indx=None
        return indx
    def getEntryByIndex(self,index,doByteSwap=1):
        if index==None:
            return None
        if index>=self.dims[0]:
            return None
        esize=reduce(lambda x,y:x*y,self.dims[1:])*abs(self.bitpix)/8
        self.fd.seek(self.dataOffset+index*esize,0)
        data=self.fd.read(esize)
        data=numpy.fromstring(data,dtype=self.bpdict[self.bitpix])
        data.shape=self.dims[1:]

        if numpy.little_endian and doByteSwap:
            if self.hdr.has_key("UNORDERD") and self.hdr["UNORDERD"]=='T':
                pass
            else:
                data.byteswap(True)
        bscale = string.atof(self.hdr.get('BSCALE', '1.0'))
        bzero = string.atof(self.hdr.get('BZERO', '0.0'))
        if bscale!=1:
            data*=bscale#array(bscale,typecode=typ)
        if bzero!=0:
            data+=bzero#array(bzero,typecode=typ)
        return data,self.frameno[index],self.timestamp[index]
        
    def getNEntries(self):
        return self.dims[0]
    def getNDataUnits(self):
        pass
    def setDataUnit(self,n):
        """Sets the current HDU"""
        pass
    def makeTime(self,y=2010,m=9,d=27,H=0,M=0,S=0,dst=-1):
        """Makes a time value for the specified date.
        If dst==0, makes a UTC time.
        """
        if y<2000:
            y+=2000#make a valid year.
        return time.mktime((y,m,d,H,M,S,0,1,dst))
if __name__=="__main__":
    if len(sys.argv)>1:
        if sys.argv[1]=="convert":
            iname=sys.argv[2]
            oname=sys.argv[3]
            s=Saver(iname,"r")
            s.tofits(oname)
