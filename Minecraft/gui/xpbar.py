from os.path import join

from Minecraft.gui.base import GUI
from Minecraft.source import path
from Minecraft.utils.utils import *

import pyglet
from pyglet import image
from pyglet.sprite import Sprite

class XPBar(GUI):

    def __init__(self):
        width, height = get_size()
        GUI.__init__(self, width, height)
        self._element = []
        for i in range(27):
            self._element.append(Sprite(image.load(join(path['texture.ui'], 'xpbar_empty.png')).get_region(1, 0, 11, 5),
                    x= (width - 450) // 2 + i * 16.5 - 2, y=64))
            self._element[i].scale = 1.5

    def draw(self):
        for i in self._element:
            i.draw()

    def resize(self, width, height):
        for i in range(27):
            self._element[i].position = (width - 450) // 2 + i * 16.5 - 2, 64

