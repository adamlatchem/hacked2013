hacked2013
==========

HackerLeague summary: https://www.hackerleague.org/hackathons/hacked/hacks/hued-home

We've got the Philips Hue lights up and running/

use mkUser.py to initially connect after setting IP in lightsapi.py and pressing Link button
use getLights.py to try ranom lights

You'll need scikits.audiolab-0.11.0/ point the symlink to audiolab to your install if not
globally installed

First server written was main.py - it reads from the test.wav fifo and transcodes that audio
so it can be heard on the MacBooks speaker and flashes lights. the lights form a spectrum
analyser - three bands low.med.high. The FFT gives the spectrum and this drives the hue and
brightness of the lights.

https://en.wikipedia.org/wiki/Theremin

use node.js to run the thermin synth:
$ node server.py

This gives a server that processes URL GET requests. Any request has its URL examined and if
there is a query string the x and y values for the thermin synth are extracted. Typically
hese are sent as values from a mobile devices accelerometer and must lie in the range [0, 1].
So e.g.
http://blah.blah.blah.blah/thermin.htm?x=0.5&y=0.5

will set frequency to some halfway value :) and volume to 0.5 of max volume possible.

The output from the thermin synth goes to the thermin.raw fifo. So make sure it is a fifo:
$ mkfifo thermin.py

This can then be piped into either a transcoder (we used sox for a while :) or another server
eventually around 10a.m. on the Sunday we got it feeding into thermin.py a simple realtime
transcoder and light show used to let us hear the sound and show simple 3 band spectrum
analyser on the lights.
