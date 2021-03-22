import json
import socket
import time
import threading

from Minecraft.source import player
from Minecraft.utils.utils import *


class Client():

    def __init__(self, ip, addr):
        # 创建&连接套接字
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect((ip, addr))
        self.socket.send('client'.encode())
        data = self.socket.recv(1024).decode()
        # 互换版本号
        if data.startswith('server '):
            log_info('server version %s' % json.loads(data[7:])['version'])
            self.socket.send(('client {"version": "%s"}' % VERSION['str']).encode())
            data = self.socket.recv(1024).decode()
            if data == 'refused':
                self.connected = False
                return
            elif data == 'welcome':
                data = self.socket.recv(1024).decode()
                # 请求玩家名称及 UUID
                if data == 'get_player':
                    self.socket.send(('player {"id": "%s", "name": "%s"}' % (player['id'], player['name'])).encode())
                    data = self.socket.recv(1024).decode()
                    if data == 'refused':
                        self.connected = False
                    elif data == 'welcome ' + player['name']:
                        # 验证成功
                        self.connected = True

def get_info(ip, addr):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((ip, addr))
    now = time.time()
    s.send('get_info'.encode())
    data = json.loads(s.recv(1024).decode())
    data['delay'] = (data['time'] - now) * 1000
    del data['time']
    return data
