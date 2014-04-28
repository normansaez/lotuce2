from datetime import datetime
import matplotlib.pyplot as plt
import numpy
from matplotlib import dates
from pylab import legend


time_x = [3000,5000,10000,12000,15000]
fps_t = []
fps_e = []

#120x120
#fps_t.append(333.333)
#fps_e.append(487.805)
#fps_t.append(200.000)
#fps_e.append(478.469)
#fps_t.append(100.000)
#fps_e.append(414.938)
#fps_t.append(83.333)
#fps_e.append(438.596)
#fps_t.append(66.667)
#fps_e.append(452.489)

#100x100
#fps_t.append(333.333)
#fps_e.append(606.061)
#fps_t.append(200.000)
#fps_e.append(595.238)
#fps_t.append(100.000)
#fps_e.append(662.252)
#fps_t.append(83.333)
#fps_e.append(606.061)
#fps_t.append(66.667)
#fps_e.append(613.497)

#50x50    
fps_t.append(333.333)
fps_e.append(990.099)
fps_t.append(200.000)
fps_e.append(970.874)
fps_t.append(100.000)
fps_e.append(917.431)
fps_t.append(83.333)
fps_e.append(909.091)
fps_t.append(66.667)
fps_e.append(917.431)


#hfmt = dates.DateFormatter(fmt)
#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.xaxis.set_major_locator(dates.HourLocator())
#ax.xaxis.set_major_formatter(hfmt)
#plt.subplots_adjust(bottom=.3)
#plt.xticks(rotation='vertical')
p1 = plt.plot(time_x, fps_t,'gx',label='theoric')
p2 = plt.plot(time_x, fps_e,'ro', label='empiric')
#plt.title('120x120')
#plt.title('100x100')
plt.title('50x50')
plt.ylabel('FPS')
plt.xlabel('Exp Time [us]')
legend()
plt.show()             

