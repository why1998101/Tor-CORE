import socket
import sys
import time
from multiprocessing import Process
import random
import netifaces as ni

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

def handle_relay(host, port, key):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((host,port))
    serversocket.listen(1)

    while True:
        connection, address = serversocket.accept()
        print("connection accepted...\n")
        buf = connection.recv(4096)
        if len(buf) > 0:
            buf = buf.decode('UTF-8')
            print("Received: " + buf + "\n")
            buf = decrypt(buf,key)
            tmp = buf.split()
            nhost = tmp[0]
            nport = int(tmp[1])
            buf = " ".join(tmp[2:])
            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientsocket.connect((nhost,nport))
            
            clientsocket.send(bytes(buf,'UTF-8'))
            print("Sent: " + buf + "\n")
            buf = clientsocket.recv(4096)
            if len(buf) > 0:
                buf = buf.decode('UTF-8')
                print("Received: " + buf + "\n")
                buf = encrypt(buf,key)
                connection.send(bytes(buf,'UTF-8'))
            clientsocket.close()
        connection.close()
    

def handle_heartbeat(directory_servers, relay_type, local_ip, relay_port, encryption_key, interval):
    while True:
        try:
            for (directory_host, directory_port) in directory_servers:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    try:
                        s.connect((directory_host, directory_port))
                        ts = str(int(time.time()))
                        ip = local_ip
                        port = str(relay_port)
                        key = str(encryption_key)
                        type = relay_type
                        status = 'ON'
                        info = [ts, ip, port, key, type, status]
                        msg = ' '.join(info).encode("utf-8")
                        s.sendall(msg)
                        print(f"info sent to directory {directory_host}:{str(directory_port)}")
                    except socket.error as e:
                        print(f"cannot connect to directory server {directory_host}:{str(directory_port)}: {e}")
                        
            print(f'sleep for {interval} seconds\n')
            time.sleep(interval)
        except (KeyboardInterrupt, SystemExit):
            print("going offline, sending status update")
            for (directory_host, directory_port) in directory_servers:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    try:
                        s.connect((directory_host, directory_port))
                        ts = str(int(time.time()))
                        ip = local_ip
                        port = str(relay_port)
                        key = str(encryption_key)
                        type = relay_type
                        status = 'OFF'
                        info = [ts, ip, port, key, type, status]
                        msg = ' '.join(info).encode("utf-8")
                        s.sendall(msg)
                        print(f"info sent to directory {directory_host}:{str(directory_port)}")
                    except socket.error as e:
                        print(f"cannot connect to directory server {directory_host}:{str(directory_port)}: {e}")
            sys.exit(0)

relay_host = ''
relay_port = int (sys.argv[1])
relay_type = sys.argv[2]

directory_servers = [('10.0.4.10', 14760), ('10.0.5.10', 14760)]
heartbeat_interval = 15

ni.ifaddresses('eth0')
local_ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
random.seed(local_ip)
encryption_key = random.randint(0, 10000)
print('local IP is ' + local_ip)
print('encryption key is ' + str(encryption_key))

relay_process = Process(target=handle_relay, args=(relay_host, relay_port, encryption_key))
heartbeat_process = Process(target=handle_heartbeat, args=(directory_servers, relay_type, local_ip, relay_port, encryption_key, heartbeat_interval))

relay_process.start()
heartbeat_process.start()