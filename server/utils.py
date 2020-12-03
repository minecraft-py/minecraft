from sys import platform
import time
from threading import get_native_id as get_id

from colorama import Fore, Style

def log_err(text):
    # 打印错误信息
    print('%s[ERR  %s %d]%s %s' % (Fore.RED, time.strftime('%H:%M:%S'), get_id(), Style.RESET_ALL, text))

def log_info(text):
    # 打印信息
    print('%s[INFO %s %d]%s %s' % (Fore.GREEN, time.strftime('%H:%M:%S'), get_id(), Style.RESET_ALL, text))

def log_warn(text):
    # 打印警告信息
    print('%s[WARN %s %d]%s %s' % (Fore.YELLOW, time.strftime('%H:%M:%S'), get_id(), Style.RESET_ALL, text))

def pos2str(position):
    # 将坐标转换为字符串
    return ' '.join([str(s) for s in position])

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

def str2pos(string, float_=False):
    # pos2str 的逆函数
    if float_:
        return tuple([float(i) for i in string.split(' ')])
    else:
        return tuple([int(float(i)) for i in string.split(' ')])

VERSION = '0.2'
