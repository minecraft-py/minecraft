import math
import time

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

def normalize(position):
    """ Accepts `position` of arbitrary precision and returns the block
    containing that position.

    Parameters
    ----------
    position : tuple of len 3

    Returns
    -------
    block_position : tuple of ints of len 3

    """
    x, y, z = position
    x, y, z = (int(round(x)), int(round(y)), int(round(z)))
    return (x, y, z)

def sectorize(position):
    """ Returns a tuple representing the sector for the given `position`.

    Parameters
    ----------
    position : tuple of len 3

    Returns
    -------
    sector : tuple of len 3

    """
    x, y, z = normalize(position)
    x, y, z = x // SECTOR_SIZE, y // SECTOR_SIZE, z // SECTOR_SIZE
    return (x, 0, z)

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

def log_err(text):
    print('[%s ERR ]: %s' % (time.strftime('%H:%M:%S'), text))

def log_info(text):
    print('[%s INFO]: %s' % (time.strftime('%H:%M:%S'), text))

def log_warn(text):
    print('[%s WARN]: %s' % (time.strftime('%H:%M:%S'), text))

FACES = [
    ( 0, 1, 0),
    ( 0,-1, 0),
    (-1, 0, 0),
    ( 1, 0, 0),
    ( 0, 0, 1),
    ( 0, 0,-1),
]

TICKS_PER_SEC = 20
SECTOR_SIZE = 16

MAX_SIZE = 16

STEALING_SPEED = 3
WALKING_SPEED = 5
RUNNING_SPEED = 8
FLYING_SPEED = 10

GRAVITY = 20.0
MAX_JUMP_HEIGHT = 1.0
# 获得跳跃的高度, 首先计算公式:
#    v_t = v_0 + a * t
# for the time at which you achieve maximum height, where a is the acceleration
# due to gravity and v_t = 0. This gives:
#    t = - v_0 / a
# Use t and the desired MAX_JUMP_HEIGHT to solve for v_0 (jump speed) in
#    s = s_0 + v_0 * t + (a * t ** 2) / 2
JUMP_SPEED = math.sqrt(2 * GRAVITY * MAX_JUMP_HEIGHT)
TERMINAL_VELOCITY = 50

PLAYER_HEIGHT = 2
