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
        self._start = Sprite(image.load(join(path['texture.ui'], 'xpbar_empty.png')).get_region(0, 0, 12, 5),
                x=(width - 450) // 2 + 4, y=64)
        for i in range(39):
            self._element.append(Sprite(image.load(join(path['texture.ui'], 'xpbar_empty.png')).get_region(1, 0, 11, 5),
                x=(width - 450) // 2 + 12 + 11 * i + 4, y=64))
        self._end = Sprite(image.load(join(path['texture.ui'], 'xpbar_empty.png')).get_region(1, 0, 12, 5),
            x=(width - 450) // 2 + 12 + 11 * 38 + 4, y=64)

    def draw(self):
        self._start.draw()
        self._end.draw()
        for i in self._element:
            i.draw()

    def resize(self, width, height):
        self._start.position = (width - 450) // 2 + 4, 64
        self._end.position = (width - 450) // 2 + 12 + 11 * 38 + 4, 64
        for i in range(len(self._element)):
            self._element[i].position = (width - 450) // 2 + 12 + 11 * i + 4, 64

