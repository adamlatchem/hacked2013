#!/usr/bin/env python
import sys
import time
import random

import lightapi

api = lightapi.connect()
lights = lightapi.getLights(api)
for i in lights.keys():
    state = lightapi.getLightState(api, i)
    # 1 == 100ms for state transition
    state['transitiontime'] = 1
    lightapi.setLightState(api, i, state)

while True:
  for i in lights.keys():
    print 'turn on ' + str(i)
    light = lights[i]
    state = lightapi.getLightState(api, i)
    state['on'] = True

    # hue falls in the rnage [0,65535]
    h = random.random() * 65535.0

    # force to int as otherwise odd behaviour occurs
    state['hue'] = int(h)
    lightapi.setLightState(api, i, state)
    time.sleep(1.0/4.0)

  for i in lights.keys():
    print 'turn off ' + str(i)
    light = lights[i]
    state = lightapi.getLightState(api, i)
    state['on'] = False
    lightapi.setLightState(api, i, state)
