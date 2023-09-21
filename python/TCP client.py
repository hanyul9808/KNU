import socket
port = int(input("port NO :"))
address = ("localhost",port)
BUFSIZE = 1024
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)
while True:
    msg = input("message to send: ")
    s.send(msg.encode())
    data = s.recv(BUFSIZE)
    print("Received message : %s" %data.decode())
   #socket test 2