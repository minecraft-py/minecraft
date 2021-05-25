from math import radians, cos, sin

from pyglet.gl import *


class Camera3D:
    def __init__(self, position):
        self.position = position
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.rx = 0.0
        self.ry = 0.0

    def goto(self, position):
        self.position = position
        self.update()

    def rotate(self, x, y):
        self.rx = x
        self.ry = y

    def update(self, dt=0):
        self.x, self.y, self.z = self.position

    def transform(self):
        glRotatef(self.rx, 0, 1, 0)
        rx = radians(self.rx)
        glRotatef(-self.ry, cos(rx), 0, sin(rx))
        glTranslatef(-self.x, -self.y, -self.z)

    def look(self):
        glRotatef(self.rx, 0, 1, 0)
        rx = radians(self.rx)
        glRotatef(-self.ry, cos(rx), 0, sin(rx))
        glTranslatef(0, -40.0, 0)
        glRotatef(-90.0, 1, 0, 0)
