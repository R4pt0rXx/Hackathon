import sounddevice as sd
import numpy as np
import queue, threading
import socket, struct, argparse
from scipy.signal import find_peaks
from scipy import signal

samplerate = 48000
device = 'snd_rpi_i2s_card'
blocksize = 1000

secondsPerStep = 1/samplerate 
buffer  = np.zeros(shape=(blocksize + blocksize//10,2))
change = False
q = queue.Queue()

parse = argparse.ArgumentParser()
parse.add_argument("-s", action="store_true")
args = parse.parse_args()

def get_WiNkEl(diff):
    return np.rad2deg(np.arcsin((diff * secondsPerStep  * 343.2 )/ 0.044))

def server(conn: socket.socket):
    while 1:
        val = struct.pack("!i", q.get())
        try:
            conn.send(val)
        except:
            break
    conn.close()

def m_fun(tpl):
    tpl = (abs(tpl[0]), abs(tpl[1]))

def processBuffer():
    global buffer

    f0, _ = find_peaks([i[0] for i in buffer], height=0.012, distance=20)

    if len(f0) == 0 :
        return

    d0 = np.array([buffer[i][0] * buffer[i][0] for i in range(len(buffer))])
    d1 = np.array([buffer[i][1] * buffer[i][1] for i in range(len(buffer))])

    data0 = d0 - np.mean(d0)
    data1 = d1 - np.mean(d1)

    corr = signal.correlate(data0, data1, "full", "fft").argmax()#-(len(data0)-1)
    lags = signal.correlation_lags(data0.size, data1.size, "full")
    lag = lags[corr]
    if abs(lag) > 7:
        return
    winkel =(get_WiNkEl(lag))
    print(winkel)
    if args.s and not np.isnan(winkel):    
        q.put(int(winkel*1000))


def callback(indata, frames, time, status):
    global buffer
    global last_time
    global change
    if status:
        print(status)
    buffer = np.roll(buffer,blocksize//10,axis=0)
    buffer[blocksize//10:] = abs(indata)

    change = True

if args.s:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 6969))
    s.listen(1)
    print("Waiting for incoming connection...")
    conn, addr = s.accept()
    print("Got connection. Starting server thread")
    t = threading.Thread(target=server, args=(conn,))
    t.start()

with sd.InputStream(device=device, channels=2, callback=callback, samplerate=samplerate, blocksize=blocksize,latency="low"):
    print("Start")
    while(1):
        if change:
            change = False
            processBuffer()
