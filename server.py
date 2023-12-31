#authors: DieDosenTomaten - Jannik, Raphael, Hendrik 24.06.2023

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
buffer  = np.zeros(shape=(blocksize + blocksize//10,2)) #to have a bit of sliding window we at a tenth of the blocksize to the buffersize
change = False
q = queue.Queue()

parse = argparse.ArgumentParser()
parse.add_argument("-s", action="store_true")
parse.add_argument("--silent", action="store_true")
args = parse.parse_args()

def get_WiNkEl(diff):
    #calculates the angle from the calculated time differential
    return np.rad2deg(np.arcsin((diff * secondsPerStep  * 343.2 )/ 0.044))

#server function to send data to client
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

    f0, _ = find_peaks([i[0] for i in buffer], height=0.012, distance=20) #only process further if there are peaks over 0.012

    if len(f0) == 0 :
        return

    d0 = np.array([buffer[i][0] * buffer[i][0] for i in range(len(buffer))]) #sqaure all Elements in Buffer
    d1 = np.array([buffer[i][1] * buffer[i][1] for i in range(len(buffer))]) #so that small values become smaller and big values become bigger

    data0 = d0 - np.mean(d0) #normalize arrays
    data1 = d1 - np.mean(d1)

    corr = signal.correlate(data0, data1, "full", "fft").argmax() #correlation between left and right channel
    lags = signal.correlation_lags(data0.size, data1.size, "full") 
    lag = lags[corr] #get lag (delay) from lag function
    if abs(lag) > 6: #all lags above 6 are not processible with our microphones
        return
    winkel = get_WiNkEl(lag)
    if not args.silent:
        print(winkel)

    if args.s and not np.isnan(winkel):    
        q.put(int(winkel*1000)) #send data to client


def callback(indata, frames, time, status):
    global buffer
    global last_time
    global change
    if status:
        print(status)
    buffer = np.roll(buffer,blocksize//10,axis=0) #slide window
    buffer[blocksize//10:] = abs(indata) #add new data

    change = True

if args.s:
    #setup server
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
