#!/usr/bin/env python
#Doorbell Alert System 
# Written By Fei Manheche
# Revision for Hacked.io
# Team: Electrical Disruption
# Licensed under the MIiT License (the "License")

#Ignore some libraries here that are not used in any way..... Cleanup job TODO
from bluetooth import *
import time
import httplib, urllib2
import ssl
import json
import socket
import struct
import binascii
from firebase import Firebase

#Usage of light API	//Ensure the location path is correct
import lightapi

#Bluetooth Device MAC Address, use hcitool to find this out
server_address = "00:13:04:10:11:96"
port = 1

def controlLights(option):
  api = lightapi.connect()

  lights = lightapi.getLights(api)
  for i in lights.keys():
    state = lightapi.getLightState(api, i)
    state['transitiontime'] = 1
    state['on'] = True
    lightapi.setLightState(api, i, state)
    print 'on'
    time.sleep(.20)
    state['on'] = False
    lightapi.setLightState(api, i, state)
    print 'off'

def pushNotifyWP():
  response = urllib2.urlopen('http://push.necto.me/wp/')
  html = response.read()
  
def pushFirefox(state):
  f = Firebase('https://project1.firebaseio.com/state')
  r = f.set(state)

#Bluetooth Listner
sock = BluetoothSocket( RFCOMM )
sock.connect((server_address, port))
Counter = 0

controlLights(1)
while True:

	Ddata = ''
	while True:
		r = sock.recv(1)
		if r == '\n' or r == 'Doorbell':
			Counter += 1
			if Counter == 2:
				print "Got Something"
				pushFirefox('on') #Notifies Firefox OS
				pushNotifyWP()	  #Notifies Windows Phone
				controlLights(1)  #Uses Hue Lights API
				Counter = 0
				pass
				time.sleep(1.2)
				pushFirefox('off')
				break			
sock.close()
