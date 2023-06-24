import socket

BUFFER_SIZE=1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((input("IP: "), 6969))
while 1:
    data = s.recv(BUFFER_SIZE)
    print(data)