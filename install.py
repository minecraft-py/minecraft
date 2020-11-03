#!/usr/bin/env python3

from os import environ, mkdir, path, system
from shutil import copyfile, copytree
from register import register_user

# 下载依赖项
print('[install requirements]')
if (code := system('pip install -r requirements.txt')) != 0:
    print('pip raise error code: %d' % code)
    exit(1)
else:
    print('install successfully')
# 注册玩家
print('[register]')
register_user()
# 复杂运行所需的文件
print('[copy lib]')
for xdir in ['screenshot', 'save']:
    if not path.isdir(xdir):
        mkdir(path.join(environ['MCPYPATH'], xdir))
# 完成!
print('[done]')
