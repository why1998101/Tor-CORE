from ctypes import BigEndianStructure
import socket
import sys
import json
import random

host1 = "10.0.4.10" # DA Server1
host2 = "10.0.5.10" # DA Server2
server_port = 14736

#get node info from host1
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket created ...")
except:
    print("Socker Created Failed..., Exited")
    sys.exit()

# connect to server
sock.connect((host1,server_port))
str = "I want relay"
sock.sendall(bytes(str,encoding='utf-8'))
print("Sent hello msg to server")

while True:
    jsonReceived = sock.recv(1024)
    parsed = json.loads(jsonReceived)
    break;
sock.close()

#get all nodes list
begin_list_host1 =parsed['guard']
middle_list_host1 =parsed['middle']
exit_list_host1 =parsed['exit']
print("Get info from DA 1....")
print(json.dumps(parsed, indent=4, sort_keys=False))
#############################

#get node info from host2
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket created ...")
except:
    print("Socker Created Failed..., Exited")
    sys.exit()

# connect to server
sock.connect((host2,server_port))
str = "I want relay"
sock.sendall(bytes(str,encoding='utf-8'))
print("Sent hello msg to server")

while True:
    jsonReceived = sock.recv(1024)
    parsed = json.loads(jsonReceived)
    break;
sock.close()

#get all nodes list
begin_list_host2 =parsed['guard']
middle_list_host2 =parsed['middle']
exit_list_host2 =parsed['exit']
print("Get info from DA 2....")
print(json.dumps(parsed, indent=4, sort_keys=False))

begin_list = begin_list_host1+ begin_list_host2
middle_list = middle_list_host1 + middle_list_host2
exit_list = exit_list_host1 +   exit_list_host2

#randomly choose one node
begin_node= random.choice(begin_list)
middle_node = random.choice(middle_list)
exit_node = random.choice(exit_list)

# set parameter for ip, port and key
guardip = begin_node['ip']
guardport = int (begin_node['port'])
middleip = middle_node['ip']
middleport = middle_node['port']
exitip = exit_node['ip']
exitport = exit_node['port']
key1 = int (begin_node['key'])
key2 = int (middle_node['key'])
key3 = int (exit_node['key'])

# get server ip and port from CLI
serverip = sys.argv[1]
serverport = sys.argv[2]

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

for line in sys.stdin:
    if 'q' == line.rstrip():
        break

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

    clientsocket.close()

print("Exit")
