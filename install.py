#!/usr/bin/env python3

from os import environ, mkdir, path, system
from shutil import copyfile, copytree, rmtree
from register import register_user, search_mcpy

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
MCPYPATH = search_mcpy()
# 正式复制文件/目录
if not path.isdir(MCPYPATH):
    mkdir(MCPYPATH)
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
# 完成!
print('[done]')
