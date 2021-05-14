from os.path import join

from Minecraft.gui.base import GUI
from Minecraft.source import resource_pack
from Minecraft.utils.utils import *

import pyglet
from pyglet.sprite import Sprite


class Loading(GUI):

    def __init__(self):
        width, height = get_size()
        GUI.__init__(self, width, height)
        self._element = list()
        self._img = resource_pack.get_resource('textures/gui/options_background')
        for x in range(width // self._img.width * 2 + 1):
            for y in range(height // self._img.height * 2 + 1):
                sprite = Sprite(self._img, x=x * self._img.width, y = y * self._img.height)
                sprite.scale = 2
                self._element.append(sprite)

    def resize(self, width, height):
        self._element = list()
        for x in range(width // self._img.width * 2 + 1):
            for y in range(height // self._img.height * 2 + 1):
                sprite = Sprite(self._img, x=x * self._img.width, y = y * self._img.height)
                sprite.scale = 2
                self._element.append(sprite)

    def draw(self):
        for i in self._element:
            i.draw()
