import math
import time

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
        if w.caption == 'Minecraft' and w.__class__.__name__ == 'Game':
            return w.width, w.height
    else:
        return 800, 600

def log_err(text):
    # 打印错误信息
    print('[%s ERR ]: %s' % (time.strftime('%H:%M:%S'), text))

def log_info(text):
    # 打印信息
    print('[%s INFO]: %s' % (time.strftime('%H:%M:%S'), text))

def log_warn(text):
    # 打印警告信息
    print('[%s WARN]: %s' % (time.strftime('%H:%M:%S'), text))

def normalize(position):
    x, y, z = position
    x, y, z = (int(round(x)), int(round(y)), int(round(z)))
    return (x, y, z)

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

def tex_coord(x, y, n=4):
    #返回纹理正方形绑定的顶点
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m

def tex_coords(top, bottom, side):
    # 返回纹理正方形的顶面, 底面, 侧面
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side = tex_coord(*side)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side * 4)
    return result

def tex_coords_all(top, bottom, side0, side1, side2, side3):
    # 返回纹理正方形所有的面
    # 同 tex_coords() 类似, 但是要传入全部的四个侧面
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side0, side1 = tex_coord(*side0), tex_coord(*side1)
    side2, side3 = tex_coord(*side2), tex_coord(*side3)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side0)
    result.extend(side1)
    result.extend(side2)
    result.extend(side3)
    return result

FACES = [
    ( 0, 1, 0),
    ( 0,-1, 0),
    (-1, 0, 0),
    ( 1, 0, 0),
    ( 0, 0, 1),
    ( 0, 0,-1),
]

VERSION = 'classic 0.2'

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
