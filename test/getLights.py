#!/usr/bin/env python
import sys
import time
import random

import lightapi

api = lightapi.connect()
lights = lightapi.getLights(api)
for i in lights.keys():
    state = lightapi.getLightState(api, i)
    state['transitiontime'] = 1
    lightapi.setLightState(api, i, state)

while True:
  for i in lights.keys():
    print 'turn on ' + str(i)
    light = lights[i]
    state = lightapi.getLightState(api, i)
    state['on'] = True
    h = random.random() * 65535.0
    state['hue'] = int(h)
    lightapi.setLightState(api, i, state)
    time.sleep(1.0/4.0)
  for i in lights.keys():
    print 'turn on ' + str(i)
    light = lights[i]
    state = lightapi.getLightState(api, i)
    state['on'] = False
    lightapi.setLightState(api, i, state)
