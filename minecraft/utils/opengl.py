from minecraft.utils.utils import *

from pyglet.image import Texture
from pyglet.gl import *

_is_blind = False

def setup_opengl():
    glClearColor(0.5, 0.69, 1.0, 1)
    glEnable(GL_BLEND)
    glEnable(GL_CULL_FACE)
    glEnable(GL_FOG)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.5, 0.69, 1.0, 1))
    glFogf(GL_FOG_START, 30.0)
    glFogf(GL_FOG_END, 60.0)
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glHint(GL_FOG_HINT, GL_DONT_CARE)
    Texture.default_min_filter = GL_NEAREST
    Texture.default_mag_filter = GL_NEAREST

def toggle_blind(change=True):
    global _is_blind
    if change:
        _is_blind = not _is_blind
    if _is_blind:
        glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0, 0, 0, 1))
        glFogf(GL_FOG_START, 2)
        glFogf(GL_FOG_END, 3)
    else:
        change_sky_color(0)
        glFogf(GL_FOG_START, 30)
        glFogf(GL_FOG_END, 60)

def is_blind():
    return _is_blind

def change_sky_color(dt):
    # 改变天空的颜色
    # 下面6行, 上一行为顶点坐标, 下一行是这3个顶点组成的y关于x的二次函数解析式
    # (0, 0.05), (10, 0.5), (20, 0.05)
    get_color_r = lambda x: -0.0045 * x ** 2 + 0.09 * x + 0.05
    # (0, 0), (10, 0.69), (20, 0)
    get_color_g = lambda x: -0.0069 * x ** 2 + 0.138* x + 0.0
    # (0, 0.15), (10, 1), (20, 0.15)
    get_color_b = lambda x: -0.0085 * x ** 2 + 0.17 * x + 0.15
    now = int(get_game().time) % 1200 / 60
    r = get_color_r(now)
    g = get_color_g(now)
    b = get_color_b(now)
    glClearColor(r, g, b, 1.0)
    if is_blind():
        glFogfv(GL_FOG_COLOR, (GLfloat * 4)(r, g, b, 1.0))
        toggle_blind(False)
