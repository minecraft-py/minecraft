import socket
import time
from threading import Thread

from server.utils import *

class Server():

    def __init__(self):
        self.thread = []
        self.thread_count = -1

    def start(self):
        log_info('start server')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('localhost', 10240))
        self.socket.listen(1)
        while True:
            conn, addr = self.socket.accept()
            self.thread_count += 1
            self.thread.append(Thread(target=self.connect, args=(conn, addr)))
            log_info('new connection @ %s:%d, total %d thread(s)' % (addr[0], addr[1], self.thread_count + 1))
            self.thread[self.thread_count].start()

    def connect(self, conn, addr):
        pass
