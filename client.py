import socket, signal, struct, tkinter as tk

BUFFER_SIZE=1024

run = True

def signal_handler():
    global run
    run = False



signal.signal(signal.SIGINT, signal_handler)

window = tk.Tk()

canvas = tk.Canvas(window)
canvas.pack()
canvas.create_rectangle(10,10,20,20)

def do_smth():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((input("IP: "), 6969))
    while run:
        data = b''
        while len(data) < 4:
            data += s.recv(BUFFER_SIZE)
        print(struct.unpack("!i",data[:4])[0])

window.after(1000,do_smth)
window.mainloop()