#!/usr/bin/env python3

from os import environ, mkdir, path, system
from shutil import copyfile, copytree, rmtree
from register import register_user

# 下载依赖项
print('[install requirements]')

"""
# 适用于 python3 -m pip，以备你没有可执行的pip
if (code := system('python.exe -m pip install -r requirements.txt')) != 0:
    print('pip raise error code: %d' % code)
    exit(1)
else:
    print('install successfully')
"""
# 注册玩家
print('[register]')
register_user()
# 复杂运行所需的文件
print('[copy lib]')

if (MCPYPATH := environ.get('MCPYPATH')) != None:

    copyfile(path.join('data', 'json', 'settings.json'), path.join(MCPYPATH, 'settings.json'))
    copyfile(path.join('data', 'json', 'window.json'), path.join(MCPYPATH, 'window.json'))

    if not path.isdir(path.join(MCPYPATH, 'save')):
        mkdir(path.join(MCPYPATH, 'save'))

    else:
        print('$MCPYPATH/save existed')
    
    if not path.isdir(path.join(MCPYPATH, 'screenshot')):
        mkdir(path.join(MCPYPATH, 'screenshot'))

    else:
        print('$MCPYPATH/screenshot existed')
    
    if not path.isdir(path.join(MCPYPATH, 'texture', 'default')):
        copytree(path.join('data', 'texture'), path.join(MCPYPATH, 'texture', 'default'))

    else:
        rmtree(MCPYPATH, 'texture', 'default')
        copytree(path.join('data', 'texture'), path.join(MCPYPATH, 'texture', 'default'))
else:
    print('MCPYPATH path not found')

# 完成!
print('[done]')
