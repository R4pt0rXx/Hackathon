import socket, signal, struct, tkinter as tk, threading, sys, numpy as np

BUFFER_SIZE=1024
WIDTH=1000
HEIGHT=500
A=100 #side length of middle square

run = True

def signal_handler(x,y):
    global run
    run = False
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print("Hello, please enter the IP of the Winkly Server :)")
ip = input("IP: ")

window = tk.Tk()
window.geometry("%dx%d" % (WIDTH,HEIGHT+50))

canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT)
canvas.pack()
#create figures
id_rect = canvas.create_rectangle(WIDTH/2-A/2,HEIGHT/2-A/2,WIDTH/2+A/2,HEIGHT/2+A/2, fill="red")
id_line = canvas.create_line(WIDTH/2,HEIGHT/2,WIDTH/2,HEIGHT,fill="yellow",width=3)
id_arc = canvas.create_arc((WIDTH-HEIGHT)/2, 0, (WIDTH+HEIGHT)/2, HEIGHT, start=180, extent=180)

#get data from server and refresh canvas in background
def do_smth(canvas: tk.Canvas, id, ip):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, 6969))
    except:
        canvas.create_text(100,100,text="No connection to server!")
        return
    while run:
        data = b''
        while len(data) < 4:
            data += s.recv(BUFFER_SIZE)
        num = -struct.unpack("!i",data[:4])[0] / 1000
        print(num)
        canvas.coords(id, WIDTH/2,HEIGHT/2,WIDTH/2+np.sin(np.deg2rad(num))*HEIGHT/2, HEIGHT/2+np.cos(np.deg2rad(num))*HEIGHT/2)

threading.Thread(target=do_smth, args=(canvas, id_line, ip,)).start()
window.mainloop()