#!/usr/bin/python
import sys
import requests

#XBMC settings
xbmcip = '192.168.1.14'
xbmcport = '8090'

xbmc = requests.get('http://'+xbmcip+':'+xbmcport+'/jsonrpc?request={"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}')
data = xbmc.json()

#check if we have an active player
if len(data["result"]) == 1:
    if data["result"][0]["playerid"] == 0:
	#toggle audio = 0
	requests.get('http://'+xbmcip+':'+xbmcport+'/jsonrpc?request={"jsonrpc": "2.0", "method": "Player.GoTo", "params": { "playerid": 0,"to":"previous" }, "id": 1}')
    else:
	#toggle video = 1
	requests.get('http://'+xbmcip+':'+xbmcport+'/jsonrpc?request={"jsonrpc": "2.0", "method": "Player.GoTo", "params": { "playerid": 1,"to":"previous" }, "id": 1}')
