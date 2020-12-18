#!/usr/bin/env python3

from json import dump
from os import environ, mkdir, path, system
from re import match
from shutil import copyfile, copytree, rmtree
from sys import platform, argv
import uuid

def copy():
    MCPYPATH = search_mcpy()
    if not path.isdir(MCPYPATH):
        mkdir(MCPYPATH)
    if not path.isfile(path.join(MCPYPATH, 'server.json')):
        copyfile(path.join(get_dir('data'), 'server.json'), path.join(MCPYPATH, 'server.json'))
    if not path.isfile(path.join(MCPYPATH, 'settings.json')):
        copyfile(path.join(get_dir('data'), 'settings.json'), path.join(MCPYPATH, 'settings.json'))
    if not path.isfile(path.join(MCPYPATH, 'window.json')):
        copyfile(path.join(get_dir('data'), 'window.json'), path.join(MCPYPATH, 'window.json'))
    if not path.isdir(path.join(MCPYPATH, 'log')):
        mkdir(path.join(MCPYPATH, 'log'))
    if not path.isdir(path.join(MCPYPATH, 'save')):
        mkdir(path.join(MCPYPATH, 'save'))
    if not path.isdir(path.join(MCPYPATH, 'screenshot')):
        mkdir(path.join(MCPYPATH, 'screenshot'))
    if not path.isdir(path.join(MCPYPATH, 'resource-pack')):
        mkdir(path.join(MCPYPATH, 'resource-pack'))

def install():
    # 下载依赖项
    if not '--no-install-requirements' in argv:
        print('[Install requirements]')
        pip = 'pip'
        for args in argv:
            if args.startswith('--use-pip'):
                pip = args[6:]
        if '--hide-output' in argv:
            code = system('%s install -U -r requirements.txt >> %s' % (pip, path.devnull))
        else:
            code = system('%s install -U -r requirements.txt' % pip)
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

def get_dir(d):
    return path.abspath(path.join(path.dirname(__file__), d))

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

def search_mcpy():
    # 搜索文件存储位置
    if 'MCPYPATH' in environ:
        MCPYPATH = environ['MCPYPATH']
    elif platform.startswith('win'):
        MCPYPATH = path.join(path.expanduser('~'), 'mcpy')
    else:
        MCPYPATH = path.join(path.expanduser('~'), '.mcpy')
    return MCPYPATH

if __name__ == '__main__':
    install()
