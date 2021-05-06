import json
import socket
import time
import threading

from Minecraft.source import player
from Minecraft.utils.utils import *

def connect(self, ip, addr):
    # 创建&连接套接字
    socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket.connect((ip, addr))
    socket.send('client'.encode())
    data = socket.recv(1024).decode()
    # 互换版本号
    if data.startswith('server '):
        log_info('server version %s' % json.loads(data[7:])['version'])
        socket.send(('client {"version": %s}' % VERSION['data']).encode())
        data = socket.recv(1024).decode()
        if data == 'refused':
            return False
        elif data == 'welcome':
            data = socket.recv(1024).decode()
            # 请求玩家名称及 UUID
            if data == 'get_player':
                socket.send(('player {"id": "%s", "name": "%s"}' % (player['id'], player['name'])).encode())
                data = socket.recv(1024).decode()
                if data == 'refused':
                    return False
                elif data == 'welcome ' + player['name']:
                    # 验证成功
                    return socket

def get_info(ip, addr):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((ip, addr))
    now = time.time()
    s.send('get_info'.encode())
    data = json.loads(s.recv(1024).decode())
    data['delay'] = (data['time'] - now) * 1000
    del data['time']
    return data
