import json
from os.path import join
from sys import platform
import time

from server.utils import *

def search_mcpy():
    # 寻找文件存储位置
    _os = __import__('os')
    environ, path = _os.environ, _os.path
    if 'MCPYPATH' in environ:
        MCPYPATH = environ['MCPYPATH']
    elif platform.startswith('win'):
        MCPYPATH = path.join(path.expanduser('~'), 'mcpy')
    else:
        MCPYPATH = path.join(path.expanduser('~'), '.mcpy')
    return MCPYPATH

path = {}
path['mcpypath'] = search_mcpy()

settings = json.load(open(join(path['mcpypath'], 'server.json'), encoding='utf-8'))
for key in ['port']:
    if key not in settings:
        log_err("server.json: missing '%s' key" % key)
        exit(1)
