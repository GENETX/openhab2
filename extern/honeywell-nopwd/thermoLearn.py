#!/usr/bin/python3
import csv
#import datetime
from datetime import datetime, date, time

from scipy.optimize import curve_fit
import time
import scipy
import numpy
import requests

#import matplotlib.pyplot as plt

    
    
#def fn(x, a, b,):
    #return x[0] + a*x[1]+ b*x[2]

#def fn(x, a, b, c):
    #return x[0] + a*x[1]*(1-x[3]) + b*x[1]*(x[3]) + c*x[2]
    
def fn(x, a, b, c):
	return xn[0] + a*xn[1]*xn[4] + b*xn[3] + c*xn[2]

# x[0] = indoor
# x[1] = error (setpoint - error)
# x[2] = deltaT (indoor-outdoor)
# x[3] = binary for thermostat

tmin = int(time.time()) - 4*7*24*60*60
			

to0 = []
ti0 = []
ts0 = []
to1 = []
ti1 = []
ts1 = []

y = []
x = [[] for x in range(5)]

#read data
reader = csv.reader(open('Item13.txt', 'r'))
for row in reader:
	dt = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
	dt = int(time.mktime(dt.timetuple()))
	if(dt >= tmin):
		ti0.append(dt)
		ti1.append(float(row[1]))
	
reader = csv.reader(open('Item5.txt', 'r'))
for row in reader:
	dt = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
	dt = int(time.mktime(dt.timetuple()))
	if(dt >= tmin):
		to0.append(dt)
		to1.append(float(row[1]))
	
reader = csv.reader(open('Item10.txt', 'r'))
for row in reader:
	dt = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
	dt = int(time.mktime(dt.timetuple()))
	if(dt >= tmin):
		ts0.append(dt)
		ts1.append(float(row[1]))	
	
tol = to1[0]
til = ti1[0]
tsl = ts1[0]

TindoorPrev = 0

ji = 0
jo = 0
js = 0

lastIndex = 0

for i in range(5, len(ti1)):
	if((ti0[i] - 240) > ti0[lastIndex] and (ti0[i] - 360) < ti0[lastIndex]):

		while(to0[jo] < ti0[i] and len(to0) > jo+1):
			jo += 1
			
		while(ts0[js] < ti0[i] and len(ts0) > js+1):
			js += 1
			
					
		ji = i

		if(ts0[js] == ti0[ji]): # and ti0[ji-5] + 240 < ti0[ji] and ti0[ji-5] > ti0[ji] - 360):	
			y.append(ti1[ji])
						
			#current temperature
			x[0].append(ti1[ji-5])
						
			#delta temperature
			x[1].append(ti1[ji-5]-to1[jo-5])
				
			#setpoint - temperature (error)
			if((ts1[js-5]-0.5) > ti1[ji-5]):
				x[2].append(ts1[js-5] - ti1[ji-5])		
				x[3].append(1)
				x[4].append(0)
			elif(ts1[js-5] > 15):
				x[2].append(0)		
				x[3].append(0)
				x[4].append(0)
			else:
				x[2].append(0)
				x[3].append(0)
				x[4].append(1)
			
	if((ti0[i] - 360) > ti0[lastIndex]):
		lastIndex = i
		
xn = []		
xn.append(numpy.asarray(x[0]))
xn.append(numpy.asarray(x[1]))
xn.append(numpy.asarray(x[2]))
xn.append(numpy.asarray(x[3]))
xn.append(numpy.asarray(x[4]))
yn = numpy.asarray(y)

popt, pcov = curve_fit(fn, xn, yn)

print(len(y))
requests.post('http://192.168.1.14:8086/rest/items/ThermoParamA', data=str(popt[0]))
requests.post('http://192.168.1.14:8086/rest/items/ThermoParamB', data=str(popt[1]))
requests.post('http://192.168.1.14:8086/rest/items/ThermoParamC', data=str(popt[2]))

#Now notify openhab



#plt.plot(to0, to1)
#plt.plot(ti0, ti1)
#plt.plot(ts0, ts1)
#plt.show()
