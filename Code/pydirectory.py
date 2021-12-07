import json
from multiprocessing import Process, Lock
import socket
import time

ENCODING = "utf-8"
RELAY_INFO_FILE = "relay_info.json"

"""
source: https://code.activestate.com/recipes/577803-reader-writer-lock-with-priority-for-writers/
"""
class RWLock:
	def __init__(self):
		self.__read_switch = _LightSwitch()
		self.__write_switch = _LightSwitch()
		self.__no_readers = Lock()
		self.__no_writers = Lock()
		self.__readers_queue = Lock()

	def reader_acquire(self):
		self.__readers_queue.acquire()
		self.__no_readers.acquire()
		self.__read_switch.acquire(self.__no_writers)
		self.__no_readers.release()
		self.__readers_queue.release()

	def reader_release(self):
		self.__read_switch.release(self.__no_writers)

	def writer_acquire(self):
		self.__write_switch.acquire(self.__no_readers)
		self.__no_writers.acquire()

	def writer_release(self):
		self.__no_writers.release()
		self.__write_switch.release(self.__no_readers)
	

class _LightSwitch:
	def __init__(self):
		self.__counter = 0
		self.__mutex = Lock()

	def acquire(self, lock):
		self.__mutex.acquire()
		self.__counter += 1
		if self.__counter == 1:
			lock.acquire()
		self.__mutex.release()

	def release(self, lock):
		self.__mutex.acquire()
		self.__counter -= 1
		if self.__counter == 0:
			lock.release()
		self.__mutex.release()


"""
The directory service that updates relays' states
"""
class RelayDirectory:
    def __init__(self):
        self.__heartbeat_timeout = 30

    def update_relay_info(self, msg):
        # ts ip port key type status
        relay_msg = msg.decode(ENCODING).split()

        ts = int(relay_msg[0])
        ip = relay_msg[1]
        port = relay_msg[2]
        key = relay_msg[3]
        type = relay_msg[4]
        status = relay_msg[5]

        info = dict()

        with open(RELAY_INFO_FILE, 'r') as json_file:
            info = json.load(json_file)

        info.update({ip: {
            "timestamp": ts,
            "port": port,
            "key": key,
            "type": type,
            "status": status
        }})

        with open(RELAY_INFO_FILE, 'w') as outfile:
            json.dump(info, outfile)

    def get_relay_info(self):
        result = {"guard": [], "middle": [], "exit": []}
        curr_ts = int(time.time())

        with open(RELAY_INFO_FILE, 'r') as json_file:
            info = json.load(json_file)

        for key, value in info.items():
            print(key, value)
            if value["status"] == "ON" and \
                curr_ts - value["timestamp"] <= self.__heartbeat_timeout:
                d = {
                    "ip": key,
                    "port": value["port"],
                    "key": value["key"]
                }
                result[value["type"]].append(d)

        return result


def handle_relays(host, port):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((host, port))
    serversocket.listen(1)

    def get_relay_message(connection):
        buf = bytearray("", encoding=ENCODING)
        buf_size = 0

        while True:
            curr = connection.recv(1024)
            curr_size = len(curr)
            if curr_size <= 0:
                connection.close()
                break

            buf.extend(curr)
            buf_size += curr_size

        rw_lock.writer_acquire()
        directory.update_relay_info(buf)
        rw_lock.writer_release()

        connection.close()


    while True:
        connection, _ = serversocket.accept()
        print("Relay connection accepted...\n")

        p = Process(target=get_relay_message, args=(connection, ))
        p.start()


def handle_clients(host, port):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((host, port))
    serversocket.listen(1)

    def send_client_message(connection):
        buf = connection.recv(1024)
        if len(buf) > 0:
            rw_lock.reader_acquire()
            relay_state = json.dumps(directory.get_relay_info())
            rw_lock.reader_release()

            connection.sendall(bytes(relay_state, encoding=ENCODING))

        connection.close()


    while True:
        connection, _ = serversocket.accept()
        print("Client connection accepted...\n")

        p = Process(target=send_client_message, args=(connection, ))
        p.start()


host = ''
relay_port = 14760
client_port = 14736
relay_info = {}

with open(RELAY_INFO_FILE, 'w') as outfile:
    json.dump(relay_info, outfile)

rw_lock = RWLock()
directory = RelayDirectory()

relay_process = Process(target=handle_relays, args=(host, relay_port, ))
client_process = Process(target=handle_clients, args=(host, client_port, ))

relay_process.start()
client_process.start()
