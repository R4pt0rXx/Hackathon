import sounddevice as sd
import math
import numpy as np
from scipy.signal import find_peaks
import os
import time
samplerate = 96000
seconds = 10
downsample = 1
input_gain_db = 12
device = 'snd_rpi_i2s_card'

duration = 5  # seconds
blocksize = 1000
stepsize = 10

curVol = 0
lastVol = 0

buffer  = np.zeros(shape=(2,blocksize))
amps    = np.zeros(shape=(2,int(blocksize/stepsize)))
diff    = np.zeros(shape=(2,int(blocksize/stepsize)))

def processBuffer():
    global buffer
    global diff
    global amps
    cnt = 0
    while(cnt * stepsize < len(buffer)):

        left    = max(buffer[cnt*stepsize:(cnt +1 ) *stepsize][0].min(), buffer[cnt*stepsize:(cnt +1 ) *stepsize][0].max(), key=abs)
        right   = max(buffer[cnt*stepsize:(cnt +1 ) *stepsize][1].min(), buffer[cnt*stepsize:(cnt +1 ) *stepsize][1].max(), key=abs)

        diff[0][cnt] = left  - amps[0][cnt]
        diff[1][cnt] = right - amps[1][cnt]

        smooth = 0.6
        amps[0][cnt] = amps[0][cnt] * smooth +   left * (1-smooth)
        amps[1][cnt] = amps[1][cnt] * smooth +   right * (1-smooth)

       
        cnt += 1


    

    peaks0 = find_peaks(diff[0], distance=10)
    peaks1 = find_peaks(diff[1], distance=10)

    print("1:"+str(peaks0[0]))
    print("2:"+str(peaks1[0]))


def callback(indata, outdata, frames, time, status):
    global buffer
    if status:
        print(status)
    buffer = indata
    outdata.fill(0)

with sd.Stream(channels=2, callback=callback, device=device, samplerate=samplerate, blocksize=blocksize) as sde:
    sde.start()
    while(1):
        time.sleep(0.016)
        processBuffer()


    sde.stop()
#test
