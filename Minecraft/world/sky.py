from pyglet.gl import *

now = 0
step = -0.125

def change_sky_color(dt):
    # 改变天空的颜色
    global now, step
    # 根据坐标 (0.5, 0) 与 (0.05, 10) 计算出一次函数 x 关于 y 的解析式, 下同
    get_color_r = lambda y: (y - 11.1111111111111) / -22.2222222222222
    # (0.69, 0) 与 (0, 10)
    get_color_g = lambda y: (y - 10.0) / -14.4927536231884
    # (1, 0) 与 (0.15, 10)
    get_color_b = lambda y: (y - 11.7647058823529) / -11.7647058823529 
    if now == 10:
        step = -step
    elif now == 0:
        step = -step
    now += step
    r = get_color_r(now)
    g = get_color_g(now)
    b = get_color_b(now)
    glClearColor(r, g, b, 1.0)
    glFogfv(GL_FOG_COLOR, (GLfloat * 4)(r, g, b, 1.0))
