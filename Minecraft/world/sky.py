from pyglet.gl import *

now = 0

def change_sky_color(dt):
    # 改变天空的颜色
    global now
    # 下面6行, 上一行为顶点坐标, 下一行是这3个顶点组成的y关于x的二次函数解析式
    # (0, 0.05), (10, 0.5), (20, 0.05)
    get_color_r = lambda x: -0.0045 * x ** 2 + 0.09 * x + 0.05
    # (0, 0), (10, 0.69), (20, 0)
    get_color_g = lambda x: -0.0069 * x ** 2 + 0.138* x + 0.0
    # (0, 0.15), (10, 1), (20, 0.15)
    get_color_b = lambda x: -0.0085 * x ** 2 + 0.17 * x + 0.15
    if now == 0:
        now = 20
    elif now == 20:
        now = 0
    now += 0.125
    r = get_color_r(now)
    g = get_color_g(now)
    b = get_color_b(now)
    glClearColor(r, g, b, 1.0)
    glFogfv(GL_FOG_COLOR, (GLfloat * 4)(r, g, b, 1.0))

def get_time():
    # 获取当前游戏时间
    return now

def set_time(now_time):
    # 设置当前游戏时间
    global now
    now = now_time
