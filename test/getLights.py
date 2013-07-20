#!/usr/bin/env python
import json, httplib
import sys
import time

def connect():
  api = httplib.HTTPConnection('192.168.2.208', 80)
  api.connect()
  api.url = '/api/1234567890/'
  return api

def getLights(api):
  api.request('GET', api.url + 'lights', json.dumps({}))
  return json.loads(api.getresponse().read())

def getLightState(api, id):
  api.request('GET', api.url + 'lights/' + str(id))
  return json.loads(api.getresponse().read())

def setLightState(api, id, state):
  api.request('PUT', api.url + 'lights/' + str(id) + '/state', json.dumps(state))
  return json.loads(api.getresponse().read())

api = connect()
lights = getLights(api)
while True:
  for i in lights.keys():
    print 'turn on ' + str(i)
    light = lights[i]
    state = getLightState(api, i)
    state['on'] = True
    setLightState(api, i, state)
    time.sleep(1.0/4.0)
  for i in lights.keys():
    print 'turn on ' + str(i)
    light = lights[i]
    state = getLightState(api, i)
    state['on'] = False
    setLightState(api, i, state)
