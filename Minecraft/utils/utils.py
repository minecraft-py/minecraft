import atexit
import math
import time

from colorama import Fore, Style, init
import pyglet

init()

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
        if w.caption == 'Minecraft' and str(w).startswith('Game'):
            return w.width, w.height
    else:
        return 800, 600

def log_err(text):
    # 打印错误信息
    print('%s[ERR  %s]%s %s' % (Fore.RED, time.strftime('%H:%M:%S'), Style.RESET_ALL, text))

def log_info(text):
    # 打印信息
    print('%s[INFO %s]%s %s' % (Fore.GREEN, time.strftime('%H:%M:%S'), Style.RESET_ALL, text))

def log_warn(text):
    # 打印警告信息
    print('%s[WARN %s]%s %s' % (Fore.YELLOW, time.strftime('%H:%M:%S'), Style.RESET_ALL, text))

def normalize(position):
    x, y, z = position
    x, y, z = (int(round(x)), int(round(y)), int(round(z)))
    return (x, y, z)

@atexit.register
def on_exit():
    log_info('exit')

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
        'patch': 1,
        'str': '0.3.1'
        }

TICKS_PER_SEC = 60
SECTOR_SIZE = 16

MAX_SIZE = 32

STEALING_SPEED = 3
WALKING_SPEED = 5
RUNNING_SPEED = 8
FLYING_SPEED = 10

GRAVITY = 20.0
MAX_JUMP_HEIGHT = 1.0
JUMP_SPEED = math.sqrt(2 * GRAVITY * MAX_JUMP_HEIGHT)
TERMINAL_VELOCITY = 50

PLAYER_HEIGHT = 2
