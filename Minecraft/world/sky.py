from pyglet.gl import *

now = 0
step = -0.125

def change_sky_color(dt):
    # 改变天空的颜色
    global now, step
    get_color_r = lambda x: 0.0045 * x ** 2 - 0.09 * x + 0.5
    get_color_g = lambda x: 0.0069 * x ** 2 - 0.138* x + 0.69
    get_color_b = lambda x: 0.0085 * x ** 2 - 0.17 * x + 1.0
    if now == 0 or now == 20:
        step = -step
    now += step
    print(now, step)
    r = get_color_r(now)
    g = get_color_g(now)
    b = get_color_b(now)
    glClearColor(r, g, b, 1.0)
    glFogfv(GL_FOG_COLOR, (GLfloat * 4)(r, g, b, 1.0))

def get_time():
    # 获取当前游戏时间
    global now, step
    return [now, step]

def set_time(now_time, step_time):
    # 设置当前游戏时间
    global now, step
    now, step = now_time, step_time
