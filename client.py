import socket, signal, struct, tkinter as tk, threading, sys

BUFFER_SIZE=1024
WIDTH=1000
HEIGHT=500
A=100

run = True

def signal_handler(x,y):
    global run
    run = False
    sys.exit(0)

def reset(canvas: tk.Canvas, id):
    canvas.moveto(id, WIDTH/2-A/2, HEIGHT/2-A/2)

signal.signal(signal.SIGINT, signal_handler)

ip = "192.168.2.4" #input("IP: ")

window = tk.Tk()
window.geometry("%dx%d" % (WIDTH,HEIGHT+50))

canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT)
canvas.pack()
id = canvas.create_rectangle(WIDTH/2-A/2,HEIGHT/2-A/2,WIDTH/2+A/2,HEIGHT/2+A/2)

button = tk.Button(window, text="Reset", command=lambda: reset(canvas, id))
button.pack()

def do_smth(canvas, id, ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, 6969))
    while run:
        data = b''
        while len(data) < 4:
            data += s.recv(BUFFER_SIZE)
        canvas.move(id, struct.unpack("!i",data[:4])[0]*10,0)

threading.Thread(target=do_smth, args=(canvas, id, ip,)).start()
window.mainloop()