import sounddevice as sd
import numpy as np
import queue, threading
import socket, struct
from scipy.signal import find_peaks
from scipy import signal

samplerate = 44000
seconds = 10
downsample = 1
input_gain_db = 12
device = 'snd_rpi_i2s_card'

duration = 5  # seconds
blocksize = 1000
stepsize = 10

secondsPerStep = 1/samplerate * (blocksize/stepsize)

curVol = 0
lastVol = 0

buffer  = np.zeros(shape=(blocksize,2))
last_time = None
last = ""
change = False
q = queue.Queue()

def server(conn: socket.socket):
    while 1:
        val = struct.pack("!i", q.get())
        try:
            conn.send(val)
        except:
            break
    conn.close()

def processBuffer():
    global buffer
    #global diff
    #global amps
    # while True:
    #     try:
    #         data = q.get_nowait()
    #     except queue.Empty:
    #         break
    #     shift = len(data)
    #     buffer = np.roll(buffer, -shift)
    #     buffer[-shift:] = data
    #print("start process")
    # cnt = 0
    # amps    = np.zeros(shape=(2,int(blocksize/stepsize)))
    # diff    = np.zeros(shape=(2,int(blocksize/stepsize)))
    # #print("process:", last_time.currentTime if last_time != None else "")

    # while(cnt * stepsize < len(buffer)):

    #     left    = max(buffer[cnt*stepsize:(cnt +1 ) *stepsize][0].min(), buffer[cnt*stepsize:(cnt +1 ) *stepsize][0].max(), key=abs)
    #     right   = max(buffer[cnt*stepsize:(cnt +1 ) *stepsize][1].min(), buffer[cnt*stepsize:(cnt +1 ) *stepsize][1].max(), key=abs)

    #     diff[0][cnt] = left  - amps[0][cnt]
    #     diff[1][cnt] = right - amps[1][cnt]

    #     smooth = 0.6
    #     amps[0][cnt] = amps[0][cnt] * smooth +   left * (1-smooth)
    #     amps[1][cnt] = amps[1][cnt] * smooth +   right * (1-smooth)

    #     cnt += 1

    f0, _ = find_peaks([i[0] for i in buffer], height=0.006, distance=20)
    f1, _ = find_peaks([i[1] for i in buffer], height=0.006, distance=20)

    if len(f0) == 0 or len(f1) == 0:
        return
        
    d0 = np.array([buffer[i][0] if i in f0 else 0 for i in range(len(buffer))])
    d1 = np.array([buffer[i][1] if i in f1 else 0 for i in range(len(buffer))])

    #print(buffer)
    data0 = d0 - np.mean(d0)
    data1 = d1 - np.mean(d1)
    #print(data0, data1)

    corr = signal.correlate(data0, data1, "full", "fft").argmax()#-(len(data0)-1)
    lags = signal.correlation_lags(data0.size, data1.size, "full")
    lag = lags[corr]
    if lag != 0:
        q.put(lag//abs(lag))

    #peaks0 = find_peaks(diff[0], distance=blocksize/stepsize)
    #peaks1 = find_peaks(diff[1], distance=blocksize/stepsize)
    #peaks0 = np.argmax(diff[0])
    #peaks1 = np.argmax(diff[1])

    #print("1" + str(peaks0[0]))
    #print("2" + str(peaks1[0]))

    #threshold = 1

    #peakDiffX = peaks0 - peaks1
    #peakDiffX += secondsPerStep
    #print("end process")

    # for d in diff[0]:
    #     out = "#" * int(d*1000)
    #     print(out)


def callback(indata, frames, time, status):
    global buffer
    global last_time
    global change
    if status:
        print(status)
    #buffer = np.roll(buffer,-blocksize,axis=0)
    buffer[:] = indata
    #q.put(indata[:])
    #print(indata)
    #print(buffer)
    #print("callback:", time.currentTime)
    #last_time = time
    #print("Here")
    change = True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 6969))
s.listen(1)
print("Waiting for incoming connection...")
conn, addr = s.accept()
print("Got connection. Starting server thread")

t = threading.Thread(target=server, args=(conn,))
t.start()
with sd.InputStream(channels=2, callback=callback, samplerate=samplerate, blocksize=blocksize,latency="low"):
    #sde.start
    print("Start")
    while(1):
        if change:
            change = False
            processBuffer()


    #sde.stop()
t.join()
