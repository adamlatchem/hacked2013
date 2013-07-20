#!/usr/bin/env python
import json, httplib

def connect():
  api = httplib.HTTPConnection('192.168.2.208', 80)
  api.connect()
  return api

def getLights(api):
  api.request('GET', '/api/1234567890/lights', json.dumps({}))
  return json.loads(api.getresponse().read())

api = connect()
lights = getLights(api)
print lights
