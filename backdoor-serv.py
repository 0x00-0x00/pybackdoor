
import time
import random
from socket import *
from multiprocessing import Queue
from threading import Thread

queue = Queue()
output_queue = Queue()
bind_opt = ('127.0.0.1', 9044)

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(bind_opt)
sock.listen(1)

conn, addr = sock.accept()

def send_data():
    while queue.empty() is not True:
        data = queue.get()
        conn.send(data.encode())
    return 0

def receive_data(sock):
    while True:
        try:
            data = sock.recv(4096)
            print("[Debug] Received data: {0}".format(data))
            output_queue.put(data)
        except timeout:
            pass

print ("[New connection from {0}]".format(':'.join([addr[0], str(addr[1])])))
conn.settimeout(4)

recv_thr = Thread(target=receive_data, args=(conn,)).start()

while True:
    command = input("Type your command: ")
    queue.put(command)
    send_thr = Thread(target=send_data, args=())
    send_thr.start()
    if send_thr is None:
        print("[!] Send thread is None.")
    else:
        print("[+] Waiting to send ...")
        send_thr.join()
        print("[+] Sent.")

recv_thr.join()


