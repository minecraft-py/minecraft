import atexit
import math
import time

_have_color = None
try:
    from colorama import Fore, Style, init
    init()
except ModuleNotFoundError:
    _have_color = False
else:
    _have_color = True

import pyglet

def cube_vertices(x, y, z, n):
    # 返回在 x, y, z 坐标的方形顶点 
    return [
            x-n,y+n,z-n, x-n,y+n,z+n, x+n,y+n,z+n, x+n,y+n,z-n,  # 顶部
            x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # 底部
            x-n,y-n,z-n, x-n,y-n,z+n, x-n,y+n,z+n, x-n,y+n,z-n,  # 左边
            x+n,y-n,z+n, x+n,y-n,z-n, x+n,y+n,z-n, x+n,y+n,z+n,  # 右边
            x-n,y-n,z+n, x+n,y-n,z+n, x+n,y+n,z+n, x-n,y+n,z+n,  # 前面
            x+n,y-n,z-n, x-n,y-n,z-n, x-n,y+n,z-n, x+n,y+n,z-n,  # 后面
        ]

def get_size():
    # 返回窗口大小
    for w in pyglet.canvas.get_display().get_windows():
        if str(w).startswith('Game'):
            return w.width, w.height
    else:
        return 800, 600

def get_game():
    # 获取 Game 类
    for w in pyglet.canvas.get_display().get_windows():
        if str(w).startswith('Game'):
            return w

def log_err(text, name='client'):
    # 打印错误信息
    if _have_color:
        print('%s[ERR  %s %s]%s %s' % (Fore.RED, time.strftime('%H:%M:%S'), name, Style.RESET_ALL, text))
    else:
        print('[ERR  %s %s] %s' % (time.strftime('%H:%M:%S'), name, text))

def log_info(text, name='client'):
    # 打印信息
    if _have_color:
        print('%s[INFO %s %s]%s %s' % (Fore.GREEN, time.strftime('%H:%M:%S'), name, Style.RESET_ALL, text))
    else:
        print('[INFO %s %s] %s' % (time.strftime('%H:%M:%S'), name, text))

def log_warn(text, name='client'):
    # 打印警告信息
    if _have_color:
        print('%s[WARN %s %s]%s %s' % (Fore.YELLOW, time.strftime('%H:%M:%S'), name, Style.RESET_ALL, text))
    else:
        print('[WARN %s %s] %s' % (time.strftime('%H:%M:%S'), name, text))

def normalize(position):
    pos = []
    for n in position:
        pos.append(int(round(n)))
    else:
        return tuple(pos)

@atexit.register
def on_exit():
    log_info('Exit')

def pos2str(position):
    # 将坐标转换为字符串
    return ' '.join([str(s) for s in position])

def search_mcpy():
    # 寻找文件存储位置
    _os  = __import__('os')
    _sys = __import__('sys')
    platform = _sys.platform
    environ, path = _os.environ, _os.path
    if 'MCPYPATH' in environ:
        MCPYPATH = environ['MCPYPATH']
    elif platform == 'darwin':
        MCPYPATH = path.join(path.expanduser('~'), 'Library', 'Application Support', 'mcpy')
    elif platform.startswith('win'):
        MCPYPATH = path.join(path.expanduser('~'), 'mcpy')
    else:
        MCPYPATH = path.join(path.expanduser('~'), '.mcpy')
    return MCPYPATH

def sectorize(position):
    # 返回坐标所在的区块
    x, y, z = normalize(position)
    x, y, z = x // SECTOR_SIZE, y // SECTOR_SIZE, z // SECTOR_SIZE
    return (x, 0, z)

def str2pos(string, float_=False):
    # pos2str 的逆函数
    if float_:
        return tuple([float(i) for i in string.split(' ')])
    else:
        return tuple([int(float(i)) for i in string.split(' ')])

FACES = [
    ( 0, 1, 0),
    ( 0,-1, 0),
    (-1, 0, 0),
    ( 1, 0, 0),
    ( 0, 0, 1),
    ( 0, 0,-1),
]

VERSION = {
        'major': 0,
        'minor': 3,
        'patch': 2,
        'str': '0.3.2',
        'data': 1
    }

TICKS_PER_SEC = 60
SECTOR_SIZE = 16

MAX_SIZE = 32
SEA_LEVEL = 10

STEALING_SPEED = 3
WALKING_SPEED = 5
RUNNING_SPEED = 8
FLYING_SPEED = 10

GRAVITY = 20.0
MAX_JUMP_HEIGHT = 1.2
JUMP_SPEED = math.sqrt(2 * GRAVITY * MAX_JUMP_HEIGHT)
TERMINAL_VELOCITY = 36
