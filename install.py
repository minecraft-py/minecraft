#!/usr/bin/env python3

from json import dump
from os import environ, mkdir, path, system
from re import match
from shutil import copyfile, copytree, rmtree
from sys import platform
import uuid

def copy():
    MCPYPATH = search_mcpy()
    if not path.isdir(MCPYPATH):
        mkdir(MCPYPATH)
    if not path.isfile(path.join(MCPYPATH, 'server.json')):
        copyfile(path.join('data', 'json', 'server.json'), path.join(MCPYPATH, 'server.json'))
    if not path.isfile(path.join(MCPYPATH, 'settings.json')):
        copyfile(path.join('data', 'json', 'settings.json'), path.join(MCPYPATH, 'settings.json'))
    if not path.isfile(path.join(MCPYPATH, 'window.json')):
        copyfile(path.join('data', 'json', 'window.json'), path.join(MCPYPATH, 'window.json'))
    if not path.isdir(path.join(MCPYPATH, 'log')):
        mkdir(path.join(MCPYPATH, 'log'))
    if not path.isdir(path.join(MCPYPATH, 'save')):
        mkdir(path.join(MCPYPATH, 'save'))
    if not path.isdir(path.join(MCPYPATH, 'screenshot')):
        mkdir(path.join(MCPYPATH, 'screenshot'))
    if path.isdir(path.join(MCPYPATH, 'texture', 'default')):
        rmtree(path.join(MCPYPATH, 'texture', 'default'))
    copytree(path.join('data', 'texture'), path.join(MCPYPATH, 'texture', 'default'))

def install():
    # 下载依赖项
    print('[Install requirements]')
    code = system('pip3 install -U -r requirements.txt')
    if code != 0:
        print('pip raise error code: %d' % code)
        exit(1)
    else:
        print('install successfully')
    # 注册玩家
    print('[Register]')
    register_user()
    # 复制运行所需的文件
    print('[Copy lib]')
    copy()
    # 完成!
    print('[Done]')

def search_mcpy():
    # 搜索文件存储位置
    if 'MCPYPATH' in environ:
        MCPYPATH = environ['MCPYPATH']
    elif platform.startswith('win'):
        MCPYPATH = path.join(path.expanduser('~'), 'mcpy')
    else:
        MCPYPATH = path.join(path.expanduser('~'), '.mcpy')
    return MCPYPATH

def register_user():
    # 注册
    if 'MCPYPATH' not in environ:
        environ['MCPYPATH'] = search_mcpy()
    if not path.isdir(environ['MCPYPATH']):
        mkdir(environ['MCPYPATH'])
    if not path.isfile(path.join(environ['MCPYPATH'], 'player.json')):
        player_id = str(uuid.uuid4())
        print('Your uuid is %s, do not change it' % player_id)
        player_name = ''
        while not match(r'^([a-z]|[A-Z]|_)\w+$', player_name):
            player_name = input('Your name: ')
        dump({'id': player_id, 'name': player_name}, open(path.join(environ['MCPYPATH'], 'player.json'), 'w+'), indent='\t')
        print('Regsitered successfully, you can use your id to play multiplayer game!')
    else:
        print('You have regsitered!')

if __name__ == '__main__':
    install()
