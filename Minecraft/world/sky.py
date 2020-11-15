from pyglet.gl import *

now = 0
step = -0.125

def change_sky_color(dt):
    global now, step
    get_color_r = lambda x: (x - 11.1111111111111) / -22.2222222222222
    get_color_g = lambda x: (x - 10.0) / -14.4927536231884
    get_color_b = lambda x: (x - 11.7647058823529) / -11.7647058823529 
    if now == 10:
        step = -step
    elif now == 0:
        step = -step
    now += step
    r = get_color_r(now)
    g = get_color_g(now)
    b = get_color_b(now)
    glClearColor(r, g, b, 1.0)
