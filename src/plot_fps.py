from datetime import datetime
import matplotlib.pyplot as plt
import numpy
from matplotlib import dates
from pylab import legend


time_x = [3000,5000,10000,12000,15000]
fps_t = []
fps_e = []


#Theory:  120x120 = 66.667 Hz.  3000 num of img. Exptime: 15000 [us]. 15.36 Mbps aprox
#Empirical: 120x120 = 355.450 fps. 3000 num of img. Exptime: 15000 [us]
#########
m_120 = [1.3113589930555563, 1.7046389236111146, 2.834339270833337, 3.5200261458333322, 5.1562564467592731]


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

#Theory:  100x100 = 66.667 Hz.  3000 num of img. Exptime: 15000 [us]. 10.67 Mbps aprox
#Empirical: 100x100 = 489.396 fps. 3000 num of img. Exptime: 15000 [us]
########
m_100 = [1.5993922499999951, 2.191089316666663, 3.7160825833333324, 4.4224262333333346, 5.6826870666666682]


#50x50    
#fps_t.append(333.333)
#fps_e.append(990.099)
#fps_t.append(200.000)
#fps_e.append(970.874)
#fps_t.append(100.000)
#fps_e.append(917.431)
#fps_t.append(83.333)
#fps_e.append(909.091)
#fps_t.append(66.667)
#fps_e.append(917.431)

#Theory:  50x50 = 66.667 Hz.  3000 num of img. Exptime: 15000 [us]. 2.67 Mbps aprox
#Empirical: 50x50 = 779.221 fps. 3000 num of img. Exptime: 15000 [us]
########
m_50 = [1.6931037333333354, 2.4284506000000028, 4.0837678000000119, 4.8331458666666585, 5.8004594000000056]



#hfmt = dates.DateFormatter(fmt)
#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.xaxis.set_major_locator(dates.HourLocator())
#ax.xaxis.set_major_formatter(hfmt)
#plt.subplots_adjust(bottom=.3)
#plt.xticks(rotation='vertical')
p1 = plt.plot(time_x, m_50,'go-',label='50')
p2 = plt.plot(time_x, m_100,'ro-', label='100')
p3 = plt.plot(time_x, m_120,'yo-', label='120')
#plt.title('120x120')
#plt.title('100x100')
plt.title('Mean v/s T')
plt.ylabel('Mean')
plt.xlabel('Exp Time [us]')
legend()
plt.show()             

