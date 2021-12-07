import socket
import sys
import time

guardip = sys.argv[1]
guardport = int (sys.argv[2])

def encrypt(text,s):
    result = ""

    for i in range(len(text)):
        char = text[i]
 
        if (char.isupper()):
            result += chr((ord(char) + s-65) % 26 + 65)

        elif (char.islower()):
            result += chr((ord(char) + s - 97) % 26 + 97)
        
        elif (char.isdigit()):
            result += chr((ord(char) + s - 48) % 10 + 48)

        else:
            result += char
 
    return result

def decrypt(text,s):
    return encrypt(text, -s)

line = ""
for i in range(99):
    line += "abcdefghij"

clog = open("/home/ini760/logs/simple.log", "w+")

while(1):
    clog.write("S "+str(time.time())+" \n")
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((guardip,guardport))
    print("connected...\n")

    clientsocket.send(bytes(line,'UTF-8'))
    print("Sent: " + line + "\n")
    buf = clientsocket.recv(4096)

    if len(buf) > 0:
        buf = buf.decode('UTF-8')
        print("Received: " + buf + "\n")
    clog.write("R "+str(time.time())+" "+str(len(buf))+"\n")
    clientsocket.close()