#!/usr/bin/env python -u
import json
import httplib
import sys
import time
import random
import audiolab
import numpy as np
import wave
import struct
import lightapi
import subprocess
import colorsys

# number of 100ms chunks
mult = 1

def player():
  #process = subprocess.Popen("sox -v 8 -c2 -traw -r196400 -b16 -e signed-integer - -tcoreaudio".split(' '), stdin=subprocess.PIPE)
  process = subprocess.Popen("sox -c2 -traw -r196400 -b16 -e signed-integer - -tcoreaudio".split(' '), stdin=subprocess.PIPE)
  return process.stdin

def loadData():
  fname="test.wav"
  wav_file=wave.open(fname,'r')
  data_size = wav_file.getnframes() * wav_file.getnchannels()
  data=wav_file.readframes(data_size)
  frameRate = wav_file.getframerate()
  wav_file.close()
  data=struct.unpack('{n}h'.format(n=data_size), data)
  data=np.array(data)
  return frameRate,data

def analBin(w, frate):
  freqs = np.fft.fftfreq(len(w))
  # Find the peak in the coefficients
  idx=np.argmax(np.abs(w)**2)
  return idx

def fft(theFile, offset, frate, chunk):
  data = theFile[offset:offset + chunk]

  w = np.fft.fft(data)
  freqs = np.fft.fftfreq(len(w))
  noBins = len(freqs)
  band1 = 1000
  band2 = 1012
  bin1Freq = analBin(w[0:band1], frate)
  bin2Freq = analBin(w[band1:band2], frate)
  bin3Freq = analBin(w[band2:], frate)
  return (bin1Freq, bin2Freq, bin3Freq)

def b2j(b):
  if b:
    return True
  else:
    return False

lightMap = {'1':'2', '2':'1', '3':'3'}

if __name__ == '__main__':

  sox = player()  
  
  api = lightapi.connect()

  lights = lightapi.getLights(api)
  for i in lights.keys():
    state = lightapi.getLightState(api, i)
    state['transitiontime'] = 1
    state['on'] = True
    lightapi.setLightState(api, i, state)

  frameRate,filedata = loadData()
  frameRate = 196400

  chunk = frameRate / 10 * mult

  chunk = frameRate / 10.0 * mult

  offset = 0
  while True:

    offset += chunk
    if offset > len(filedata) - chunk:
      offset = 0
    analyser = fft(filedata, offset, frameRate, chunk)

    sox.write(filedata[offset:offset + chunk])

    for i in lights.keys():
      i = lightMap[i]

      light = lights[i]
      j = int(i)

      state = lightapi.getLightState(api, i)
      
      d = analyser[j - 1]
      h = int(d * 512)
      s = 255
      b = 128
  
      state['on'] = b2j(d > 2)

      state['hue'] = int(h)
      state['sat'] = int(s)
      state['bri'] = int(b)

      print (h,s,b), state['on'],

      lightapi.setLightState(api, i, state)

    print

#    time.sleep(0.1 * mult)

