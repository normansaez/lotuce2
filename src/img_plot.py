from matplotlib.pylab import *
import time                   
import darc

ion()                        
prefix = "both"
d = darc.Control(prefix)
ncam = d.Get("ncam")
px   = d.Get("npxlx")[0]
py   = d.Get("npxly")[0]

while(True):
    stream=d.GetStream('%srtcPxlBuf'%prefix)
    data = stream[0].reshape(ncam*px,py)
    imgplot = plt.imshow(data)
    #imgplot.set_cmap('spectral')
    imgplot.set_cmap('hot')
    draw()
    time.sleep(0.5)
