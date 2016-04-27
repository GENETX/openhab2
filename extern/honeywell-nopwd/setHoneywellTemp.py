#!/usr/bin/python
import sys
import requests
from evohomeclient import EvohomeClient

setpoint = requests.get('http://localhost:8086/rest/items/CV_Setpoint/state')
client = EvohomeClient('my@e.mail', 'somePassword')
client.set_temperature('Room', setpoint.text)
print(setpoint.text)

for device in client.temperatures():
	requests.post('http://localhost:8086/rest/items/CV_Temperature', data=str(device['temp']))
