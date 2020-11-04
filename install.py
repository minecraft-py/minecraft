#!/usr/bin/env python3

from os import environ, mkdir, path, system
from shutil import copyfile, copytree, rmtree
from sys import platform
from register import register_user

# 下载依赖项
print('[install requirements]')
if (code := system('python -m pip install -r requirements.txt')) != 0:
    print('pip raise error code: %d' % code)
    exit(1)
else:
    print('install successfully')
# 注册玩家
print('[register]')
register_user()
# 复制运行所需的文件/
print('[copy lib]')
# 特定的平台, 特定的场景
MCPYPATH = ''
if 'MCPYPATH' in environ:
    MCPYPATH = environ['MCPYPATH']
elif platform.startswith('win'):
    MCPYPATH = path.join(environ['HOME'], mcpy)
else:
    MCPYPATH = path.join(path.expanduser('~'), '.mcpy')
# 正式复制文件/目录
if not path.isdir(MCPYPATH):
    mkdir(MCPYPATH)
if not path.isfile(path.join(MCPYPATH, 'settings.json')):
    copyfile(path.join('data', 'json', 'settings.json'), path.join(MCPYPATH, 'settings.json'))
if not path.isfile(path.join(MCPYPATH, 'window.json')):
    copyfile(path.join('data', 'json', 'window.json'), path.join(MCPYPATH, 'window.json'))
if not path.isdir(path.join(MCPYPATH, 'save')):
    mkdir(path.join(MCPYPATH, 'save'))
if not path.isdir(path.join(MCPYPATH, 'screenshot')):
    mkdir(path.join(MCPYPATH, 'screenshot'))
# 完成!
print('[done]')
