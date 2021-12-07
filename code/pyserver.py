import socket
import sys

host = ''
port = int(sys.argv[1])

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((host,port))
serversocket.listen(1)

while True:
    connection, address = serversocket.accept()
    print("connection accepted...\n")
    buf = connection.recv(4096)
    if len(buf) > 0:
        print("Received: " + buf.decode('UTF-8') + "\n")
        connection.send(buf)
    connection.close()