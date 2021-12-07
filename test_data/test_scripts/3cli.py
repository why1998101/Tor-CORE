import socket
import sys
import time

guardip = sys.argv[1]
guardport = int (sys.argv[2])
middleip = sys.argv[3]
middleport = sys.argv[4]
exitip = sys.argv[5]
exitport = sys.argv[6]
serverip = sys.argv[7]
serverport = sys.argv[8]
key1 = int (sys.argv[9])
key2 = int (sys.argv[10])
key3 = int (sys.argv[11])

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

base = ""
for i in range(99):
    base += "abcdefghij"

clog = open("/home/ini760/logs/client.log", "w+")

while(1):
    clog.write("S "+str(time.time())+" \n")
    line = base
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((guardip,guardport))
    print("connected...\n")

    line = serverip + " " + serverport + " " + line
    line = encrypt(line, key3)
    line = exitip + " " + exitport + " " + line
    line = encrypt(line, key2)
    line = middleip + " " + middleport + " " + line
    line = encrypt(line, key1)

    clientsocket.send(bytes(line,'UTF-8'))
    print("Sent: " + line + "\n")
    buf = clientsocket.recv(4096)

    if len(buf) > 0:
        buf = buf.decode('UTF-8')
        print("Received: " + buf + "\n")
        buf = decrypt(buf,key1)
        buf = decrypt(buf,key2)
        buf = decrypt(buf,key3)
        print("Decryted: " + buf + "\n")
    clog.write("R "+str(time.time())+" "+str(len(buf))+"\n")
    clientsocket.close()