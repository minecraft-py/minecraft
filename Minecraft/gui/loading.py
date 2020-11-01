from os.path import join

from Minecraft.source import path
from Minecraft.gui.base import GUI

import pyglet
from pyglet import image
from pyglet.sprite import Sprite


class Loading(GUI):

    def __init__(self, width, height):
        GUI.__init__(self, width, height)
        self.loading = Sprite(image.load(join(path['texture'], 'loading.png')))
        self.loading.x = 0
        self.loading.y = 0
        self.loading.scale_x = width / self.loading.width
        self.loading.scale_y = height / self.loading.height

    def resize(self, width, height):
        self.loading.x = 0
        self.loading.y = 0
        self.loading.scale_x = width / self.loading.width
        self.loading.scale_y = height / self.loading.height

    def draw(self):
        self.loading.draw()

