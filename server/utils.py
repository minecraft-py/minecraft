from sys import platform
import time
from threading import get_native_id as get_id

def log_err(text):
    # 打印错误信息
    print('[%s ERR ]: %d : %s' % (time.strftime('%H:%M:%S'), get_id(), text))

def log_info(text):
    # 打印信息
    print('[%s INFO]: %d: %s' % (time.strftime('%H:%M:%S'), get_id(), text))

def log_warn(text):
    # 打印警告信息
    print('[%s WARN]: %d: %s' % (time.strftime('%H:%M:%S'), get_id(), text))

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

VERSION = '0.2'
