#!/usr/bin/env python
import math
import wave
import struct
import sys

if __name__=='__main__':
    # http://stackoverflow.com/questions/3637350/how-to-write-stereo-wav-files-in-python
    # http://www.sonicspot.com/guide/wavefiles.html
    freq=440.0
    data_size=4000
    fname="test.wav"
    frate=11025.0 
    amp=64000.0   
    nchannels=1
    sampwidth=2
    framerate=int(frate)
    nframes=data_size
    comptype="NONE"
    compname="not compressed"
    note=[math.sin(2*math.pi*freq*(0.5*x/freq)) for x in range(data_size)]
    note1=[math.sin(2*math.pi*freq*((x/frate))) for x in range(data_size)]
    note2=[math.sin(2*math.pi*freq*((4*x/frate))) for x in range(data_size)]
    silence=[0 for x in range(data_size*4)]
    data = note + silence + note + silence + note1 + silence + note1 + silence + note2 + silence + note2 + silence
    wav_file=wave.open(fname, 'w')    
    wav_file.setparams((nchannels,sampwidth,framerate,nframes,comptype,compname))
    for v in data:
        sys.stdout.writeframes(struct.pack('h', int(v*amp/2)))
    wav_file.close()
