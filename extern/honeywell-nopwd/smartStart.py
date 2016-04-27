#!/usr/bin/python
from datetime import datetime, date, time 
import sys
import requests
#from evohomeclient import EvohomeClient

#set the timedelta, this has to be the same as in the other model! However, here it is given in minutes!!!
# So in my case thats 5:
timeDelta = 5

#Obtain the current time
#Note that all times in this script are given in minutes since the start of THIS day!
timeNow = datetime.now().minute + 60*datetime.now().hour

#Obtain the coefficients that were found using the learning script from the OpenHAB API
a = float(requests.get('http://localhost:8086/rest/items/ThermoParamA/state').text)
b = float(requests.get('http://localhost:8086/rest/items/ThermoParamB/state').text)
c = float(requests.get('http://localhost:8086/rest/items/ThermoParamC/state').text)

#Get the other user predefined settings:
setpointHour = int(requests.get('http://localhost:8086/rest/items/CV_SStart_Hour/state').text)		# Hour for which the new setpoint should be reached
setpointMin = int(requests.get('http://localhost:8086/rest/items/CV_SStart_Min/state').text)		# Idem for the minute
tempSet = float(requests.get('http://localhost:8086/rest/items/CV_SStart_Setpoint/state').text)		# The actual new setpoint to be reached
tempIn 	= float(requests.get('http://localhost:8086/rest/items/Inside_Temperature/state').text) 		# The current indoor temperature
tempOut = float(requests.get('http://localhost:8086/rest/items/Weather_Temperature/state').text) 	# The current outdoor temperature
tempDev = float(requests.get('http://localhost:8086/rest/items/CV_SStart_Dev/state').text)			# The allowed deviation (e.g., reaching setpoint-deviation by the time is enough) 
# Note: This should be at least 0.5 degrees!

#calculate the time of this day at which the setpoint has to be reached
timeSetpoint = setpointMin + setpointHour*60

if(timeSetpoint < timeNow-30):
	#We are probably talking about a setpoint to be reached the next day, add 24 hours:
	timeSetpoint += (60*24)

#first try 5 minutes without heating
tempIn = tempIn + a * (tempIn - tempOut)
timeRequired = timeDelta

#Now simulate heating (MPC) the room using the model:

while((timeRequired < timeDelta*100) and (tempIn < (tempSet - tempDev))): #stop either with simulation if we reach our setpoint, or it takes too long
	timeRequired += timeDelta							
	tempIn = tempIn + a * (tempIn - tempOut) + b + c * (tempSet - tempIn) #calculate the next temperature


# Check if we reach the temperature in time:
if(timeNow + timeRequired >= timeSetpoint):
	# Well apparently we don't.
	# But note, we tried to start heating in 5 minutes.
	# Hence we need those 5 minutes and should start heating NOW! No way we can postpone this.
		
	##indicate that we have succesfully executed a smartstart
	requests.post('http://localhost:8086/rest/items/CV_SStart_Enabled', 'OFF')
		
	#and change the settpoint in the interface too
	requests.post('http://localhost:8086/rest/items/CV_Setpoint', data=str(tempSet))