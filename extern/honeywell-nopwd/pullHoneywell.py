#!/usr/bin/python
import sys
import requests
from evohomeclient2 import EvohomeClient

client = EvohomeClient('my@e.mail', 'somePassword')

for device in client.temperatures():
	requests.post('http://localhost:8086/rest/items/CV_Temperature', data=str(device['temp']))
	requests.post('http://localhost:8086/rest/items/CV_Setpoint', data=str(device['setpoint']))
