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
import math
import select
import curses
from plotting import plot

f1 = 0.08
f2 = 0.18

# number of 100ms chunks
mult = 1

def key():
    i,o,e = select.select([sys.stdin],[],[],0.0001)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return input
    return None

def player():
  #process = subprocess.Popen("sox -v 8 -c1 -traw -r44100 -b16 -e signed-integer - -tcoreaudio".split(' '), stdin=subprocess.PIPE)
  process = subprocess.Popen("sox -c1 -traw -r44100 -b8 -e signed-integer - -tcoreaudio".split(' '), stdin=subprocess.PIPE, stderr=subprocess.PIPE)
  return process.stdin

def loadData():
  fname="thermin.raw"
  wav_file=open(fname,'r')
  return wav_file

def analBin2(w, frate, size):
  # Find the peak in the coefficients
  i = 0
  j = 0
  m = 0
  w /= size
  for i in range(len(w)):
    if m < abs(w[i]):
      m = abs(w[i])
      j = i
  return ((abs(w[j])),j / float(len(w)))

def fft2(theFile, offset, frate, chunk):
  data = theFile[offset:offset + chunk]

  w = np.fft.fft(data)
  w = np.fft.fftshift(w)
  freqs = np.fft.fftfreq(len(w))
  noBins = len(w)
  band1 = 1.0/3.0 * noBins
  band2 = 2.0/3.0 * noBins
  bin3Freq = analBin2(w[0:band1], frate, chunk)
  bin2Freq = analBin2(w[band1:band2], frate, chunk)
  bin1Freq = analBin2(w[band2:], frate, chunk)
  return (bin1Freq, bin2Freq, bin3Freq)

def analBin(w, frate):
  # Find the peak in the coefficients
  i = 0
  j = 0
  m = 0
  for i in range(len(w)):
    if m < w[i]:
      m = w[i]
      j = i
  if len(w) == 0:
    return (0, 0)
  if w[j] <= 0:
    return (0, 0)
  return (max(0, math.log10(w[j])), j / float(len(w)))

def plotit(w):
        pts = [complex(i,50*w[i]) for i in range(len(w))]
        print len(w)
        plot(pts,2000,1)


def fft(y,offset,Fs,chunk):

  import array

  #y = np.array(y)
  x = array.array('l')
  for i in y:
    x.append(ord(i))
  y = x
  #y = np.zeros((len(y)))

  global f1
  global f2

  if len(y) == 0:
    return ((0,0),(0,0),(0,0))

  y = y[offset:offset + chunk]
  n = len(y) # length of the signal
  k = np.arange(n)
  T = n/Fs
  #frq = k/T # two sides frequency range
  #frq = frq[range(n/2)] # one side frequency range

  Y = np.fft.fft(y)/n # fft computing and normalization
  Y = Y[range(n/2)]
  Y = abs(Y) 
  Y = Y[:len(Y)/2]
  
  n = len(Y) # length of the signal

  band1 = f1 * n
  band2 = f2 * n
  bin3Freq = analBin(Y[0:band1], Fs)
  bin2Freq = analBin(Y[band1:band2], Fs)
  bin1Freq = analBin(Y[band2:], Fs)
 
  return (bin1Freq, bin2Freq, bin3Freq)


def b2j(b):
  if b:
    return True
  else:
    return False

lMap = {u'1':'2', u'2':'1', u'3':'3'}

if __name__ == '__main__':

  sox = player()  
  
  api = lightapi.connect()

  lights = lightapi.getLights(api)
  print lights
  for i in lights.keys():
    state = lightapi.getLightState(api, i)
    state['transitiontime'] = 1
    state['on'] = False
    lightapi.setLightState(api, i, state)

  fd = loadData()
  frameRate = 44100

  chunk = int(frameRate / 10.0 * mult)

  offset = 0

  while True:

   print '.',

   filedata = ""
   while len(filedata) < chunk:
     filedata += fd.read(chunk)

   analyser = fft(filedata, 0, frameRate, chunk)
   
   sox.write(filedata)

   l = lights.keys()
   l.sort()
   for k in l:
     
     j = int(k) - 1
     if j > 2:
       continue
     i = lMap[k]

     state = lightapi.getLightState(api, i)
      
     v,d = analyser[j]
     h = int(d * 65535)
     b = v * 64.0
     s = 255
  
     state['on'] = b2j(b > 1)

     state['hue'] = int(h)
     state['sat'] = int(s)
     state['bri'] = int(b)

     lightapi.setLightState(api, i, state)

  for i in lights.keys():
    state = lightapi.getLightState(api, i)
    state['transitiontime'] = 1
    state['on'] = False
    lightapi.setLightState(api, i, state)
