
import sys
import time
import random
from socket import *
from multiprocessing import Queue
from threading import Thread

queue = Queue()
output_queue = Queue()
bind_opt = ('127.0.0.1', 9044)
INTERVAL = 30

#  Create socket
sock = socket(AF_INET, SOCK_STREAM)


def set_socket(sock):
    try:
        sock.bind(bind_opt)
        sock.listen(1)
        print("[+] Socket listening on *:{0}".format(bind_opt[1]))
        return 0
    except OSError:
        print("[+] Socket is already in use. Retrying in {0} seconds ...".format(INTERVAL))
        time.sleep(INTERVAL)
        return -1


def send_data():
    while queue.empty() is not True:
        data = queue.get()
        conn.send(data.encode())
    return 0


def receive_data(sock):
    while True:
        try:
            data = sock.recv(4096)
            if data != b"\00\00":
                print(data.decode())
            output_queue.put(data)
        except timeout:
            pass
        except OSError:
            #  The socket is already shut down.
            sys.exit(0)
            return 0


#  Loop until socket is bind.
sock_stat = set_socket(sock)
while sock_stat is not 0:
    sock_stat = set_socket(sock)

#  Wait for connections
conn, addr = sock.accept()

print ("[New connection from {0}]".format(':'.join([addr[0], str(addr[1])])))
conn.settimeout(4)

recv_thr = Thread(target=receive_data, args=(conn,)).start()

print("Type commands: ")
while True:
    try:
        command = input("")
        queue.put(command)
        send_thr = Thread(target=send_data, args=())
        send_thr.start()
    except KeyboardInterrupt:
        print("[+] Closing connection ...")
        conn.close()
        sys.exit(0)

recv_thr.join()


