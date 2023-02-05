# Copyright 2020-2023 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

from pyglet.image import Texture
from pyglet.gl import *


def setup_opengl():
    glClearColor(0.5, 0.69, 1.0, 1)
    glEnable(GL_BLEND)
    glEnable(GL_CULL_FACE)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    Texture.default_min_filter = GL_NEAREST
    Texture.default_mag_filter = GL_NEAREST
