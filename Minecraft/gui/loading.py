from os.path import join

from Minecraft.gui.base import GUI
from Minecraft.source import path
from Minecraft.utils.utils import *

import pyglet
from pyglet import image
from pyglet.sprite import Sprite


class Loading(GUI):

    def __init__(self):
        width, height = get_size()
        GUI.__init__(self, width, height)
        self._element = []
        self._img = image.load(join(path['texture.ui'], 'bg32.png'))
        for x in range(width // self._img.width + 1):
            for y in range(height // self._img.height + 1):
                sprite = Sprite(self._img, x=x * self._img.width, y = y * self._img.height)
                self._element.append(sprite)

    def resize(self, width, height):
        self._element = []
        for x in range(width // self._img.width + 1):
            for y in range(height // self._img.height + 1):
                sprite = Sprite(self._img, x=x * self._img.width, y = y * self._img.height)
                self._element.append(sprite)

    def draw(self):
        for i in self._element:
            i.draw()
