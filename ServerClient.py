from socket import *  # Package für Sockets
import threading  # Package für Threads, Timer , Events
import os  # Package für Subprocess Komando Bash Skripte)
import time  # Package für die Messung von Systemzeiten


class MyClient:
    server_port = 50007
    bufsize = 1024
    host = "192.168.2.119"

    def __init__(self):

        self.data_recv = None
        self.data_send = None
        self.socket_connection = socket(AF_INET, SOCK_STREAM)
        self.thread_recv = threading.Thread(target=self.worker_recv)
        self.thread_send = threading.Thread(target=self.worker_send)
        self.laufzeit = 30
        self.socket_connection.connect((self.host, self.server_port))
        print("Verbunden mit dem Server %s: " % (self.host))
        self.exit = False
        self.thread_recv.start()
        self.thread_send.start()

    def worker_recv(self):
        while self.exit == False:
            self.data_recv = self.socket_connection.recv = (self.bufsize)
            if self.data_recv != None:
                print(("Client empfängt Nachricht %s" % self.data_recv))

    def worker_send(self):
        while self.exit == False:
            self.data_send = os.popen('vcgencmd measure_temp').readline()
            self.data_send = "Client" + str(self.data_send) + " Noch: " + str(self.laufzeit) + " Sekunden"
            self.socket_connection.send(self.data_send.encode())
            self.laufzeit -= 1
            time.sleep(1)

    def stopp_connection(self):
        self.exit = True
        self.thread_recv.join()
        self.thread_send.join()
        self.socket_connection.close()


client = MyClient()
while client.laufzeit >= 0:
    None
client.stopp_connection()
