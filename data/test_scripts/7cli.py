import socket
import sys
import time

guardip = sys.argv[1]
guardport = int (sys.argv[2])
middleip1 = sys.argv[3]
middleport1 = sys.argv[4]
middleip2 = sys.argv[5]
middleport2 = sys.argv[6]
middleip3 = sys.argv[7]
middleport3 = sys.argv[8]
middleip4 = sys.argv[9]
middleport4 = sys.argv[10]
middleip5 = sys.argv[11]
middleport5 = sys.argv[12]
exitip = sys.argv[13]
exitport = sys.argv[14]
serverip = sys.argv[15]
serverport = sys.argv[16]
key1 = int (sys.argv[17])
key2 = int (sys.argv[18])
key3 = int (sys.argv[19])
key4 = int (sys.argv[20])
key5 = int (sys.argv[21])
key6 = int (sys.argv[22])
key7 = int (sys.argv[23])

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
    line = encrypt(line, key7)
    line = exitip + " " + exitport + " " + line
    line = encrypt(line, key6)
    line = middleip5 + " " + middleport5 + " " + line
    line = encrypt(line, key5)
    line = middleip4 + " " + middleport4 + " " + line
    line = encrypt(line, key4)
    line = middleip3 + " " + middleport3 + " " + line
    line = encrypt(line, key3)
    line = middleip2 + " " + middleport2 + " " + line
    line = encrypt(line, key2)
    line = middleip1 + " " + middleport1 + " " + line
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
        buf = decrypt(buf,key4)
        buf = decrypt(buf,key5)
        buf = decrypt(buf,key6)
        buf = decrypt(buf,key7)
        print("Decryted: " + buf + "\n")
    clog.write("R "+str(time.time())+" "+str(len(buf))+"\n")
    clientsocket.close()