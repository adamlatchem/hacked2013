#!/usr/bin/env python
import json
import httplib
import sys
import time
import random
import audiolab
import numpy as np
import wave
import struct

def loadData():
  data_size=20000
  fname="test.wav"
  wav_file=wave.open(fname,'r')
  data=wav_file.readframes(data_size)
  wav_file.close()
  data=struct.unpack('{n}h'.format(n=data_size), data)
  data=np.array(data)
  return data

def analBin(w):
  frate=11025.0 
  freqs = np.fft.fftfreq(len(w))
  # Find the peak in the coefficients
  idx=np.argmax(np.abs(w)**2)
  return idx

def fft(theFile, offset):
  data = theFile[offset:offset + 1024]

  w = np.fft.fft(data)
  freqs = np.fft.fftfreq(len(w))
  noBins = len(freqs)
  print noBins
  band1 = 300
  band2 = 600
  bin1Freq = analBin(w[0:band1])
  bin2Freq = analBin(w[band1:band2])
  bin3Freq = analBin(w[band2:])
  return (bin1Freq, bin2Freq, bin3Freq)

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

if __name__ == '__main__':

  api = connect()
  filedata = loadData()

  lights = getLights(api)
  for i in lights.keys():
    state = getLightState(api, i)
    state['transitiontime'] = 1
    setLightState(api, i, state)

  offset = 0
  while True:
    offset += 1024
    if offset > len(filedata) - 1024:
      offset = 0
    analyser = fft(filedata, offset)

    for i in lights.keys():
      light = lights[i]
      i = int(i)
      state = getLightState(api, i)
      state['on'] = True
      d = analyser[i - 1]
      h = d * 65535.0 / 300.0
      print "%d    %d" % (d,h)
      state['bri'] = int(h)
      setLightState(api, i, state)

    time.sleep(0.1)

