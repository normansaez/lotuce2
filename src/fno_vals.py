data=d.GetStreamBlock("rtcPxlBuf",100,asArray=1)
fno=data["rtcPxlBuf"][2]
print fno
print fno[1:]-fno[:-1]

timestamp=data["rtcPxlBuf"][1]
print timestamp
print timestamp[1:]-timestamp[:-1]

#pxls=data["rtcPxlBuf"][0]
#s1=pxls[:,:pxls.size/2].sum(1)
#s2=pxls[:,pxls.size/2:].sum(1)
#
#Then have a look at s1 and s2:
#pylab plot(s1)
#pylab.plot(s2)
#pylab.show()

