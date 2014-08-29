data=d.GetStreamBlock("rtcPxlBuf",100,asArray=1)
fno=data["rtcPxlBuf"][2]
print fno
print fno[1:]-fno[:-1]

timestamp=data["rtcPxlBuf"][1]
print timestamp
print timestamp[1:]-timestamp[:-1]
