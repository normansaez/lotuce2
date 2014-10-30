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
#import numpy as np

def bit_check(x, y, img, threshold, width):
    intensity = img[y-width:y+width,x-width:x+width].mean()
#    print "(%.0f >= %.0f)" % (intensity, threshold),
    if intensity >= threshold:
#        print " ON" 
        return 1
#    print 
    return 0

#def get_centroid(img):
#    label_img = label(img)
#    regions = regionprops(label_img)
#    
#    for props in regions:
#        y0, x0 = props.centroid
#        return floor(y0), floor(x0)
#    return -1, -1

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
#        self.fd=open(name,mode)
        self.info=numpy.zeros((8,),numpy.int32)
    def write(self,data,ftime,fno):
        #XXX: We don't want save the data, instead we want just procese it.
        # camera coordinates according windows size
        #XXX commented for 200x200
        text_file = open('lotuce2-run-results.txt','a')
#        reference = '/home/lotuce2/lotuce2/src/acquisition/ref200x200_225Hz/'
#        cam0_b0 = reference+'/img_028.fits'#'/img_000.fits'
#        cam0_b1 = reference+'/img_030.fits'#'/img_001.fits'
#        cam0_b2 = reference+'/img_034.fits'#'/img_003.fits'
#        cam0_b3 = reference+'/img_010.fits'#'/img_007.fits'
#
#        cam1_b0 = reference+'/img_028.fits'#'/img_001.fits'
#        cam1_b1 = reference+'/img_030.fits'#'/img_002.fits'
#        cam1_b2 = reference+'/img_034.fits'#'/img_004.fits'
#        cam1_b3 = reference+'/img_010.fits'#'/img_008.fits'
        xi_cam0 = 200#492#200
        xf_cam0 = 400#984#400
        yi_cam0 = 0#0
        yf_cam0 = 200#656#200

        xi_cam1 = 0#0
        xf_cam1 = 200#492#200 
        yi_cam1 = 0#0
        yf_cam1 = 200#656#200 
        
        #Padding in pixels to make closed shapes and get a correct centroid
#        padding = 5#7
        #area to search intensity (mean) taking account centroid
        width = 3#5
        #Getting central coordinates
#        b0_0 = FITS.Read(cam0_b0)[1][xi_cam0:xf_cam0,yi_cam0:yf_cam0]
#        b1_0 = FITS.Read(cam0_b1)[1][xi_cam0:xf_cam0,yi_cam0:yf_cam0]
#        b2_0 = FITS.Read(cam0_b2)[1][xi_cam0:xf_cam0,yi_cam0:yf_cam0]
#        b3_0 = FITS.Read(cam0_b3)[1][xi_cam0:xf_cam0,yi_cam0:yf_cam0]
#
#        b0_1 = FITS.Read(cam1_b0)[1][xi_cam1:xf_cam1,yi_cam1:yf_cam1]
#        b1_1 = FITS.Read(cam1_b1)[1][xi_cam1:xf_cam1,yi_cam1:yf_cam1]
#        b2_1 = FITS.Read(cam1_b2)[1][xi_cam1:xf_cam1,yi_cam1:yf_cam1]
#        b3_1 = FITS.Read(cam1_b3)[1][xi_cam1:xf_cam1,yi_cam1:yf_cam1]

        #Fixed limit to not convert a binary image
#        mask_b0_0 = np.where(b0_0 > 4000,1,0)
#        mask_b1_0 = np.where(b1_0 > 4000,1,0)
#        mask_b2_0 = np.where(b2_0 > 4000,1,0)
#        mask_b3_0 = np.where(b3_0 > 4000,1,0)
#
#        mask_b0_1 = np.where(b0_1 > 4000,1,0)
#        mask_b1_1 = np.where(b1_1 > 4000,1,0)
#        mask_b2_1 = np.where(b2_1 > 4000,1,0)
#        mask_b3_1 = np.where(b3_1 > 4000,1,0)
        
        #Apply border (padding)
#        border = np.ones(b0_0.shape)
#        border[:padding,:] = 0
#        border[:,:padding] = 0
#        border[xf_cam0 - xi_cam0 - padding:,:] = 0
#        border[:, xf_cam0 - xi_cam0 - padding:] = 0
        
        #(binary image )*(original image)*(border) = acurate centroid (in theory)  
#        mask_b0_cam0 = mask_b0_0 * b0_0 * border
#        mask_b1_cam0 = mask_b1_0 * b1_0 * border
#        mask_b2_cam0 = mask_b2_0 * b2_0 * border
#        mask_b3_cam0 = mask_b3_0 * b3_0 * border
#
#        mask_b0_cam1 = mask_b0_1 * b0_1 * border
#        mask_b1_cam1 = mask_b1_1 * b1_1 * border
#        mask_b2_cam1 = mask_b2_1 * b2_1 * border
#        mask_b3_cam1 = mask_b3_1 * b3_1 * border

        #Getting centroid
        #y0_cam0, x0_cam0 = get_centroid(mask_b0_cam0)
        y0_cam0 = 140
        x0_cam0 = 190
        #y1_cam0, x1_cam0 = get_centroid(mask_b1_cam0)
        y1_cam0 = 132
        x1_cam0 = 143
#        y2_cam0, x2_cam0 = get_centroid(mask_b2_cam0)
        y2_cam0 =127
        x2_cam0 = 71
#y3_cam0, x3_cam0 = get_centroid(mask_b3_cam0)
        y3_cam0 =147
        x3_cam0 = 5
#        y0_cam1, x0_cam1 = get_centroid(mask_b0_cam1)
        y0_cam1 = 115
        x0_cam1 = 8
#y1_cam1, x1_cam1 = get_centroid(mask_b1_cam1)
        y1_cam1 = 108
        x1_cam1 = 54
#        y2_cam1, x2_cam1 = get_centroid(mask_b2_cam1)
        y2_cam1 = 105
        x2_cam1 = 125
#        y3_cam1, x3_cam1 = get_centroid(mask_b3_cam1)
        y3_cam1 = 120 
        x3_cam1 = 192
        #-------------------------------------------------------
        pxly = 200
        pxlx = 200
        fitsname = self.name.split('.fits')[0]+'_'+str(fno)+'.fits'
        mydata = data.reshape((2*pxly,pxlx))
#        FITS.Write(mydata, fitsname, writeMode='w'
        threshold = 3000
        cam_cam0 = mydata[xi_cam0:xf_cam0,yi_cam0:yf_cam0]
        b0_cam0 = bit_check(x0_cam0, y0_cam0, cam_cam0, threshold, width)
        b1_cam0 = bit_check(x1_cam0, y1_cam0, cam_cam0, threshold, width)
        b2_cam0 = bit_check(x2_cam0, y2_cam0, cam_cam0, threshold, width)
        b3_cam0 = bit_check(x3_cam0, y3_cam0, cam_cam0, threshold, width)
        num_cam0 = '0b'+str(b3_cam0)+str(b2_cam0)+str(b1_cam0)+str(b0_cam0)
        num_cam0 = eval(num_cam0)
        cam_cam1 = mydata[xi_cam1:xf_cam1,yi_cam1:yf_cam1]
#        print "-------------"
        b0_cam1 = bit_check(x0_cam1, y0_cam1, cam_cam1, threshold, width)
        b1_cam1 = bit_check(x1_cam1, y1_cam1, cam_cam1, threshold, width)
        b2_cam1 = bit_check(x2_cam1, y2_cam1, cam_cam1, threshold, width)
        b3_cam1 = bit_check(x3_cam1, y3_cam1, cam_cam1, threshold, width)
        num_cam1 = '0b'+str(b3_cam1)+str(b2_cam1)+str(b1_cam1)+str(b0_cam1)
        num_cam1 = eval(num_cam1)
        text_file.write('%f %d %d %d\n'%(ftime, fno, num_cam0, num_cam1))
        text_file.close()
        c0 = mydata[:200,:]
        c1 = mydata[200:400,:]
    
        c0_x = c0.sum(0)
        c0_y = c0.sum(1)
        col_cam0 = numpy.array([numpy.append(c0_x,c0_y)])
        c1_x = c1.sum(0)
        c1_y = c1.sum(1)
        col_cam1 = numpy.array([numpy.append(c1_x,c1_y)])
        myprofile = numpy.append(col_cam0,col_cam1,0)

        FITS.Write(myprofile, fitsname, writeMode='w')
#        if num_cam1 != num_cam0:
#            FITS.Write(mydata, fitsname, writeMode='w')
#        FITS.Write(mydata, fitsname, writeMode='w')
#        if num_cam1 != num_cam0:
#            FITS.Write(mydata, fitsname, writeMode='w')
        return
        #XXX End of the fix
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
