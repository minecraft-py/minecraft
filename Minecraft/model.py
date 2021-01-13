import math

import pyglet
from pyglet.gl import *

def get_texture_coordinates(x, y, height, width, texture_height, texture_width):
    if x == -1 and y == -1:
        return ()
    x /= float(texture_width)
    y /= float(texture_height)
    height /= float(texture_height)
    width /= float(texture_width)
    return x, y, x + width, y, x + width, y + height, x, y + height

class BoxModel:

    def __init__(self, length, width, height, texture, pixel_length, pixel_width, pixel_height,
            position=(0, 0, 0), rotate=(0, 0, 0)):
        self.image = texture
        self.length, self.width, self.height = length, width, height
        self.pixel_length, self.pixel_width, self.pixel_height = pixel_length, pixel_width, pixel_height
        self.texture_height = self.image.height
        self.texture_width = self.image.width
        self.textures = [(-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1)]
        self.texture_data = None
        self.display = None
        self.position = position
        self.rotate_angle = rotate

    def get_texture_data(self):
        texture_data = []
        texture_data += get_texture_coordinates(self.textures[0][0], self.textures[0][-1], self.pixel_width, self.pixel_length, self.texture_height, self.texture_width)
        texture_data += get_texture_coordinates(self.textures[1][0], self.textures[1][-1], self.pixel_width, self.pixel_length, self.texture_height, self.texture_width)
        texture_data += get_texture_coordinates(self.textures[2][0], self.textures[2][-1], self.pixel_height, self.pixel_width, self.texture_height, self.texture_width)
        texture_data += get_texture_coordinates(self.textures[3][0], self.textures[3][-1], self.pixel_height, self.pixel_width, self.texture_height, self.texture_width)
        texture_data += get_texture_coordinates(self.textures[4][0], self.textures[4][-1], self.pixel_height, self.pixel_length, self.texture_height, self.texture_width)
        texture_data += get_texture_coordinates(self.textures[-1][0], self.textures[-1][-1], self.pixel_height, self.pixel_length, self.texture_height, self.texture_width)
        return texture_data

    def update_texture_data(self, textures):
        self.textures = textures
        self.texture_data = self.get_texture_data()
        self.display = pyglet.graphics.vertex_list(24,
            ('v3f/static', self.get_vertices()),
            ('t2f/static', self.texture_data),
        )

    def get_vertices(self):
        xm = 0
        xp = self.length
        ym = 0
        yp = self.height
        zm = 0
        zp = self.width
        vertices = (
            xm, yp, zm,   xm, yp, zp,   xp, yp, zp,   xp, yp, zm,
            xm, ym, zm,   xp, ym, zm,   xp, ym, zp,   xm, ym, zp,
            xm, ym, zm,   xm, ym, zp,   xm, yp, zp,   xm, yp, zm,
            xp, ym, zp,   xp, ym, zm,   xp, yp, zm,   xp, yp, zp,
            xm, ym, zp,   xp, ym, zp,   xp, yp, zp,   xm, yp, zp,
            xp, ym, zm,   xm, ym, zm,   xm, yp, zm,   xp, yp, zm,
        )
        return vertices

    def draw(self):
        glPushMatrix()
        glBindTexture(self.image.texture.target, self.image.texture.id)
        glEnable(self.image.texture.target)
        glTranslatef(*self.position)
        glRotatef(self.rotate_angle[0] * (180 / float(pi)), 1.0, 0.0, 0.0)
        glRotatef(self.rotate_angle[1] * (180 / float(pi)), 0.0, 1.0, 0.0)
        glRotatef(self.rotate_angle[-1] * (180 / float(pi)), 0.0, 0.0, 1.0)
        self.display.draw(GL_QUADS)
        glPopMatrix()
