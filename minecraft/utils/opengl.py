from pyglet.image import Texture
from pyglet.gl import *


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
