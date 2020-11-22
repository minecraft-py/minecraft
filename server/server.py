import json
from os import getpid
import socket
import time
import threading

from server.client import Client
from server.utils import *

import psutil

class Server():

    def __init__(self):
        self.console_thread = None
        self.thread = {}
        self.thread_count = -1

    def start(self):
        # 开启服务器
        log_info('start server @ localhost:16384')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('localhost', 16384))
        self.socket.listen(5)
        while True:
            try:
                conn, addr = self.socket.accept()
            except:
                log_info('server stopped')
                break
            data = conn.recv(1024).decode()
            if self.console_thread != None and not self.console_thread.is_alive():
                self.console_thread = None
            if data == 'client':
                # 客户端连接
                self.thread_count += 1
                self.thread[self.thread_count] = threading.Thread(target=self.client, args=(conn, addr),
                        name='t{0}'.format(self.thread_count))
                log_info('new connection @ %s:%d, total %d thread(s)' % (addr[0], addr[1], self.thread_count + 1))
                self.thread[self.thread_count].start()
            elif data == 'console':
                # 控制台连接
                if addr[0] == '127.0.0.1' and self.console_thread == None:
                    log_info('connected to console @ %s:%d' % (addr[0], addr[1]))
                    conn.send('welcome'.encode())
                    self.console_thread = threading.Thread(target=self.console, args=(conn, addr), name='console')
                    self.console_thread.start()
                else:
                    conn.send('refused'.encode())
            else:
                conn.send('unknow'.encode())

    def client(self, conn, addr):
        # 客户端连接
        log_info('new client thread')
        # 互换版本号
        # 发送: server {"version": VERSION}
        conn.send('server {0}'.format(json.dumps({'version': VERSION})).encode())
        version = conn.recv(1024).decode()
        # 期望接收到: client {"version": VERSION}
        if version.startswith('client '):
            try:
                client_ver = json.loads(version[7:])['version']
            except:
                log_info('unknow client version: %s' % version[7:])
                conn.send('refused'.encode())
                conn.close()
                return
            else:
                # 接收到正确版本
                log_info('client version: %s' % client_ver)
                conn.send('welcome'.encode())
        else:
            conn.send('refused'.encode())
            conn.close()
            return
        # 请求玩家名称及 UUID
        conn.send('get_player'.encode())
        player = conn.recv(1024).decode()
        if player.startswith('player '):
            try:
                player = json.loads(player[7:])
            except:
                log_info('unknow player: %s' % player)
                conn.send('refused'.encode())
                conn.close()
                return
            else:
                # 接收到正确的玩家数据
                log_info('new player: id: %s, name: %s' % (player['id'], player['name']))
                conn.send('welcome {0}'.format(player['name']).encode())
        else:
            conn.send('refused'.encode())
            conn.close()
            return
        client = Client(conn, addr, client_ver, player)

    def console(self, conn, addr):
        # 控制台连接
        log_info('new console')
        conn.send('Minecraft server version {0}'.format(VERSION).encode())
        while True:
            data = conn.recv(1024).decode()
            log_info('command: %s' % data)
            if data == 'exit':
                conn.close()
                break
            elif data == 'help':
                data = 'available commands:\n  exit help ip status threads version(ver)'
                conn.send(data.encode())
            elif data == 'ip':
                conn.send('ip addr: {0}:{1}'.format(*addr).encode())
            elif data == 'status':
                mem = round(psutil.Process(getpid()).memory_full_info()[7] / 1048576, 2)
                data = ''
                for t in threading.enumerate():
                    data += t.getName() + ' '
                data = 'running:\n  ' + data + '\nall client thread:\n  '
                for t in self.thread.values():
                    data += t.getName() + ' '
                data += '\nmemory use:\n  %.2fMB' % mem
                conn.send(data.encode())
            elif data == 'threads':
                conn.send('total {0} thread(s)'.format(self.thread_count + 1).encode())
            elif data == 'version' or data == 'ver':
                conn.send('version {0}'.format(VERSION).encode())
            else:
                conn.send('command not found'.encode())
