from matplotlib.pylab import *
import time                   
import darc

ion()                        
 
x = range(0,5000)
line, = plot(x,x)          
line.axes.set_ylim(0, 4095) 
 
starttime = time.time()         
t = 0                          
prefix = "both"
d = darc.Control(prefix)
while(True):
    stream=d.GetStream('%srtcPxlBuf'%prefix)
    data = stream[0]
    t = time.time() - starttime 
    y = data        
    line.set_ydata(y)           
    draw()
