#!/usr/bin/python
import sys
import requests
from evohomeclient import EvohomeClient

client = EvohomeClient('my@e.mail', 'somePassword')
client.set_status_normal()

for device in client.temperatures():
	requests.post('http://localhost:8086/rest/items/CV_Temperature', data=str(device['temp']))
