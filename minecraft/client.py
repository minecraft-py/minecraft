import json
import socket
import time
import threading

from minecraft.source import player
from minecraft.utils.utils import *

def connect(ip, addr):
    # 创建&连接套接字
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((ip, addr))
    s.send('client'.encode())
    data = s.recv(1024).decode()
    if data == 'refuse':
        return False
    # 互换版本号
    elif data.startswith('server '):
        log_info('server version %s' % json.loads(data[7:])['str'])
        s.send(('client {"version": %s}' % VERSION['data']).encode())
        data = s.recv(1024).decode()
        if data == 'refused':
            return False
        else:
            # 请求玩家名称及 UUID
            if data == 'get_player':
                s.send(('player {"id": "%s", "name": "%s"}' % (player['id'], player['name'])).encode())
                data = s.recv(1024).decode()
                if data == 'refused':
                    return False
                elif data == 'welcome ' + player['name']:
                    # 验证成功
                    return s

def get_info(ip, addr):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((ip, addr))
    now = time.time()
    s.send('get_info'.encode())
    data = json.loads(s.recv(1024).decode())
    data['delay'] = (data['time'] - now) * 1000
    del data['time']
    return data
