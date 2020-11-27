import json
from os import getpid
import socket
import time
import threading

from server.player import Player
from server.source import settings
from server.utils import *

import psutil

class Server():

    def __init__(self):
        # 控制台线程
        self.console_thread = None
        # 线程
        self.thread = []
        self.thread_count = -1
        # 玩家
        self.player = {}
        self.world = {}

    def start(self):
        # 开启服务器
        log_info('start server @ localhost:%d' % settings['port'])
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('localhost', settings['port']))
        self.socket.listen(5)
        while True:
            try:
                conn, addr = self.socket.accept()
            except:
                print()
                log_info('server stopped')
                break
            data = conn.recv(1024).decode()
            if self.console_thread != None and not self.console_thread.is_alive():
                self.console_thread = None
            if data == 'client':
                # 客户端连接
                self.thread_count += 1
                self.thread.append(threading.Thread(target=self.client, args=(conn, addr),
                        name='t{0}'.format(self.thread_count)))
                log_info('new connection @ %s:%d, total %d thread(s)' % (addr[0], addr[1], self.thread_count + 1))
                self.thread[self.thread_count].start()
            elif data == 'console %s' % settings['password']:
                # 控制台连接
                if self.console_thread == None:
                    log_info('connected to console @ %s:%d' % (addr[0], addr[1]))
                    conn.send('welcome'.encode())
                    self.console_thread = threading.Thread(target=self.console, args=(conn, addr), name='console')
                    self.console_thread.start()
                else:
                    conn.send('refused'.encode())
            else:
                conn.send('refused'.encode())

    def client(self, conn, addr):
        # 客户端连接
        log_info('new client thread')
        if (player := self.connect_to_client(conn)) == False:
            return
        conn.send('position {0}'.format(pos2str(self.player[player].position)).encode())

    def connect_to_client(self, conn):
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
                return False
            else:
                # 接收到正确版本
                log_info('client version: %s' % client_ver)
                conn.send('welcome'.encode())
        else:
            conn.send('refused'.encode())
            conn.close()
            return False
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
                return False
            else:
                # 接收到正确的玩家数据
                log_info('new player: id: %s, name: %s' % (player['id'], player['name']))
                conn.send('welcome {0}'.format(player['name']).encode())
                self.player[player['id']] = Player(player['id'])
                self.player[player['id']].position = str2pos(settings['spawn_position'])
                return player['id']
        else:
            conn.send('refused'.encode())
            conn.close()
            return False

    def console(self, conn, addr):
        # 控制台连接
        log_info('new console')
        conn.send('Minecraft server version {0}'.format(VERSION).encode())
        while True:
            data = conn.recv(1024).decode()
            if data == 'exit':
                log_info('console exit')
                conn.close()
                break
            elif data == 'help':
                data = 'available commands:\n  exit help ip status stop threads version(ver)'
                conn.send(data.encode())
            elif data == 'ip':
                conn.send('ip addr: {0}:{1}'.format(*addr).encode())
            elif data == 'status':
                mem = round(psutil.Process(getpid()).memory_full_info()[7] / 1048576, 2)
                data = ''
                for t in threading.enumerate():
                    data += t.getName() + ' '
                data = 'running:\n  ' + data + '\nall client thread:\n  '
                for t in self.thread:
                    data += t.name + ' '
                data += '\nmemory used:\n  %.2fMB' % mem
                conn.send(data.encode())
            elif data == 'stop':
                log_info('server stopped by console')
                psutil.Process(getpid()).kill()
            elif data == 'threads':
                conn.send('total {0} thread(s)'.format(self.thread_count + 1).encode())
            elif data == 'version' or data == 'ver':
                conn.send('version {0}'.format(VERSION).encode())
            else:
                conn.send('command not found'.encode())
